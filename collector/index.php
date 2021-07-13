<!DOCTYPE html>
<?php
$DB_FILENAME = "/home/pi/weather/weather.db";

function getColor($num) {
    $hash = md5('color' . $num);
    return '#'. hexdec(substr($hash, 0, 5));
}

function get_sensors($db, $column, $lag) {
    return $db->query(
        "SELECT id AS sensor_id, name ".
        "FROM sensors ".
        "WHERE sensor_id IN ( ".
        "    SELECT DISTINCT sensor_id ". 
        "    FROM measurements mx ".
        "    WHERE mx.". $column . " IS NOT NULL AND ".
        "          mx.measured_at > (SELECT DATETIME('now', 'localtime', '".$lag."'))" .
        ");"
    );
}

function get_measurements_on_sensor($db, $sensor, $column_expr, $join, $lag)
{
    $source = array();
    $cmd = $db->prepare("
        SELECT mx.measured_at, " . $column_expr . " AS m ".
        "FROM measurements mx ".
        $join .
        " WHERE mx.sensor_id = :id AND ".
        "       mx.measured_at > (SELECT DATETIME('now', 'localtime', '".$lag."'))" .";"
    );
    $cmd->bindValue(':id', $sensor['sensor_id']);
    $levels = $cmd->execute();
    
    while ($level = $levels->fetchArray()) {
        array_push(
            $source, 
            array("x" => $level["measured_at"], 
                  "y" => floatval($level["m"]))
        );
    }
    $color = getColor($sensor['name']);

    return array(
        'label' => $sensor['name'], 
        'borderColor' => $color, 
        'backgroundColor' => $color, 
        'data' => $source
    );
}

function get_api_measurements($db, $column, $lag)
{
    $source = array();
    $levels = $db->query(
        "SELECT DISTINCT reference_time, ". $column . " AS m " .
        "FROM openweathermap ".
        "WHERE reference_time > (SELECT DATETIME('now', '".$lag."'))" .";"
    );
    
    while ($level = $levels->fetchArray()) {
        array_push(
            $source, 
            array("x" => $level["reference_time"], 
                  "y" => floatval($level["m"]))
        );
    }
    
    $color = "#4ea832";
    return array(
        'label' => "OWM ". $column, 
        'borderColor' => $color, 
        'backgroundColor' => $color, 
        'data' => $source
    );
}

function daylight_graph() {
    $sunrise = array();
    $sunset = array();
    global $DB_FILENAME;
    $db = new SQLite3($DB_FILENAME);
    
    $levels = $db->query(
        "SELECT DATE(sunrise_time) AS day, sunrise_time, sunset_time " .
        "FROM openweathermap ".
        "GROUP BY sunrise_time, sunset_time;"
    );
    
    while ($level = $levels->fetchArray()) {
        array_push($sunrise, array("x" => $level["day"], "y" => $level["sunrise_time"])); 
        array_push($sunset, array("x" => $level["day"], "y" => $level["sunset_time"])); 
    }
    $db->close();
    
    return array(
        array(
            'label' => "Východ slnka", 
            'backgroundColor' => "#3242a8", 
            'data' => $sunrise
        ),
        array(
            'label' => "Západ slnka", 
            'backgroundColor' => "#e8cb0e", 
            'data' => $sunset
        )
    );
}

function generateGraph($api_field, $column, $column_expr, $join) {
    global $DB_FILENAME;
    $LAG = "-5 day";
    $db = new SQLite3($DB_FILENAME);
    
    $measure = array();
    if ($column !== '') {
        $sensors = get_sensors($db, $column, $LAG);
        while ($sensor = $sensors->fetchArray()) {
            array_push($measure, get_measurements_on_sensor($db, $sensor, $column_expr, $join, $LAG));
        }
    }
    
    if ($api_field !== '')
        array_push($measure, get_api_measurements($db, $api_field, $LAG));
    $db->close();

    return $measure;
}
?>
<html>
    <head>
        <title>Počasie</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="design.css" />
    </head>
    <body class="wrapper">
        <div class="title">
            <h1>Meteo senzorové údaje</h1>
        </div>
        <div class="main">
            <h2>Bratislava </h2>
            <div><canvas id="temperature" width="500rem" height="160rem"></canvas></div>
            <div><canvas id="light" width="500rem" height="100rem"></canvas></div>
            <div><canvas id="pressure" width="500rem" height="100rem"></canvas></div>
            <div><canvas id="humidity" width="500rem" height="100rem"></canvas></div>
            <div><canvas id="daylight" width="500rem" height="100rem"></canvas></div>
            <!-- Chýba: Graf diferencie a autokorelácie teploty a korelácie teplôt pearsonov koef -->
            <h2>Slovenská technická univerzita &middot; Fakulta informatiky a informačných technológií &middot; Miroslav Hájek</h2>
        </div>
    </body>
    <script type="text/javascript" src="chart.js"></script>
    <script type="text/javascript" src="chartjs-adapter-date-fns.bundle.min.js"></script>
    <script type="text/javascript">
        <?php echo 'const t = '.json_encode(generateGraph('temperature', 't_celsius', 't_celsius', '')).';'; ?>
        <?php echo 'const p = '.json_encode(generateGraph('pressure', 'p_mslp_pa', 'CAST(p_mslp_pa AS REAL) / 100', '')).';'; ?>
        <?php echo 'const h = '.json_encode(generateGraph('humidity', 'rel_humidity', 'rel_humidity', '')).';'; ?>
        <?php echo 'const lx = '.json_encode(
            generateGraph('clouds', 'light_analog',
                '((light_analog - offset) / diff) * 100', 
                'JOIN ( '.
                '   SELECT sensor_id, '.
                '       MIN(light_analog) AS offset, '.
                '       CAST(ABS(MAX(light_analog) - MIN(light_analog)) AS REAL) AS diff '. // Normalize 0..100
                '   FROM measurements '.
                '   GROUP BY sensor_id '.
                ') x ON x.sensor_id = mx.sensor_id')
        ).';'; ?>
        <?php echo 'const s = '.json_encode(daylight_graph()).';'; ?>
    

        const tooltip = {
            tooltipFormat: 'dd.MM.yyyy HH:mm',
            unit: 'hour',
            displayFormats: {
                hour: 'HH:mm'
            }
        };
        const scales = {
            x: {
                type: 'time',
                time: tooltip
            }
        };        

        var tChart = new Chart(document.getElementById('temperature'), {
            type: 'line',
            data: {datasets: t},
            options: {
                plugins: {title: {display: true, text: 'Teplota [°C]'}},
                scales: scales
            }
        });
        var lxChart = new Chart(document.getElementById('light'), {
            type: 'line',
            data: {datasets: lx},
            options: {
                plugins: {title: {display: true, text: 'Osvetlenie [% rel.]'}},
                scales: scales
            }
        });
        var pChart = new Chart(document.getElementById('pressure'), {
            type: 'line',
            data: {datasets: p},
            options: {
                plugins: {title: {display: true, text: 'Tlak [hPa]'}},
                scales: scales
            }
        });
        var hChart = new Chart(document.getElementById('humidity'), {
            type: 'line',
            data: {datasets: h},
            options: {
                plugins: {title: {display: true, text: 'Relatívna vlhkosť [%]'}},
                scales: scales
            }
        });
        var sChart = new Chart(document.getElementById('daylight'), {
            type: 'bar',
            data: {datasets: s},
            options: {
                plugins: {title: {display: true, text: 'Slnečný svit [hod.]'}},
                scales: {
                    x: {stacked: true,
                        type: 'time',
                        time: {
                            unit: 'day',
                            displayFormats: {
                                day: 'dd.MM'
                            }
                        }
                    },
                    y: {
                        type: 'time',
                        stacked: true,
                        time: tooltip
                    }
                }
            }
        });
    </script>
</html>
