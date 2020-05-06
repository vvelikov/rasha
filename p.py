#!/usr/bin/env python3
from datetime import datetime
import time

file = "/mnt1/Tom/Tom & Jerry - Back to School!.mp4"
now = str(datetime.now().strftime("%H:%M"))
counter = 3
f = open( 'x.log', 'a' )
x = file[5:]
print(x)
y = x[:-4]
y = y.replace('/',' - ')
print(y)
if y.startswith('Conni'):
    y = y[8:]
elif y.startswith(' -'):
    y = y[9:]
print(y)
f.write( "%s" % now + ' ' + "# %s" % round(counter,1) + ' ' + y + '\n' )
f.close()
