<html>
  <head>
    <title>RASHA</title>
	<link rel="icon" href="favicon.ico">
 </head>
  <body>
    <div align="center">
<!--    <h3>Rasha's Temperature Monitor</h3> -->
<?php
    $mytemp=("/logs/temp.log");
    $weather=shell_exec("cat /logs/temp.log | tail -n 1");
    $tempIN=shell_exec("cat /logs/temp.log | head -n 1");
    $tempOUT=shell_exec("cat /logs/temp.log | tail -n 2 | head -n 1");
    $mylog=("/logs/all.log");
    $myradio=("/logs/radio.log");
    $mytitle=shell_exec("mpc current -f [%title%] | tr -d '\n'");

    if(file_exists($mytemp)){
      echo "<br></br>";
      echo "<div><font size='3'>Munich, Germany: <b>$weather</div></b>";
      echo "<div><font size='3'>Outside: <b>$tempOUT</b>";
      echo "&deg;C";
      echo "</div></b>";
      echo "<div><font size='3'>Inside: <b>$tempIN</b>";
      echo "&deg;C";
      echo "</div></b>";
    }
?>
<p></p>
<iframe marginwidth="0" marginheight="0" frameborder="0" width="700" height="350" name="graph">
</iframe>
<form action="graph.pl" method="get" style="width: 275px" target="graph">
<p></p>
  <fieldset>
    <legend align="center">Time Period</legend>
  <input type="radio" name="type" value="day" checked="checked"/>Day
  <input type="radio" name="type" value="week"/>Week
  <input type="radio" name="type" value="month"/>Month
  <input type="radio" name="type" value="year"/>Year
  </fieldset>
  <p></p>
  <input type="submit" value="Show" />
</form>
<?php
    if (!empty($mytitle)) {
	  echo "<div><b><font size='3'>Current song: </div></b>"; 
	  echo "<pre>$mytitle</pre>";
    }
?>
 <br></br>  
<?php
if(file_exists($myradio)){
  echo "<div><font size='2'>";
  echo nl2br( file_get_contents($myradio));
  echo "</div></font>";
}
?>
</form>
  <br></br>
<form name="input" action="./cgi-bin/reboot.py" method="get">
<input type="submit" value="Reboot">
  <br></br>
</div>
  </body>
</html>
