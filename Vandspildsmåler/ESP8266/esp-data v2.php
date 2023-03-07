<!DOCTYPE html>
<html><body>
<?php

$servername = "localhost";


$dbname = "Test";

$username = "debian-sys-maint";

$password = "5u0Gzk06Ezn1anzh";

// Laver connection til SQL via SQLI
$conn = new mysqli($servername, $username, $password, $dbname);
// Tjekker connection
if ($conn->connect_error) {
    die("Connection interrupted: " . $conn->connect_error);
} 
// select returnerer valgte data records fra vores table i databasen
$sql = "SELECT id, sensor, location, value1, value2, tidspunkt FROM SensorData ORDER BY id DESC";

echo '<table cellspacing="5" cellpadding="5">
      <tr> 
        <td>ID</td> 
        <td>Sensor</td> 
        <td>Location</td> 
        <td>Value 1</td> 
        <td>Value 2</td>
        <td>Timestamp</td> 
      </tr>';
      
 //indsætter vores SELECT values i vores bestemte database rows
if ($result = $conn->query($sql)) {
    while ($row = $result->fetch_assoc()) {
        $row_id = $row["id"];
        $row_sensor = $row["sensor"];
        $row_location = $row["location"];
        $row_value1 = $row["value1"];
        $row_value2 = $row["value2"];  
        $row_tidspunkt = $row["tidspunkt"];
        $row_tidspunkt = date("Y-m-d H:i:s", strtotime("$row_tidspunkt + 1 hours"));
      
        echo '<tr> 
                <td>' . $row_id . '</td> 
                <td>' . $row_sensor . '</td> 
                <td>' . $row_location . '</td> 
                <td>' . $row_value1 . '</td> 
                <td>' . $row_value2 . '</td>
                <td>' . $row_tidspunkt . '</td> 
              </tr>';
    }
    $result->free();
}

$conn->close();
?> 
</table>
</body>
</html>
