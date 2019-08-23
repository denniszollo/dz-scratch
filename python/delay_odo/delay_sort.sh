#!/bin/bash
# first sbp2jsonify file
JSON_OUT="_1.sbp.json"
DELAY_OUT="_1.delay_odo.sbp.json"
SORT_OUT="_1.delay_odo.sort.sbp.json"
cat $1 | sbp2json > $JSON_OUT
# next delay the odo
python2 /Users/dzollo/source/dz-scratch/python/delay_odo/delay_odo.py $JSON_OUT -750 $DELAY_OUT
# next sort
python2 /Users/dzollo/source/dz-scratch/python/timesortsbp/sort_by_tow.py $DELAY_OUT 
cat $DELAY_OUT | json2sbp > $1+".delay.sort.sbp"
