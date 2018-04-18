#!/usr/bin/perl
#
# CGI script to create image using RRD graph 
use CGI qw(:all);
use RRDs;
use strict;

# path to database
my $rrd='/var/www/html/tmp/Temp.rrd';

# size
my $width=700;
my $height=350;

# label

# read and check query params
my $query=new CGI;
my $type=$query->param('type');
$type='day' unless $type =~ /day|week|month|year/;

# write image into temp file
my $tmpfile="/tmp/graphx_$$.png";
my @opts=("-v", "°C",
"--slope-mode",
"-v Temperature °C / Humidity %",
"-w", $width,
"--full-size-mode",
"-h", $height,
"-s", "now - 1 $type",
"-e", "now",
"--y-grid", "5:1",
"--right-axis", "1:0",
"-P",
"-D");
RRDs::graph($tmpfile,
  @opts,
  "DEF:tempIN=$rrd:tempIN:AVERAGE",
  "DEF:tempOUT=$rrd:tempOUT:AVERAGE",
  "DEF:humidity=$rrd:humidity:AVERAGE",
  "CDEF:AAA=tempOUT,31,GE,tempOUT,0,IF",
  "CDEF:AA=tempOUT,29,GE,tempOUT,30,LT,tempOUT,30,IF,0,IF",
  "CDEF:AB=tempOUT,28,GE,tempOUT,29,LT,tempOUT,29,IF,0,IF",
  "CDEF:AC=tempOUT,27,GE,tempOUT,28,LT,tempOUT,28,IF,0,IF",
  "CDEF:A=tempOUT,26,GE,tempOUT,27,LT,tempOUT,27,IF,0,IF",
  "CDEF:B=tempOUT,25,GE,tempOUT,26,LT,tempOUT,26,IF,0,IF",
  "CDEF:D=tempOUT,23,GE,tempOUT,24,LT,tempOUT,24,IF,0,IF",
  "CDEF:C=tempOUT,24,GE,tempOUT,0,IF",
  "CDEF:E=tempOUT,22,GE,tempOUT,23,LT,tempOUT,23,IF,0,IF",
  "CDEF:F=tempOUT,21,GE,tempOUT,22,LT,tempOUT,22,IF,0,IF",
  "CDEF:G=tempOUT,20,GE,tempOUT,21,LT,tempOUT,21,IF,0,IF",
  "CDEF:H=tempOUT,19,GE,tempOUT,20,LT,tempOUT,20,IF,0,IF",
  "CDEF:I=tempOUT,18,GE,tempOUT,19,LT,tempOUT,19,IF,0,IF",
  "CDEF:J=tempOUT,17,GE,tempOUT,18,LT,tempOUT,18,IF,0,IF",
  "CDEF:K=tempOUT,16,GE,tempOUT,17,LT,tempOUT,17,IF,0,IF",
  "CDEF:L=tempOUT,11,GE,tempOUT,16,LT,tempOUT,16,IF,0,IF",
  "CDEF:M=tempOUT,10,GE,tempOUT,12,LT,tempOUT,11,IF,0,IF",
  "CDEF:N=tempOUT,9,GE,tempOUT,10,LT,tempOUT,10,IF,0,IF",
  "CDEF:O=tempOUT,8,GE,tempOUT,9,LT,tempOUT,9,IF,0,IF",
  "CDEF:P=tempOUT,7,GE,tempOUT,8,LT,tempOUT,8,IF,0,IF",
  "CDEF:Q=tempOUT,6,GE,tempOUT,7,LT,tempOUT,7,IF,0,IF",
  "CDEF:R=tempOUT,5,GE,tempOUT,6,LT,tempOUT,6,IF,0,IF",
  "CDEF:S=tempOUT,4,GE,tempOUT,5,LT,tempOUT,5,IF,0,IF",
  "CDEF:T=tempOUT,3,GE,tempOUT,4,LT,tempOUT,4,IF,0,IF",
  "CDEF:U=tempOUT,3,LT,tempOUT,5,IF",
  "CDEF:X=tempOUT",
  "VDEF:V=tempOUT,AVERAGE",
  "LINE1:tempOUT:",
  "AREA:AAA#810541:",
  "AREA:AA#7E3517:",
  "AREA:AB#8C001A:",
  "AREA:AC#990012:",
  "AREA:A#C11B17:",
  "AREA:B#E42217:",
  "AREA:D#FF3300:",
  "AREA:C#FF0000:",
  "AREA:E#FF6600:",
  "AREA:F#FF9900:",
  "AREA:G#FFCC00:",
  "AREA:H#CCFF00:",
  "AREA:I#99FF00:",
  "AREA:J#66FF00:",
  "AREA:K#33FF00:",
  "AREA:L#00FF00:",
  "AREA:M#00FF33:",
  "AREA:N#00FF66:",
  "AREA:O#00FF99:",
  "AREA:P#00FFCC:",
  "AREA:Q#00CCFF:",
  "AREA:R#0099FF:",
  "AREA:S#0066FF:",
  "AREA:T#0033FF:",
  "AREA:U#0000FF:",
  "COMMENT: \\n",
  "COMMENT:\\t",
  "COMMENT:\\t",
  "COMMENT:\\t",
  "LINE1:tempOUT#9B1CC8:",
  "COMMENT: \\n",
  "VDEF:tempIN_avg=tempIN,AVERAGE",
  "VDEF:tempIN_cur=tempIN,LAST",
  "VDEF:tempIN_min=tempIN,MINIMUM",
  "VDEF:tempIN_max=tempIN,MAXIMUM",
  "VDEF:tempOUT_avg=tempOUT,AVERAGE",
  "VDEF:tempOUT_cur=tempOUT,LAST",
  "VDEF:tempOUT_min=tempOUT,MINIMUM",
  "VDEF:tempOUT_max=tempOUT,MAXIMUM",
  "VDEF:humidity_avg=humidity,AVERAGE",
  "VDEF:humidity_cur=humidity,LAST",
  "VDEF:humidity_min=humidity,MINIMUM",
  "VDEF:humidity_max=humidity,MAXIMUM",
  "COMMENT:\\t\\t\\t\\t   Current\\t\\t    Avg\\t\\t   Min\\t\\t  Max\\l", 
  "COMMENT:\\t",
  "HRULE:60#FF0000",
  "LINE1:tempOUT#0000FF:outside\\t",
  "GPRINT:tempOUT_cur:%6.1lf °C \\t",
  "GPRINT:tempOUT_avg:%6.1lf °C \\t",
  "GPRINT:tempOUT_min:%6.1lf °C \\t",
  "GPRINT:tempOUT_max:%6.1lf °C \\l",
  "COMMENT:\\t",
  "LINE2:tempIN#660099:inside\\t",
  "GPRINT:tempIN_cur:%6.1lf °C \\t",
  "GPRINT:tempIN_avg:%6.1lf °C \\t",
  "GPRINT:tempIN_min:%6.1lf °C \\t",
  "GPRINT:tempIN_max:%6.1lf °C \\l",
  "COMMENT:\\t",
  "LINE2:humidity#41924B:humidity\\t",
  "GPRINT:humidity_cur:%6.1lf  %% \\t",
  "GPRINT:humidity_avg:%6.1lf  %% \\t",
  "GPRINT:humidity_min:%6.1lf  %% \\t",
  "GPRINT:humidity_max:%6.1lf  %% \\l",
  "COMMENT:\\t", 
);
# check error
my $err=RRDs::error;
die "$err\n" if $err;

# feed tmpfile to stdout
open(IMG, $tmpfile) or die "can't open $tmpfile\n";
print header(-type=>'image/png', -expires=>'+1m');
print <IMG>;
close IMG;
unlink $tmpfile;