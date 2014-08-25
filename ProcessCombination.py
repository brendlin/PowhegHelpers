#!/usr/bin/env python

from ROOT import TFile
from PyGenericUtils import GetRootObj,CleanNameForMacro
from MinloTheory import QuadratureUpDown,LinearUpDown
from Variables import VarProps

# ggH_prediction = 'ggH'
# ggH_prediction = 'Minlo_HJPY8'
ggH_prediction = 'HRes'

ggH_name = {'ggH':'Powheg'
            ,'Minlo_HJPY8':'HJ'
            ,'HRes':'HRes'
            }

variables = []
variables.append('pt')
variables.append('Rapidity')
# variables.append('jet1pt')
# variables.append('m34')
# variables.append('Njets')
# variables.append('cthstr')

files = dict()
files['ggH' ] = TFile('rootfiles/Predictions_%s.root'%(ggH_prediction))
files['VBFH'] = TFile('rootfiles/Predictions_VBFH.root')
files['WH'  ] = TFile('rootfiles/Predictions_WH.root')
files['ZH'  ] = TFile('rootfiles/Predictions_ZH.root')
files['ttH' ] = TFile('rootfiles/Predictions_ttH.root')

f = TFile('rootfiles/FinalPrediction.root','recreate')

for i in variables :
    ##
    ## Add all processes' pdf/eigen linearly
    ##
    textfile = open('rootfiles/WorkspaceInput.%s.dsigmadx%s.txt'%(VarProps[i]['JonNaming'],ggH_name[ggH_prediction]),'w')

    pdf_shapes = []
    pdf_shapes.append(GetRootObj(files['ggH' ],'Higgs_%s_%s_Combined_PDF_Envelope'%(i,ggH_prediction )))
    pdf_shapes.append(GetRootObj(files['VBFH'],'Higgs_%s_%s_Combined_PDF_Envelope'%(i,'VBFH')))
    # pdf_shapes.append(GetRootObj(files['WH'  ],'Higgs_%s_%s_Combined_PDF_Envelope'%(i,'WH'  )))
    # pdf_shapes.append(GetRootObj(files['ZH'  ],'Higgs_%s_%s_Combined_PDF_Envelope'%(i,'ZH'  )))
    # pdf_shapes.append(GetRootObj(files['ttH' ],'Higgs_%s_%s_Combined_PDF_Envelope'%(i,'ttH' )))
    pdf_shape_all = LinearUpDown('PDF Shape All',asymlist=pdf_shapes,AddHists=True)

    pdf_flat = []
    pdf_flat.append(GetRootObj(files['ggH' ],'Higgs_%s_%s_Flat_Combined_PDF_Envelope'%(i,ggH_prediction )))
    pdf_flat.append(GetRootObj(files['VBFH'],'Higgs_%s_%s_Flat_Combined_PDF_Envelope'%(i,'VBFH')))
    pdf_flat.append(GetRootObj(files['WH'  ],'Higgs_%s_%s_Flat_Combined_PDF_Envelope'%(i,'WH'  )))
    pdf_flat.append(GetRootObj(files['ZH'  ],'Higgs_%s_%s_Flat_Combined_PDF_Envelope'%(i,'ZH'  )))
    pdf_flat.append(GetRootObj(files['ttH' ],'Higgs_%s_%s_Flat_Combined_PDF_Envelope'%(i,'ttH' )))
    pdf_flat_all = LinearUpDown('PDF Flat All',asymlist=pdf_flat,AddHists=True)

    qcd_shapes = []
    qcd_shapes.append(GetRootObj(files['ggH' ],'Higgs_%s_%s_Scale_Envelope'%(i,ggH_prediction )))
    qcd_shapes.append(GetRootObj(files['VBFH'],'Higgs_%s_%s_Scale_Envelope'%(i,'VBFH')))
    # qcd_shapes.append(GetRootObj(files['WH'  ],'Higgs_%s_%s_Scale_Envelope'%(i,'WH'  )))
    # qcd_shapes.append(GetRootObj(files['ZH'  ],'Higgs_%s_%s_Scale_Envelope'%(i,'ZH'  )))
    # qcd_shapes.append(GetRootObj(files['ttH' ],'Higgs_%s_%s_Scale_Envelope'%(i,'ttH' )))
    qcd_shape_all = LinearUpDown('QCD Shape All',asymlist=qcd_shapes,AddHists=True)

    qcd_flat = []
    qcd_flat.append(GetRootObj(files['ggH' ],'Higgs_%s_%s_Flat_Scale_Envelope'%(i,ggH_prediction )))
    qcd_flat.append(GetRootObj(files['VBFH'],'Higgs_%s_%s_Flat_Scale_Envelope'%(i,'VBFH')))
    qcd_flat.append(GetRootObj(files['WH'  ],'Higgs_%s_%s_Flat_Scale_Envelope'%(i,'WH'  )))
    qcd_flat.append(GetRootObj(files['ZH'  ],'Higgs_%s_%s_Flat_Scale_Envelope'%(i,'ZH'  )))
    qcd_flat.append(GetRootObj(files['ttH' ],'Higgs_%s_%s_Flat_Scale_Envelope'%(i,'ttH' )))
    qcd_flat_all = LinearUpDown('QCD Flat All',asymlist=qcd_flat,AddHists=True)
    
    mc_stat = []
    mc_stat.append(GetRootObj(files['ggH' ],'Higgs_%s_%s_MC_Statistics'%(i,ggH_prediction )))
    mc_stat.append(GetRootObj(files['VBFH'],'Higgs_%s_%s_MC_Statistics'%(i,'VBFH')))
    mc_stat.append(GetRootObj(files['WH'  ],'Higgs_%s_%s_MC_Statistics'%(i,'WH'  )))
    mc_stat.append(GetRootObj(files['ZH'  ],'Higgs_%s_%s_MC_Statistics'%(i,'ZH'  )))
    mc_stat.append(GetRootObj(files['ttH' ],'Higgs_%s_%s_MC_Statistics'%(i,'ttH' )))
    mc_stat_all = QuadratureUpDown('%s MC Stat All'%(i),hists=mc_stat,AddHists=True)
    
    text = ('Nominal,dsigmadx%s'%(ggH_name[ggH_prediction])).ljust(35)
    for i in range(pdf_shape_all.GetN()) :
        text += str( ' %f'%(mc_stat_all.GetY()[i])).ljust(20)
    text += '\n'
    textfile.write(text)

    text = 'MCStat_dsigmadx,Sym'.ljust(35)
    for i in range(mc_stat_all.GetN()) :
        text += str(' %f'%(100.*mc_stat_all.GetEYlow()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'PDF_dsigmadx_shape,Down'.ljust(35)
    for i in range(pdf_shape_all.GetN()) :
        text += str('%f'%(-100.*pdf_shape_all.GetEYlow()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'PDF_dsigmadx_shape,Up'.ljust(35)
    for i in range(pdf_shape_all.GetN()) :
        text += str(' %f'%(100.*pdf_shape_all.GetEYhigh()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'PDF_dsigmadx_norm,Down'.ljust(35)
    for i in range(pdf_flat_all.GetN()) :
        text += str('%f'%(-100.*pdf_flat_all.GetEYlow()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'PDF_dsigmadx_norm,Up'.ljust(35)
    for i in range(pdf_flat_all.GetN()) :
        text += str(' %f'%(100.*pdf_flat_all.GetEYhigh()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'QCD_dsigmadx_shape,Down'.ljust(35)
    for i in range(qcd_shape_all.GetN()) :
        text += str('%f'%(-100.*qcd_shape_all.GetEYlow()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'QCD_dsigmadx_shape,Up'.ljust(35)
    for i in range(qcd_shape_all.GetN()) :
        text += str(' %f'%(100.*qcd_shape_all.GetEYhigh()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'QCD_dsigmadx_norm,Down'.ljust(35)
    for i in range(qcd_flat_all.GetN()) :
        text += str('%f'%(-100.*qcd_flat_all.GetEYlow()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    text = 'QCD_dsigmadx_norm,Up'.ljust(35)
    for i in range(qcd_flat_all.GetN()) :
        text += str(' %f'%(100.*qcd_flat_all.GetEYhigh()[i]/float(mc_stat_all.GetY()[i]))).ljust(20)
    text += '\n'
    textfile.write(text)
    
    textfile.close()

    final_all = QuadratureUpDown('%s All Uncertainties'%(i),asymlist=[pdf_shape_all
                                                                      ,pdf_flat_all
                                                                      ,qcd_shape_all
                                                                      ,qcd_flat_all
                                                                      ,mc_stat_all
                                                                      ]
                                 )
    
    f.cd()
    final_all.Write(CleanNameForMacro(final_all.GetName()))
    
f.Close()
