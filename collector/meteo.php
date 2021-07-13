<?php

if (!empty($_POST)) {
    $db = new SQLite3('/home/pi/weather.db');
    $q = $db->prepare(
        'INSERT INTO measurements(sensor_id, t_celsius, light_analog, p_mslp_pa, rel_humidity) ' .
        'VALUES (:id, :t, :lx, :p, :h);'
    );
    $q->bindValue(':id', $_POST['id'] ?? null);
    $q->bindValue(':t', $_POST['t'] ?? null);
    $q->bindValue(':lx', $_POST['lx'] ?? null);
    $q->bindValue(':p', $_POST['p'] ?? null);
    $q->bindValue(':h', $_POST['h'] ?? null);
    $q->execute();
    $db->close();
}
?>
