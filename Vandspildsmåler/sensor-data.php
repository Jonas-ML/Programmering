<!DOCTYPE html>
<html><body>
<?php

// login til DB
$serverName = "localhost";
$dbName = "Test";
$userName = "debian-sys-maint";
$passWord = "5u0Gzk06Ezn1anzh";

//Connection til database
$connection = mysqli_connect($serverName, $userName, $passWord, $dbName);

//klargører en SQL SELECT query, vi siger her hvilke rows i vores database den skal bruge og vi indexerer efter id descending - nyest måling vises først
$query = "SELECT id, sensor, sensor2, location, location2, value1, value2, tidspunkt FROM SensorData ORDER BY id DESC"; 

//echoer vores keys, eller identifieres i toppen af siden
echo '<table cellspacing="5" cellpadding="8">
	<tr>
		<th>ID</th>
		<th>Sensor1</th>
		<th>Sensor2</th>
		<th>Lokation1</th>
		<th>Lokation2</th>
		<th>Temp1</th>
		<th>Temp2</th>
		<th>Tidspunkt</th>
	</tr>';

// pakker
$result = mysqli_query($connection, $query);

// num rows tjekker om der er flere end 0 rows returneret. 
//Hvorefter fetch_assoc(), putter resultaterne ind i et associative array.
//dette array looper vi igennem og pakker dataen ind i disse row variables
//et associative array, er et array der holder key value pairs, istedet for at man har en liste indexeret i 1,2,3 osv. kan man have en key som sensor og en tilhørende value dertil
if (mysqli_num_rows($result) > 0) {

	while($row = $result ->fetch_assoc()) {
		$row_id = $row["id"];
        	$row_sensor = $row["sensor"];
        	$row_sensor2 = $row["sensor2"];
        	$row_location = $row["location"];
        	$row_location2 = $row["location2"];
        	$row_value1 = $row["value1"];
        	$row_value2 = $row["value2"];
        	$row_tidspunkt = $row["tidspunkt"];
        	$row_tidspunkt = date("Y-m-d H:i:s", strtotime("$row_tidspunkt + 1 hours"));

// echoer vores data til vores table
		echo '<tr>
			<td>' . $row_id . '</td>
			<td>' . $row_sensor . '</td>
			<td>' . $row_sensor2 . '</td>
			<td>' . $row_location . '</td>
			<td>' . $row_location2 . '</td>
			<td>' . $row_value1 . '</td>
			<td>' . $row_value2 . '</td>
			<td>' . $row_tidspunkt . '</td>
		</tr>';
	}
}
$connection->close();

// tr definere et row i et table mens td definere en celle i table


?>
</table>
</body>
</html>
