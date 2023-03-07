<?php

$servername = "localhost";


$dbname = "Test";

$username = "debian-sys-maint";

$password = "5u0Gzk06Ezn1anzh";

$_
$api_key_value = "jonasjonas";

$api_key= $sensor = $sensor2 = $location = $location2 = $value1 = $value2 = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $api_key = test_input($_POST["api_key"]);
    if($api_key == $api_key_value) {
        $sensor = test_input($_POST["sensor"]);
        $sensor2 = test_input($_POST["sensor2"]);
        $location = test_input($_POST["location"]);
        $location2 = test_input($_POST["location2"]);
        $value1 = test_input($_POST["value1"]);
        $value2 = test_input($_POST["value2"]);
        
        // Laver SQL connection via SQL
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        $sql = "INSERT INTO SensorData (sensor, sensor2, location, location2, value1, value2)
        VALUES ('" . $sensor . "','" . $sensor2 . "','" . $location . "','" . $location2 . "', '" . $value1 . "', '" . $value2 . "')";
        
        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } 
        else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
