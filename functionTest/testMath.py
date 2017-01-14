#!/usr/bin/python

import random
import math

for i in range(1,10000000,1):
    ba = math.floor(random.random() * 10000000)
    if(ba < 100 and ba > 98):
        print 'The value ', ba, 'fit this scale.'
    pass