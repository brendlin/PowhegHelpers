#!/usr/bin/env python

import os, stat

all = open ("powheg_all.sh", "w")
all.write("#!/bin/bash\n\n")

condor = open("powheg/submit/condor_powheg.sh","w")
condor.write("#!/bin/bash\n\n")

swdir = os.getenv('swdir')

condorTemplate = \
"""universe   = vanilla
Executable = %s.sh
Initialdir = %s/powheg/submit
getenv     = True
output     = %s/powheg/log/%s.out
error      = %s/powheg/log/%s.err
log        = %s/powheg/log/%s.log
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
cd %s/powheg/out/%s
%s/POWHEG-BOX/%s/pwhg_main <<< %d

echo done.
"""

def WriteVariations(variations,nfiles,process) :
    for v in variations :
        for i in range(1,nfiles+1) :
            tag = '%s_%04d'%(v,i)
            vshort = v.replace('0.5','0')
            submit_name = "powheg/submit/%s.sh" % tag
            with open(submit_name, "w") as sub:
                ##                          asetup,cd          v,exec ,VBF_H, seed
                sub.write(submitTemplate % (swdir ,os.getcwd(),v,swdir,process, i   ))
            st = os.stat(submit_name).st_mode
            os.chmod(submit_name, st | stat.S_IEXEC)
            doEmail = '-N -u \"kurt.brendlinger@gmail.com\"' if (i == nfiles) else ''
            all.write("bsub -q 8nh -J %s -o powheg/log/%s %s < %s\n" % (tag,tag,doEmail,submit_name))

            condor_name = "powheg/submit/%s.job" % tag
            with open(condor_name, "w") as sub:
                sub.write(condorTemplate % (tag,os.getcwd(),os.getcwd(),tag,os.getcwd(),tag,os.getcwd(),tag))
            st = os.stat(condor_name).st_mode
            os.chmod(condor_name, st | stat.S_IEXEC)
            condor.write("condor_submit %s.job\n" % (tag))

# ## nominal - ggH
h_variations = ['ggH_0.5_0.5','ggH_0.5_1','ggH_1_0.5','ggH_1_1','ggH_1_2','ggH_2_1','ggH_2_2']
h_nfiles = 20
h_process = 'gg_H_quark-mass-effects'
WriteVariations(h_variations,h_nfiles,h_process)

# ## hfact - ggH
h_variations = ['ggH_hfact_0.5_0.5','ggH_hfact_0.5_1','ggH_hfact_1_0.5','ggH_hfact_1_1','ggH_hfact_1_2','ggH_hfact_2_1','ggH_hfact_2_2']
h_nfiles = 20
h_process = 'gg_H_quark-mass-effects'
WriteVariations(h_variations,h_nfiles,h_process)

# ## VBF
h_variations = ['VBFH125_0.5_0.5','VBFH125_0.5_1','VBFH125_1_0.5','VBFH125_1_1','VBFH125_1_2','VBFH125_2_1','VBFH125_2_2']
h_nfiles = 12
h_process = 'VBF_H'
WriteVariations(h_variations,h_nfiles,h_process)

## HJ
h_variations = ['minlo_HJ_mH125_0.5_0.5','minlo_HJ_mH125_0.5_1','minlo_HJ_mH125_1_0.5','minlo_HJ_mH125_1_1','minlo_HJ_mH125_1_2','minlo_HJ_mH125_2_1','minlo_HJ_mH125_2_2']
h_nfiles = 20
h_process = 'HJ'
WriteVariations(h_variations,h_nfiles,h_process)

# ## HJJ
# hjj_variations = ['minlo_HJJ_mH125_0.5_0.5','minlo_HJJ_mH125_0.5_1','minlo_HJJ_mH125_1_0.5','minlo_HJJ_mH125_1_1','minlo_HJJ_mH125_1_2','minlo_HJJ_mH125_2_1','minlo_HJJ_mH125_2_2']
# hjj_process = 'minlo_HJJ_mH125_kurt'
# hjj_nfiles = 10
# WriteVariations(hjj_variations,hjj_process,hjj_nfiles)

all.close()
st = os.stat('powheg_all.sh').st_mode
os.chmod('powheg_all.sh',st | stat.S_IEXEC)
