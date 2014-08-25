#!/usr/bin/env python

import os, stat

all = open ("all_pythia.sh", "w")
all.write("#!/bin/bash\n\n")

condor = open("var/submit/condor_pythia.sh","w")
condor.write("#!/bin/bash\n\n")

swdir = os.getenv('swdir')

condorTemplate = \
"""universe   = vanilla
Executable = %s.sh
Initialdir = %s/var/submit
getenv     = True
output     = %s/var/log/%s.out
error      = %s/var/log/%s.err
log        = %s/var/log/%s.log
arguments  = 
should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT

queue
"""

submitTemplate = \
"""#!/bin/bash

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
localSetupROOT --skipConfirm
cd %s
source ASETUP
./zz_powheg_hgg.exe pythia_settings/%s.cmnd GENERATE %d %s/var/out/%s.root


echo done.
"""

def WriteVariations(variations,process,nfiles,nevents) :
    for v in variations :
        for i in range(1,nfiles+1) :
            tag = '%s_%04d'%(v,i)
            submit_name = "var/submit/%s.sh" % tag
            with open(submit_name, "w") as sub:
                sub.write(submitTemplate % (os.getcwd(),process,nevents,os.getcwd(),tag))
                #                           cd %s,cd %s      ,%s.cmnd, %d    ,%s/var/    ,%s.root
            st = os.stat(submit_name).st_mode
            os.chmod(submit_name, st | stat.S_IEXEC)
            doEmail = '-N -u \"kurt.brendlinger@gmail.com\"' if (i == nfiles) else ''
            all.write("bsub -q 8nh -J %s -o var/log/%s %s < %s\n" % (tag,tag,doEmail,submit_name))

            condor_name = "var/submit/%s.job" % tag
            with open(condor_name, "w") as sub:
                sub.write(condorTemplate % (tag,os.getcwd(),os.getcwd(),tag,os.getcwd(),tag,os.getcwd(),tag))
            st = os.stat(condor_name).st_mode
            os.chmod(condor_name, st | stat.S_IEXEC)
            condor.write("condor_submit %s.job\n" % (tag))

## WH
h_variations = ['WH_0.5_0.5','WH_0.5_1','WH_1_0.5','WH_1_1','WH_1_2','WH_2_1','WH_2_2']
h_process = 'WH'
h_nfiles  = 12
h_nevents = 50000
WriteVariations(h_variations,h_process,h_nfiles,h_nevents)

## ZH
h_variations = ['ZH_0.5_0.5','ZH_0.5_1','ZH_1_0.5','ZH_1_1','ZH_1_2','ZH_2_1','ZH_2_2']
h_process = 'ZH'
h_nfiles = 30
h_nevents = 2500
WriteVariations(h_variations,h_process,h_nfiles,h_nevents)

## ttH
h_variations = ['ttH_0.5_0.5','ttH_0.5_1','ttH_1_0.5','ttH_1_1','ttH_1_2','ttH_2_1','ttH_2_2']
h_process = 'ttH'
h_nfiles = 12
h_nevents = 50000
WriteVariations(h_variations,h_process,h_nfiles,h_nevents)

all.close()
st = os.stat('all_pythia.sh').st_mode
os.chmod('all_pythia.sh',st | stat.S_IEXEC)
