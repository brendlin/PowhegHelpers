#!/usr/bin/env python

import os

h_nominals = [#'ggH_1_1'
              #,'ggH_hfact_1_1'
              #,'minlo_HJ_mH125_1_1'
              #,'minlo_HJJ_mH125_1_1'
              'WH_1_1'
              ,'ZH_1_1'
              ,'ttH_1_1'
              ,'VBFH125_1_1'
              ]

h_variations = ['ggH_0.5_0.5','ggH_0.5_1','ggH_1_0.5','ggH_1_1','ggH_1_2','ggH_2_1','ggH_2_2']

hfact_variations = ['ggH_hfact_0.5_0.5','ggH_hfact_0.5_1','ggH_hfact_1_0.5','ggH_hfact_1_1','ggH_hfact_1_2','ggH_hfact_2_1','ggH_hfact_2_2']

hj_variations = ['minlo_HJ_mH125_0.5_0.5','minlo_HJ_mH125_0.5_1','minlo_HJ_mH125_1_0.5','minlo_HJ_mH125_1_1'
                 ,'minlo_HJ_mH125_1_2','minlo_HJ_mH125_2_1','minlo_HJ_mH125_2_2']

hjj_variations = ['minlo_HJJ_mH125_0.5_0.5','minlo_HJJ_mH125_0.5_1','minlo_HJJ_mH125_1_0.5'
                  ,'minlo_HJJ_mH125_1_1'
                  ,'minlo_HJJ_mH125_1_2','minlo_HJJ_mH125_2_1','minlo_HJJ_mH125_2_2']

wh_variations = ['WH_0.5_0.5','WH_0.5_1','WH_1_0.5','WH_1_1','WH_1_2','WH_2_1','WH_2_2']
zh_variations = ['ZH_0.5_0.5','ZH_0.5_1','ZH_1_0.5','ZH_1_1','ZH_1_2','ZH_2_1','ZH_2_2']
tth_variations = ['ttH_0.5_0.5','ttH_0.5_1','ttH_1_0.5','ttH_1_1','ttH_1_2','ttH_2_1','ttH_2_2']

vbf_variations = ['VBFH125_0.5_0.5','VBFH125_0.5_1','VBFH125_1_0.5','VBFH125_1_1','VBFH125_1_2','VBFH125_2_1','VBFH125_2_2']

# for i in h_variations : # +hfact_variations+hj_variations+hjj_variations :
#     print ('hadd -f hadded/%s.root %s_00*.root'%(i,i))
#     #os.system('hadd -f hadded/%s.root %s_00*.root'%(i,i))

# for i in wh_variations+zh_variations+tth_variations :
#     print ('hadd -f hadded/%s.root %s_00*.root'%(i,i))
#     os.system('hadd -f hadded/%s.root %s_00*.root'%(i,i))

# for i in h_nominals :
#     print ('hadd -f hadded/%s.root %s_00*.root'%(i,i))
#     os.system('hadd -f hadded/%s.root %s_00*.root'%(i,i))    

for i in vbf_variations :
    print ('hadd -f hadded/%s.root %s_00*.root'%(i,i))
    os.system('hadd -f hadded/%s.root %s_00*.root'%(i,i))    

print 'done'
