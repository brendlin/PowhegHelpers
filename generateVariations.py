#!/usr/bin/env python

import os, stat

## for i in range(cut_flow.GetNbinsX()) :
##     print '%s %2.4f'%(cut_flow.GetXaxis().GetBinLabel(i+2).ljust(20),cut_flow.GetBinContent(i+2)/float(cut_flow.GetBinContent(i+1)))

all = open ("all.sh", "w")
all.write("#!/bin/bash\n\n")

condor = open("var/submit/condor.sh","w")
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
./zz_powheg_hgg.exe pythia_settings/zz_nominal.cmnd /disk/userdata00/atlas_data2/bijanh/HZZRun2/LHE/%s/%s/PowhegOTF._%04d.events -1 %s/var/out/%s.root


echo done.
"""

def WriteVariations(variations,process,nfiles) :
    for v in variations :
        for i in range(1,nfiles+1) :
            tag = '%s_%04d'%(v,i)
            submit_name = "var/submit/%s.sh" % tag
            with open(submit_name, "w") as sub:
                sub.write(submitTemplate % (os.getcwd(),process,v,i,os.getcwd(),tag))
            st = os.stat(submit_name).st_mode
            os.chmod(submit_name, st | stat.S_IEXEC)
            doEmail = '-N -u \"bijanh@sas.upenn.edu\"' if (i == nfiles) else ''
            all.write("bsub -q 8nh -J %s -o var/log/%s %s < %s\n" % (tag,tag,doEmail,submit_name))

            condor_name = "var/submit/%s.job" % tag
            with open(condor_name, "w") as sub:
                sub.write(condorTemplate % (tag,os.getcwd(),os.getcwd(),tag,os.getcwd(),tag,os.getcwd(),tag))
            st = os.stat(condor_name).st_mode
            os.chmod(condor_name, st | stat.S_IEXEC)
            condor.write("condor_submit %s.job\n" % (tag))

## nominal
h_variations = ['ggH_1_1']
h_process = 'ggH8TeV'
h_nfiles = 500
WriteVariations(h_variations,h_process,h_nfiles)

h_variations = ['VBF_1_1']
h_process = 'VBF8TeV'
h_nfiles = 2000
WriteVariations(h_variations,h_process,h_nfiles)
'''
## hfact
h_variations = ['ggH_hfact_0.5_0.5','ggH_hfact_0.5_1','ggH_hfact_1_0.5','ggH_hfact_1_1','ggH_hfact_1_2','ggH_hfact_2_1','ggH_hfact_2_2']
h_process = 'ggH_hfact'
h_nfiles = 20
WriteVariations(h_variations,h_process,h_nfiles)

## VBF
h_variations = ['VBFH125_0.5_0.5','VBFH125_0.5_1','VBFH125_1_0.5','VBFH125_1_1','VBFH125_1_2','VBFH125_2_1','VBFH125_2_2']
h_process = 'VBFH125'
h_nfiles = 12
WriteVariations(h_variations,h_process,h_nfiles)

## HJ
hj_variations = ['minlo_HJ_mH125_0.5_0.5','minlo_HJ_mH125_0.5_1','minlo_HJ_mH125_1_0.5','minlo_HJ_mH125_1_1','minlo_HJ_mH125_1_2','minlo_HJ_mH125_2_1','minlo_HJ_mH125_2_2']
hj_process = 'minlo_HJ_mH125'
hj_nfiles = 20
WriteVariations(hj_variations,hj_process,hj_nfiles)

## HJJ
hjj_variations = ['minlo_HJJ_mH125_0.5_0.5','minlo_HJJ_mH125_0.5_1','minlo_HJJ_mH125_1_0.5','minlo_HJJ_mH125_1_1','minlo_HJJ_mH125_1_2','minlo_HJJ_mH125_2_1','minlo_HJJ_mH125_2_2']
hjj_process = 'minlo_HJJ_mH125'
hjj_nfiles = 10
WriteVariations(hjj_variations,hjj_process,hjj_nfiles)
'''


all.close()
st = os.stat('all.sh').st_mode
os.chmod('all.sh',st | stat.S_IEXEC)
