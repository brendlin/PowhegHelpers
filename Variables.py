
def GetSampleName(inname) :
    return {'ggH_hfact':'ggH w/hfact'  
            ,'ggH'      :'ggH'          
            ,'WH'       :'WH'           
            ,'ZH'       :'ZH'           
            ,'ttH'      :'ttH'          
            ,'minlo_HJJ':'Minlo HJJ+PY8'
            ,'minlo_HJ'       :'Minlo HJ+PY8' 
            ,'minlo_HJ_mH125' :'Minlo HJ+PY8' 
            ,'VBFH125'  :'VBFH'         
            }.get(inname,'Unknown')

def GetMinitreeFileName(inname) :
    return {'ggH_1_1'       :'fiducial_minitree_v02/mc12_8TeV.160155.PowhegPythia8_AU2CT10_ggH125_ZZ4lep.Fiducial.root'
            ,'ggH_hfact_1_1':'fiducial_minitree_v02/mc12_8TeV.160155.PowhegPythia8_AU2CT10_ggH125_ZZ4lep.Fiducial.root'
            #,'ggH_hfact_1_1':'MyMinitree/MyMinitree.ggH.root'
            #,'ggH_hfact_1_1':'MyMinitree/160155_tag.root'
            #,'ggH_hfact_1_1':'MyMinitree/160155_with_leptons.root'
            #,'ggH_hfact_1_1':'MyMinitree/160155_with_leptons_no_ptrew.root'
            #,'ggH_hfact_1_1':'MyMinitree/160155_leps.root'            
            #,'ttH_1_1'      :'MyMinitrees/167562_leps.root'            
            #,'ttH_1_1'       :'MyMinitrees/167562_LatestStahlman.root'
            #,'ttH_1_1'       :'MyMinitrees/167562_mc12a.root'
            #,'ttH_1_1'       :'MyMinitrees/167562_mc12c.root'
            #,'ttH_1_1'       :'MyMinitrees/167562_mc12a_WRONGTAG.root'
            #,'ttH_1_1'       :'MyMinitrees/167562_mc12c_WRONGTAG.root'
            ,'ttH_1_1'      :'fiducial_minitree_v02/mc12_8TeV.167562.Pythia8_AU2CTEQ6L1_ttH125_ZZ4lep.Fiducial.root'
            ,'WH_1_1'       :'fiducial_minitree_v02/mc12_8TeV.160255.Pythia8_AU2CTEQ6L1_WH125_ZZ4lep.Fiducial.root'
            ,'ZH_1_1'       :'fiducial_minitree_v02/mc12_8TeV.160305.Pythia8_AU2CTEQ6L1_ZH125_ZZ4lep.Fiducial.root'
            ,'VBFH125_1_1'  :'fiducial_minitree_v02/mc12_8TeV.160205.PowhegPythia8_AU2CT10_VBFH125_ZZ4lep.Fiducial.root'
            }.get(inname)

# BRCorrection.h: 0 = 4mu, 1 = 2mu2e, 2 = 4e
# Jon minitree:   0 = 4mu, 1 = 4e   , 2,3 = mue,emu
#                                 4mu     2mu2e   4e
BRCorrection = {'ggH_1_1'       :[0.97365,0.97536,0.96402]
                ,'ggH_hfact_1_1':[0.97365,0.97536,0.96402]
                ,'ttH_1_1'      :[0.96980,0.96963,0.97422]
                ,'WH_1_1'       :[0.95893,0.97402,0.97346]
                ,'ZH_1_1'       :[0.95685,0.98536,0.97522]
                ,'VBFH125_1_1'  :[0.96534,0.97835,0.97496]
                }


def SetNjetsBins(plot) :
    plot.GetXaxis().SetBinLabel(1,'0')    
    plot.GetXaxis().SetBinLabel(2,'1')    
    plot.GetXaxis().SetBinLabel(3,'2')    
    plot.GetXaxis().SetBinLabel(4,'#geq3')

VarProps = dict()
VarProps['pt'      ] = dict()
VarProps['Rapidity'] = dict()
VarProps['jet1pt'  ] = dict()
VarProps['lep1'    ] = dict()
VarProps['lep2'    ] = dict()
VarProps['lep3'    ] = dict()
VarProps['lep4'    ] = dict()
VarProps['m12'     ] = dict()
VarProps['m34'     ] = dict()
VarProps['Njets'   ] = dict()
VarProps['cthstr'  ] = dict()
VarProps['Total'   ] = dict()

VarProps['pt'      ]['Bins'],VarProps['pt'      ]['BinStr'] = [0,20,50,100,200]          , '(20,0,200)'  
VarProps['Rapidity']['Bins'],VarProps['Rapidity']['BinStr'] = [0,0.3,0.65,1.0,1.4,2.4]   , '(48,0,2.4)'  
VarProps['jet1pt'  ]['Bins'],VarProps['jet1pt'  ]['BinStr'] = [0,30,50,70,140]           , '(14,0,140)'
VarProps['lep1'    ]['Bins'],VarProps['lep1'    ]['BinStr'] = [0,10,20,30,40,60]         , '(6,0,60)'   
VarProps['lep2'    ]['Bins'],VarProps['lep2'    ]['BinStr'] = [0,10,20,30,40,60]         , '(6,0,60)'   
VarProps['lep3'    ]['Bins'],VarProps['lep3'    ]['BinStr'] = [0,10,20,30,40,60]         , '(6,0,60)'   
VarProps['lep4'    ]['Bins'],VarProps['lep4'    ]['BinStr'] = [0,10,20,30,40,60]         , '(6,0,60)'   
VarProps['m12'     ]['Bins'],VarProps['m12'     ]['BinStr'] = [10,20,30,40,60]           , '(5,10,60)'   
VarProps['m34'     ]['Bins'],VarProps['m34'     ]['BinStr'] = [12.5,20,30,40,60]         , '(19,12.5,60)'
VarProps['Njets'   ]['Bins'],VarProps['Njets'   ]['BinStr'] = [-0.5,0.5,1.5,2.5,3.5]     , '(4,-0.5,3.5)'
VarProps['cthstr'  ]['Bins'],VarProps['cthstr'  ]['BinStr'] = [0.0,0.2,0.4,0.6,0.8,1.0]  , '(5,0,1)'     
VarProps['Total'   ]['Bins'],VarProps['Total'   ]['BinStr'] = [0.0,1.0]                  , '(1,0,1)'


# Debugging with minitrees binning
VarProps['pt'      ]['BinsMT'],VarProps['pt'      ]['BinStrMT'] = list(a*4 for a in range(0,51))     ,'(50,0,200)'
VarProps['Rapidity']['BinsMT'],VarProps['Rapidity']['BinStrMT'] = list(a*0.10 for a in range(0,25))  ,'(24,0,2.4)'
VarProps['jet1pt'  ]['BinsMT'],VarProps['jet1pt'  ]['BinStrMT'] = list(a*4 for a in range(0,36))     ,'(35,0,140)'
VarProps['lep1'    ]['BinsMT'],VarProps['lep1'    ]['BinStrMT'] = list(range(0,111))                 ,'(110,0,110)' # was 10-60
VarProps['lep2'    ]['BinsMT'],VarProps['lep2'    ]['BinStrMT'] = list(range(0,111))                 ,'(110,0,110)' # was 10-60
VarProps['lep3'    ]['BinsMT'],VarProps['lep3'    ]['BinStrMT'] = list(range(0,111))                 ,'(110,0,110)' # was 10-60
VarProps['lep4'    ]['BinsMT'],VarProps['lep4'    ]['BinStrMT'] = list(range(0,111))                 ,'(110,0,110)' # was 10-60
VarProps['m12'     ]['BinsMT'],VarProps['m12'     ]['BinStrMT'] = list(range(0,111))                 ,'(110,0,110)' # was 10-60
VarProps['m34'     ]['BinsMT'],VarProps['m34'     ]['BinStrMT'] = list(range(0,71))                  ,'(70,0,70)' # was 10-60
VarProps['Njets'   ]['BinsMT'],VarProps['Njets'   ]['BinStrMT'] = [-0.5,0.5,1.5,2.5,3.5]             ,'(4,-0.5,3.5)'
VarProps['cthstr'  ]['BinsMT'],VarProps['cthstr'  ]['BinStrMT'] = list(a*0.04 for a in range(0,26))  ,'(25,0,1)'
VarProps['Total'   ]['BinsMT'],VarProps['cthstr'  ]['BinStrMT'] = [0,1]                              ,'(1,0,1)'

# Correction factor binning
VarProps['pt'      ]['BinsCF'],VarProps['pt'      ]['BinStrCF'] = (list(a*2      for a in range(0,10))+
                                                                   list(a*3+20   for a in range(0,10))+
                                                                   list(a*5+50   for a in range(0,10))+
                                                                   list(a*10+100 for a in range(0,11))) ,'(200,0,200)'
VarProps['Rapidity']['BinsCF'],VarProps['Rapidity']['BinStrCF'] = (list(a*0.03       for a in range(0,10))+
                                                                   list(a*0.035+0.3  for a in range(0,10))+
                                                                   list(a*0.035+0.65 for a in range(0,10))+
                                                                   list(a*0.04+1.0   for a in range(0,10))+
                                                                   list(a*0.10+1.4   for a in range(0,10))+
                                                                   list(a*0.10+2.4   for a in range(0,17))) ,'(1000,0,4.0)'
VarProps['jet1pt'  ]['BinsCF'],VarProps['jet1pt'  ]['BinStrCF'] = ([0]+
                                                                   list(a*2+30 for a in range(0,20))+
                                                                   list(a*7+70 for a in range(0,11))) ,'(140,0,140)'
VarProps['lep1'    ]['BinsCF'],VarProps['lep1'    ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['lep2'    ]['BinsCF'],VarProps['lep2'    ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['lep3'    ]['BinsCF'],VarProps['lep3'    ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['lep4'    ]['BinsCF'],VarProps['lep4'    ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['m12'     ]['BinsCF'],VarProps['m12'     ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+
                                                                   list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['m34'     ]['BinsCF'],VarProps['m34'     ]['BinStrCF'] = (list(a*1+2 for a in range(0,38))+
                                                                   list(a*2+40 for a in range(0,11))) ,'(60,00,60)'
VarProps['Njets'   ]['BinsCF'],VarProps['Njets'   ]['BinStrCF'] = [-0.5,0.5,1.5,2.5,3.5] ,'(4,-0.5,3.5)'
VarProps['cthstr'  ]['BinsCF'],VarProps['cthstr'  ]['BinStrCF'] = list(a*0.02 for a in range(0,51)) ,'(50,0,1)'
VarProps['Total'   ]['BinsCF'],VarProps['Total'   ]['BinStrCF'] = [0,1] ,'(1,0,1)'

VarProps['pt'      ]['JonNaming'] = 'pt'          ; 
VarProps['Rapidity']['JonNaming'] = 'rapidity'    ; 
VarProps['jet1pt'  ]['JonNaming'] = 'leadingjetpt'; 
VarProps['lep1'    ]['JonNaming'] = 'lep1'        ; 
VarProps['lep2'    ]['JonNaming'] = 'lep2'        ; 
VarProps['lep3'    ]['JonNaming'] = 'lep3'        ; 
VarProps['lep4'    ]['JonNaming'] = 'lep4'        ; 
VarProps['m12'     ]['JonNaming'] = 'm12'         ; 
VarProps['m34'     ]['JonNaming'] = 'm34'         ; 
VarProps['Njets'   ]['JonNaming'] = 'njets'       ; 
VarProps['cthstr'  ]['JonNaming'] = 'costhetastar'; 
VarProps['Total'   ]['JonNaming'] = 'total'       ;

VarProps['pt'      ]['MinitreeDrawStr'] = 'higgs_pt'
VarProps['Rapidity']['MinitreeDrawStr'] = 'abs(higgs_rapidity)'
VarProps['jet1pt'  ]['MinitreeDrawStr'] = 'leading_jet_pt_truth_fid'
VarProps['lep1'    ]['MinitreeDrawStr'] = 'born_higgslepton1_pt'
VarProps['lep2'    ]['MinitreeDrawStr'] = 'born_higgslepton2_pt'
VarProps['lep3'    ]['MinitreeDrawStr'] = 'born_higgslepton3_pt'
VarProps['lep4'    ]['MinitreeDrawStr'] = 'born_higgslepton4_pt'
VarProps['m12'     ]['MinitreeDrawStr'] = 'born_paired_higgslep12_m'
VarProps['m34'     ]['MinitreeDrawStr'] = 'born_paired_higgslep34_m'
VarProps['Njets'   ]['MinitreeDrawStr'] = '(n_jets_truth_fid)*(n_jets_truth_fid<3) + 3*(n_jets_truth_fid>=3)'
VarProps['cthstr'  ]['MinitreeDrawStr'] = 'abs(born_paired_higgslep4_cthstr)'
VarProps['Total'   ]['MinitreeDrawStr'] = 'abs(?)'

VarProps['pt'      ]['MyDrawStr'] = 'H_truth_pt'
VarProps['Rapidity']['MyDrawStr'] = 'abs(H_truth_rap)'
VarProps['jet1pt'  ]['MyDrawStr'] = 'max(jet1_truth_fid_pt,0)'
VarProps['lep1'    ]['MyDrawStr'] = 'lep1_pt'
VarProps['lep2'    ]['MyDrawStr'] = 'lep2_pt'
VarProps['lep3'    ]['MyDrawStr'] = 'lep3_pt'
VarProps['lep4'    ]['MyDrawStr'] = 'lep4_pt'
VarProps['m12'     ]['MyDrawStr'] = 'H_truth_m12'
VarProps['m34'     ]['MyDrawStr'] = 'H_truth_m34'
VarProps['Njets'   ]['MyDrawStr'] = '(Njets_30GeV_truth_fid)*(Njets_30GeV_truth_fid<3) + 3*(Njets_30GeV_truth_fid>=3)'
VarProps['cthstr'  ]['MyDrawStr'] = 'abs(H_truth_cthstr)'
VarProps['Total'   ]['MyDrawStr'] = 'abs(?)'

#
# Plotting specifications
#
VarProps['pt'      ]['HistRange'] = [0,0.03];
VarProps['Rapidity']['HistRange'] = [0,2.00];
VarProps['jet1pt'  ]['HistRange'] = [0,0.07];
VarProps['lep1'    ]['HistRange'] = [0,0.10];
VarProps['lep2'    ]['HistRange'] = [0,0.10];
VarProps['lep3'    ]['HistRange'] = [0,0.10];
VarProps['lep4'    ]['HistRange'] = [0,0.10];
VarProps['m12'     ]['HistRange'] = [0,0.10];
VarProps['m34'     ]['HistRange'] = [0,0.10];
VarProps['Njets'   ]['HistRange'] = [0,1.00];
VarProps['cthstr'  ]['HistRange'] = [0,3.00];
VarProps['Total'   ]['HistRange'] = [0,2.00];

VarProps['pt'      ]['XLabel'] = 'p_{T} [GeV]'
VarProps['Rapidity']['XLabel'] = '|y|'
VarProps['jet1pt'  ]['XLabel'] = 'p_{T,jet1} [GeV]'
VarProps['lep1'    ]['XLabel'] = 'p_{T,lep1}'
VarProps['lep2'    ]['XLabel'] = 'p_{T,lep2}'
VarProps['lep3'    ]['XLabel'] = 'p_{T,lep3}'
VarProps['lep4'    ]['XLabel'] = 'p_{T,lep4}'
VarProps['m12'     ]['XLabel'] = 'm_{12}'
VarProps['m34'     ]['XLabel'] = 'm_{34}'
VarProps['Njets'   ]['XLabel'] = 'N_{jets}'
VarProps['cthstr'  ]['XLabel'] = '|cos(#theta*)|'
VarProps['Total'   ]['XLabel'] = 'Total'

VarProps['pt'      ]['YLabel'] = 'd#sigma_{fid}/dp_{T} [fb/GeV]'
VarProps['Rapidity']['YLabel'] = 'd#sigma_{fid}/d|y| [fb]'
VarProps['jet1pt'  ]['YLabel'] = 'd#sigma_{fid}/dp_{T,jet1} [fb/GeV]'
VarProps['lep1'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep1} [fb/GeV]'
VarProps['lep2'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep2} [fb/GeV]'
VarProps['lep3'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep3} [fb/GeV]'
VarProps['lep4'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep4} [fb/GeV]'
VarProps['m12'     ]['YLabel'] = 'd#sigma_{fid}/dm_{12} [fb/GeV]'
VarProps['m34'     ]['YLabel'] = 'd#sigma_{fid}/dm_{34} [fb/GeV]'
VarProps['Njets'   ]['YLabel'] = '#sigma_{fid} [fb]'
VarProps['cthstr'  ]['YLabel'] = 'd#sigma_{fid}/d|cos(#theta*)| [fb]'
VarProps['Total'   ]['YLabel'] = 'Total [fb]'

for k in VarProps.keys() :
    VarProps[k]['YLabel_gen'] = '#sigma_{generator} [fb]'
    VarProps[k]['YLabel_fid'] = '#sigma_{fiducial} [fb]'
    VarProps[k]['YLabel_eff'] = 'Fiducial Efficiency'

 # [0.5,1.5] # [.95,1.05]
VarProps['jet1pt'  ]['HistRange'] = [0,0.07];
VarProps['lep1'    ]['HistRange'] = [0,0.10];
VarProps['lep2'    ]['HistRange'] = [0,0.10];
VarProps['lep3'    ]['HistRange'] = [0,0.10];
VarProps['lep4'    ]['HistRange'] = [0,0.10];
VarProps['m12'     ]['HistRange'] = [0,0.10];
VarProps['m34'     ]['HistRange'] = [0,0.10];
VarProps['Njets'   ]['HistRange'] = [0,1.00];
VarProps['cthstr'  ]['HistRange'] = [0,3.00];

VarProps['pt'      ]['XLabel'] = 'p_{T} [GeV]'
VarProps['Rapidity']['XLabel'] = '|y|'
VarProps['jet1pt'  ]['XLabel'] = 'p_{T,jet1} [GeV]'
VarProps['lep1'    ]['XLabel'] = 'p_{T,lep1}'
VarProps['lep2'    ]['XLabel'] = 'p_{T,lep2}'
VarProps['lep3'    ]['XLabel'] = 'p_{T,lep3}'
VarProps['lep4'    ]['XLabel'] = 'p_{T,lep4}'
VarProps['m12'     ]['XLabel'] = 'm_{12}'
VarProps['m34'     ]['XLabel'] = 'm_{34}'
VarProps['Njets'   ]['XLabel'] = 'N_{jets}'
VarProps['cthstr'  ]['XLabel'] = '|cos(#theta*)|'

VarProps['pt'      ]['YLabel'] = 'd#sigma_{fid}/dp_{T} [fb/GeV]'
VarProps['Rapidity']['YLabel'] = 'd#sigma_{fid}/d|y| [fb]'
VarProps['jet1pt'  ]['YLabel'] = 'd#sigma_{fid}/dp_{T,jet1} [fb/GeV]'
VarProps['lep1'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep1} [fb/GeV]'
VarProps['lep2'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep2} [fb/GeV]'
VarProps['lep3'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep3} [fb/GeV]'
VarProps['lep4'    ]['YLabel'] = 'd#sigma_{fid}/dp_{T,lep4} [fb/GeV]'
VarProps['m12'     ]['YLabel'] = 'd#sigma_{fid}/dm_{12} [fb/GeV]'
VarProps['m34'     ]['YLabel'] = 'd#sigma_{fid}/dm_{34} [fb/GeV]'
VarProps['Njets'   ]['YLabel'] = '#sigma_{fid} [fb]'
VarProps['cthstr'  ]['YLabel'] = 'd#sigma_{fid}/d|cos(#theta*)| [fb]'

for k in VarProps.keys() :
    VarProps[k]['YLabel_gen'] = '#sigma_{generator} [fb]'
    VarProps[k]['YLabel_fid'] = '#sigma_{fiducial} [fb]'
    VarProps[k]['YLabel_eff'] = 'Fiducial Efficiency'
    VarProps[k]['RatioRange']     = [.95,1.05]
    #VarProps[k]['RatioRange']     = [0.8,1.20]
    VarProps[k]['RatioRange_fid'] = [0.8,1.20]
    VarProps[k]['RatioRange_gen'] = [0.8,1.20]
    VarProps[k]['RatioRange_eff'] = [0.8,1.20]


# Types: baseline up down
# gg_H: 13.255 11.292 15.787
# gg_HJ: 8.466 7.007 10.13
# gg_HJJ: 1.837 1.417 2.232
# vbf_H: 1.5896 1.5882 1.5847

# ggH_05_05: 15.82438 pb +/- 0.00095
# ggH_05_01: 13.20092 pb +/- 0.00075
# ggH_01_05: 15.90058 pb +/- 0.00093
# ggH_01_01: 13.28452 pb +/- 0.00077
# ggH_01_02: 11.26612 pb +/- 0.00063
# ggH_02_01: 13.34035 pb +/- 0.00078
# ggH_02_02: 11.31152 pb +/- 0.00059

CrossSections = {'minlo_HJ':(1.25541E+01,7.04881E-03)
                 ,'minlo_HJJ':(13.28452,0.00077)      # not correct yet
                 ,'ggH':(1.73089E+01,1.25338E-01)
                 ,'ggH_0.5_0.5': 15.82438
                 ,'ggH_0.5_1'  : 13.20092
                 ,'ggH_1_0.5'  : 15.90058
                 ,'ggH_1_1'    : 13.28452
                 ,'ggH_1_2'    : 11.26612
                 ,'ggH_2_1'    : 13.34035
                 ,'ggH_2_2'    : 11.31152
                 ,'ggH_hfact_0.5_0.5': 15.82438
                 ,'ggH_hfact_0.5_1'  : 13.20092
                 ,'ggH_hfact_1_0.5'  : 15.90058
                 ,'ggH_hfact_1_1'    : 13.25896 # from POWHEG-BOX
                 ,'ggH_hfact_1_2'    : 11.26612
                 ,'ggH_hfact_2_1'    : 13.34035
                 ,'ggH_hfact_2_2'    : 11.31152
#                  ,'minlo_HJ_mH125_0.5_0.5': # 9962433.50*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_0.5_1'  : # 10004917.5*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_1_0.5'  : # 7391291.25*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_1_1'    : # 7554040.00*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_1_2'    : # 7630847.75*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_2_1'    : # 6457037.75*(1.25541E+01)/float(7554040.0)
#                  ,'minlo_HJ_mH125_2_2'    : # 6533619.25*(1.25541E+01)/float(7554040.0)
                 ,'minlo_HJ_mH125_0.5_0.5': 16.57390 # from my production
                 ,'minlo_HJ_mH125_0.5_1'  : 16.65165 # from my production
                 ,'minlo_HJ_mH125_1_0.5'  : 12.31903 # from my production
                 ,'minlo_HJ_mH125_1_1'    : 12.60750 # from my production
                 ,'minlo_HJ_mH125_1_2'    : 12.69589 # from my production
                 ,'minlo_HJ_mH125_2_1'    : 10.75078 # from my production
                 ,'minlo_HJ_mH125_2_2'    : 10.86866 # from my production
                 ,'ttH_1_1'   :  0.1293 # YR
                 ,'WH_1_1'    :  0.7046 # YR
                 ,'ZH_1_1'    :  0.4153 # YR
                 ,'VBFH125_0.5_0.5':  1.578
                 ,'VBFH125_0.5_1'  :  1.578
                 ,'VBFH125_1_0.5'  :  1.578
                 ,'VBFH125_1_1'    :  1.578 # from YR #### 1.59426 # from POWHEG-BOX
                 ,'VBFH125_1_2'    :  1.578
                 ,'VBFH125_2_1'    :  1.578
                 ,'VBFH125_2_2'    :  1.578
                 }

CrossSections_Errors = {'ggH_1_1'     :{'QCD_Up':7.2,'QCD_Dn':7.8,'PDF_Up':7.5,'PDF_Dn':6.9}
                        ,'VBFH125_1_1':{'QCD_Up':0.2,'QCD_Dn':0.2,'PDF_Up':2.6,'PDF_Dn':2.8}
                        ,'WH_1_1'     :{'QCD_Up':1.0,'QCD_Dn':1.0,'PDF_Up':2.3,'PDF_Dn':2.3}
                        ,'ZH_1_1'     :{'QCD_Up':3.1,'QCD_Dn':3.1,'PDF_Up':2.5,'PDF_Dn':2.5}
                        ,'ttH_1_1'    :{'QCD_Up':3.8,'QCD_Dn':9.3,'PDF_Up':8.1,'PDF_Dn':8.1}
                        ,'minlo_HJ_mH125_1_1':{'QCD_Up':7.2,'QCD_Dn':7.8,'PDF_Up':7.5,'PDF_Dn':6.9}
                        }

CrossSections_Shape = {'minlo_HJ':(1.25541E+01,7.04881E-03)
                       ,'minlo_HJJ':(13.28452,0.00077)     # not correct yet
                       ,'ggH':(1.73089E+01,1.25338E-01)
                       ,'ggH_0.5_0.5': 19.270 
                       ,'ggH_0.5_1'  : 19.270 
                       ,'ggH_1_0.5'  : 19.270 
                       ,'ggH_1_1'    : 19.270 
                       ,'ggH_1_2'    : 19.270 
                       ,'ggH_2_1'    : 19.270 
                       ,'ggH_2_2'    : 19.270 
                       ,'ggH_hfact_0.5_0.5': 19.270  
                       ,'ggH_hfact_0.5_1'  : 19.270  
                       ,'ggH_hfact_1_0.5'  : 19.270  
                       ,'ggH_hfact_1_1'    : 19.270  
                       ,'ggH_hfact_1_2'    : 19.270  
                       ,'ggH_hfact_2_1'    : 19.270  
                       ,'ggH_hfact_2_2'    : 19.270  
#                        ,'minlo_HJ_mH125_0.5_0.5': 1.25541E+01
#                        ,'minlo_HJ_mH125_0.5_1'  : 1.25541E+01
#                        ,'minlo_HJ_mH125_1_0.5'  : 1.25541E+01
#                        ,'minlo_HJ_mH125_1_1'    : 1.25541E+01
#                        ,'minlo_HJ_mH125_1_2'    : 1.25541E+01
#                        ,'minlo_HJ_mH125_2_1'    : 1.25541E+01
#                        ,'minlo_HJ_mH125_2_2'    : 1.25541E+01
                       ,'minlo_HJ_mH125_0.5_0.5': 19.270 
                       ,'minlo_HJ_mH125_0.5_1'  : 19.270 
                       ,'minlo_HJ_mH125_1_0.5'  : 19.270 
                       ,'minlo_HJ_mH125_1_1'    : 19.270 
                       ,'minlo_HJ_mH125_1_2'    : 19.270 
                       ,'minlo_HJ_mH125_2_1'    : 19.270 
                       ,'minlo_HJ_mH125_2_2'    : 19.270 
                       ,'ttH_1_1'    :  0.1293 # YR
                       ,'WH_1_1'     :  0.7046 # YR
                       ,'ZH_1_1'     :  0.4153 # YR
                       ,'VBFH125_0.5_0.5':  1.578
                       ,'VBFH125_0.5_1'  :  1.578
                       ,'VBFH125_1_0.5'  :  1.578
                       ,'VBFH125_1_1'    :  1.578 # from YR #### 1.59426 # from POWHEG-BOX
                       ,'VBFH125_1_2'    :  1.578
                       ,'VBFH125_2_1'    :  1.578
                       ,'VBFH125_2_2'    :  1.578
                       }
