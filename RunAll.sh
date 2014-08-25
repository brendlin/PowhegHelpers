#!/bin/bash

python MinloVariations.py --vars all --eigen --scale --pdf --flat --process ggh
python MinloVariations.py --vars all --eigen --scale --pdf --flat --process vbf
python MinloVariations.py --vars all                       --flat --process wh
python MinloVariations.py --vars all                       --flat --process zh
python MinloVariations.py --vars all                       --flat --process tth

python MinloVariations.py --vars all --eigen --scale --pdf --flat --process hj

print 'done motherfucka!'