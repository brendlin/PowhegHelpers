#!/usr/bin/env python

import os
from ProcessManager import kBatchLocal

batch = kBatchLocal()

#a = list('pwgevents-%04d.lhe'%(x) for x in range(1,21))

for i in os.listdir('.') :
    batch.addJob(['python','modify_les_houches.py','--file',i])
batch.wait()

print 'done.'
