


<?php
      
      define('DB_HOST', 'localhost');
define('DB_USERNAME', 'ubuntu');
define('DB_PASSWORD', 'password');
define('DB_NAME', 'iot');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
  die("Connection failed: " . $mysqli->error);
}

//query to get data from the table
$query = ("SELECT DATE_FORMAT(record, '%d-%m-%Y %H') AS ts, COUNT(*) AS passed FROM counter GROUP BY ts");
$last_entry = ("SELECT record FROM counter ORDER BY id DESC LIMIT 1"); //show last entry
//execute query
$busiest = ("SELECT DATE_FORMAT(record, '%d-%m-%Y %H ') AS ts, COUNT(*) AS passed FROM counter GROUP BY ts ORDER BY passed DESC LIMIT 1");
//Additional queries.
//show total count for the day  SELECT DATE_FORMAT(record, '%d-%m-%Y') AS ts, COUNT(*) FROM counter WHERE record >= '2019-10-09' AND   record <  '2019-10-09' + INTERVAL 1 DAY GROUP BY DATE_FORMAT(record, '%d-%m-%Y');
//show count by day and hours SELECT DATE_FORMAT(record, '%d-%m-%Y %H') AS ts, COUNT(*) FROM counter WHERE record >= '2019-10-09' AND   record <  '2019-10-09' + INTERVAL 1 DAY GROUP BY DATE_FORMAT(record, '%d-%m-%Y %H');
$busiest5 = ("SELECT DATE_FORMAT(record, '%d-%m-%Y %H ') AS ts, COUNT(*) AS passed FROM counter GROUP BY ts ORDER BY passed DESC LIMIT 5");
$group =("SELECT 
EXTRACT(YEAR FROM record) V_YEAR,
EXTRACT(MONTH FROM record) V_MONTH,
EXTRACT(WEEK FROM record) V_WEEK,
COUNT(*)
FROM counter
GROUP BY
EXTRACT(YEAR FROM record) ,
EXTRACT(MONTH FROM record) ,
EXTRACT(WEEK FROM record) ");
$Month =("SELECT 
EXTRACT(YEAR FROM record) V_YEAR,
EXTRACT(MONTH FROM record) V_MONTH,

COUNT(*)
FROM counter
GROUP BY
EXTRACT(YEAR FROM record) ,
EXTRACT(MONTH FROM record) ");



$result = mysqli_query($mysqli, $query); 
$hour_query = mysqli_query($mysqli, $last_entry) ;
$busy_query = mysqli_query($mysqli, $busiest);
$busy5_query = mysqli_query($mysqli, $busiest5);
$groupresult = mysqli_query($mysqli, $group); 
$GroupMonth = mysqli_query($mysqli, $Month); 





        ?>

 <!DOCTYPE html>
<html>
<head> 
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>MySQL graphics</title>
    <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);
      google.charts.setOnLoadCallback(drawWeekChart);
      google.charts.setOnLoadCallback(drawgroup);
      google.charts.setOnLoadCallback(drawMonth);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date/hour', 'Sensor count'],
          <?php  
                          while($row = mysqli_fetch_array($result))  
                          {  
                               echo "['".$row["ts"]."', ".$row["passed"]."],";  
                          }  
                          ?>  
        ]);

        var options = {
          chart: {
            title: 'The chart below represents sensor activtion as a function of time, grouped hourly',
            subtitle: 'Format: Day/Month/Year - Hour',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }

      function drawWeekChart() {

var data = google.visualization.arrayToDataTable([
  ['Date/hour', 'Sensor count'],
  <?php  
                  while($row = mysqli_fetch_array($busy5_query))  
                  {  
                       echo "['".$row["ts"]."', ".$row["passed"]."],";  
                  }  
                  ?>  
]);

var options = {
  chart: {
    title: 'The chart below represents the 5 busiest hours ever recorded',
    subtitle: 'Format: Day/Month/Year - Hour',
  }
};

var chart = new google.charts.Bar(document.getElementById('columnchart_material2'));

chart.draw(data, google.charts.Bar.convertOptions(options));
}

function drawgroup() {
        var data = google.visualization.arrayToDataTable([
          ['Date/hour', 'Sensor count'],
          <?php  
                          while($row = mysqli_fetch_assoc($groupresult))  
                          {  
                               echo "['".$row["V_WEEK"]."', ".$row["COUNT(*)"]."],";  
                          }  
                          ?>  
        ]);

        var options = {
          chart: {
            title: 'The chart below represents sensor activtion grouped weekly',
            subtitle: 'Format: Seonsor count - Number of the week',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material3'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }

      function drawMonth() {
        var data = google.visualization.arrayToDataTable([
          ['Date/hour', 'Sensor count'],
          <?php  
                          while($row = mysqli_fetch_assoc($GroupMonth))  
                          {  
                               echo "['".$row["V_MONTH"]."', ".$row["COUNT(*)"]."],";  
                          }  
                          ?>  
        ]);

        var options = {
          chart: {
            title: 'The chart below represents sensor activtion grouped monthly',
            subtitle: 'Format: Seonsor count - Month number',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material4'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
      }

     


    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" type="text/css" media="screen" href="main.css">
    <script src="main.js"></script>
</head>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="" id="navbarNav">
            <ul id="nav" class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="http://172.20.240.121:8000/">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="http://172.20.240.121:8000/data/">Data analysis basics</a></li>
                    <li class="nav-item"><a class="nav-link" href="http://172.20.240.121/chart1.php">Data Analysis Bar chart</a></li>
            </ul>
        </div>
    </nav>

<body>
<?php
echo ("Last entry record: ");
while($row    = mysqli_fetch_assoc($hour_query))
{
echo $row["record"];
}
echo("<br>");

echo ("Busiest hour: ");

while ( $row = mysqli_fetch_assoc($busy_query) )
{
echo ($row["ts"]);
}

?>
<div id="columnchart_material" style="width: 800px; height: 500px;"></div>
<br>
<br>
<div id="columnchart_material2" style="width: 800px; height: 500px;"></div>
<div id="columnchart_material3" style="width: 800px; height: 500px;"></div>
<div id="columnchart_material4" style="width: 800px; height: 500px;"></div>
<!--
<h1>Live streaming</h1>
<img style="-webkit-user-select: none;margin: auto;" src="http://172.20.248.146:8081/" width="477" height="357">
--!>
</body>
</html>




