<html>
  <head>
    <title>RASHA</title>
 </head>
  <body>
    <div align="center">
<!--    <h3>Rasha's Temperature Monitor</h3> -->
<?php
    $myfilename=("/tmp/weather.txt");
    $mytemp=("/tmp/temp.out");
    $mylog=("/tmp/all.log");
    $myradio=("/tmp/radio.log");
    $mymasha=("/tmp/masha.log");
    $mybarba=("/tmp/barba.log");

    if(isset($_POST['playm'])){
     $output = shell_exec('/home/pi/scripts/playm.sh');
    }
    if(isset($_POST['stopm'])){
     $output = shell_exec('/home/pi/scripts/stopm.sh');
    }
    if(isset($_POST['nextm'])){
     $output = shell_exec('/home/pi/scripts/nextm.sh');
    }
    if(isset($_POST['playb'])){
     $output = shell_exec('/home/pi/scripts/playb.sh');
    }
    if(isset($_POST['stopb'])){
     $output = shell_exec('/home/pi/scripts/stopb.sh');
    }
    if(isset($_POST['nextb'])){
     $output = shell_exec('/home/pi/scripts/nextb.sh');
    }

    if(file_exists($mytemp)){
      echo "<br></br>";
      echo "<div><font size='3'>Munich, Germany: <b>".file_get_contents($myfilename)."</div></b>";
      echo "<div><font size='3'><b> ".file_get_contents($mytemp);
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
echo "<div><font size='2'><b>Masha Log:</div></b>";
if(file_exists($mymasha)){
  echo "<div><font size='2'>";
  echo nl2br( file_get_contents($mymasha));
  echo "</div></font>";
}
?>
  <br></br>
    <form  method="post">
    <input type="submit" name="playm" value="play">
    <input type="submit" name="stopm" value="stop" >
    <input type="submit" name="nextm" value="next" >
    </form>
<?php
echo "<div><font size='2'><b>Barba Log:</div></b>";
if(file_exists($mybarba)){
  echo "<div><font size='2'>";
  echo nl2br( file_get_contents($mybarba));
  echo "</div></font>";
}
?>
  <br></br>
    <form  method="post">
    <input type="submit" name="playb" value="play">
    <input type="submit" name="stopb" value="stop" >
    <input type="submit" name="nextb" value="next" >
    </form>
<?php
if(file_exists($myradio)){
  echo "<div><font size='2'>";
  echo nl2br( file_get_contents($myradio));
  echo "</div></font>";
}
?>
  <br></br>
<?php
if(file_exists($mylog)){
  echo "<div><font size='2'>";
  echo nl2br( file_get_contents($mylog));
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
