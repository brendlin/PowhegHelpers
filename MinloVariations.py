#!/usr/bin/env python

import os
from ROOT import gROOT,TFile,TH1F,TGraphAsymmErrors,gDirectory,TH1,kFALSE,kRed,kAzure,kOrange
gROOT.LoadMacro("rootlogon.C")
from ROOT import rootlogon
rootlogon()
from PlotUtils import PlotObject
from PyGenericUtils import GetRootObj,GetFile,CleanNameForMacro
import math
from array import array
import time
from MinloTheory import envelope,eigenvectorQuadrature,rebinme,ConvertNeventsToDSigma,NameConvert
from MinloTheory import QuadratureUpDown,AsymmErrsToPlusMinusSigma,GetVariationName
from MinloTheory import FlatErrorToAsymmErrs
from Variables import GetSampleName,GetMinitreeFileName
from Variables import SetNjetsBins,VarProps,BRCorrection
from Variables import CrossSections as CrossSections_ShapeNorm
from Variables import CrossSections_Shape as CrossSections_Shape
from Variables import CrossSections_Errors
gROOT.SetBatch(True)
#TH1.AddDirectory(kFALSE)

##
## var: variable name as in tree
## histbins: e.g. (100,0,200)
## quantity options: diff, fid, eff, gen
##
def GetMyPlot(tree,var,histbins,cross_section,quantity='diff',weight_str='weight') :

    # old way
#     br_2mu2e = 0.0000593*2. # multiply by 2 because 1/2 of the integral is not 2mu2e
#     br_4mu4e = 0.0000327*4. # multiply by 4 because 3/4 of the integral is not 4e / not 4mu
    
#     w_2mu2e = 1000.*cross_section*br_2mu2e/float(total_events)
#     w_4mu4e = 1000.*cross_section*br_4mu4e/float(total_events)

#     # For use with tau sample
#     br_2mu2e = 1.000*0.0000593*9./2. # multiply by 2 because 1/2 of the integral is not 2mu2e
#     br_4mu4e = 1.000*0.0000327*9. # multiply by 4 because 3/4 of the integral is not 4e / not 4mu
#     # tau
#     w_2mu2e = 1000.*cross_section*br_2mu2e/float(1248536.)
#     w_4mu4e = 1000.*cross_section*br_4mu4e/float(1248536.)

    # new way - one less factor of 2
    # Also this avoids the need of a BR correction, since
    # the denominator is the number
    #
    br_2mu2e = 0.0000593*1. # 
    br_4mu4e = 0.0000327*2. # 
    # new way
    tree.Draw('is2mu2e>>h00(2,0,2)',weight_str,'egoff')
    e_nevents_2mu2e = gDirectory.Get('h00').GetBinContent(2)
    e_nevents_4mu4e = gDirectory.Get('h00').GetBinContent(1)
    gROOT.ProcessLine('delete h00')
    # new way
    w_2mu2e = 1000.*cross_section*br_2mu2e/float(e_nevents_2mu2e)
    w_4mu4e = 1000.*cross_section*br_4mu4e/float(e_nevents_4mu4e)

    #
    # Quantity (or numerator)
    #
    full_weight = weight_str
    if quantity in ['diff','eff','fid'] : 
        full_weight += '*PassesCuts'
    full_weight += '*(is2mu2e*(%2.4fe-8)+(1-is2mu2e)*(%2.4fe-8))'%(w_2mu2e*1e8,w_4mu4e*1e8)

    tree.Draw('%s>>h1%s'%(var,histbins),full_weight,'egoff')
    h1 = gDirectory.Get('h1')

    if quantity == 'eff' :
        full_weight = full_weight.replace('*PassesCuts','')
        tree.Draw('%s>>Den%s'%(var,histbins),full_weight,'egoff')
        Den = gDirectory.Get('Den')
        h1.Divide(h1,Den,1,1,'B')
        gROOT.ProcessLine('delete Den')
        
    if quantity == 'diff' :
        ConvertNeventsToDSigma(h1)

    return h1

def GetJonPlot(tree_gen,tree_fid,var,histbins,quantity='diff') :
    #
    # Quantity, or numerator
    #
    #jon_weight = '0.0000072*(event_type_truth<4)/20.277'
    jon_weight = 'weight_fiducial*(event_type_truth<4)/20.277'
    if quantity in ['fid','diff','eff'] :
        #jon_weight += '*(118.<=dressed_lep4_m && dressed_lep4_m<=129.)'
        jon_weight += '*(118.<=bare_lep4_m && bare_lep4_m<=129.)'
        the_tree = tree_fid
    else :
        the_tree = tree_gen
        
    the_tree.Draw('%s>>h1%s'%(var,histbins),jon_weight,'egoff')
    h1 = gDirectory.Get('h1')

    if quantity == 'eff' :
        #jon_weight = jon_weight.replace('*(118.<=dressed_lep4_m && dressed_lep4_m<=129.)','')
        jon_weight = jon_weight.replace('*(118.<=bare_lep4_m && bare_lep4_m<=129.)','')
        tree_gen.Draw('%s>>Den%s'%(var,histbins),jon_weight,'egoff')
        Den = gDirectory.Get('Den')
        h1.Divide(h1,Den,1,1,'B')
        gROOT.ProcessLine('delete Den')

    if quantity == 'diff' :
        ConvertNeventsToDSigma(h1)

    return h1

def main(ops,args) :

    inom = list(('_1_1' in a) for a in ops.variations).index(True)

    SampleType = GetSampleName(ops.variations[inom].replace('_1_1',''))
    SampleTypeClean = CleanNameForMacro(SampleType)

    CrossSections = CrossSections_ShapeNorm
    if ops.doCorrectionFactorWeights or ops.doShapeVariations or ops.doDebug :
        CrossSections = CrossSections_Shape

#     if ops.doDebug :
#         for i in ops.Variables :
#             VarProps[i]['Bins'] = VarProps[i]['BinsMT']
#             VarProps[i]['BinStr'] = VarProps[i]['BinStrMT']

    if ops.doCorrectionFactorWeights :
        #
        # Want to contain everything within the histogram
        #
        for i in ops.Variables :
            VarProps[i]['Bins'] = VarProps[i]['BinsCF']
            VarProps[i]['BinStr'] = VarProps[i]['BinStrCF']
            VarProps[i]['MyDrawStr'] = 'min(max(%s,%s),%s)'%(VarProps[i]['MyDrawStr'],VarProps[i]['Bins'][0]+0.001,VarProps[i]['Bins'][-1]-0.001)

    #
    # Labeling
    #
    if ops.process == 'hj' :
        for i in ops.Variables :
            VarProps[i]['RatioRange'] = [0.85,1.15]
            
    for i in ops.Variables :
        if 'YLabel_%s'%(ops.quantity) in VarProps[i].keys() :
            VarProps[i]['YLabel'] = VarProps[i]['YLabel_%s'%(ops.quantity)]
        if 'RatioRange_%s'%(ops.quantity) in VarProps[i].keys() :
            VarProps[i]['RatioRange'] = VarProps[i]['RatioRange_%s'%(ops.quantity)]

    the_hists = dict() ## dictionary for pt

    for v in ops.variations :
        if v == 'dummy' : continue
        print 'Getting plots for %s ...'%v

        f = GetFile('var/out/hadded/%s.root'%v)
        e = f.Get('EvtTree')

        for i in sorted(ops.Variables) :
            key = '%s, %s'%(i,v)
            the_hists[key] = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
            the_hists[key].SetDirectory(0)

            h1 = GetMyPlot(e
                           ,VarProps[i]['MyDrawStr']
                           ,VarProps[i]['BinStr']
                           ,CrossSections.get(v)
                           ,quantity=ops.quantity
                           )

            rebinme(h1,the_hists['%s, %s'%(i,v)])
            gROOT.ProcessLine('delete h1')

            if i == 'Njets' : SetNjetsBins(the_hists['%s, %s'%(i,v)])

        # Close file.
        f.Close()

    ##
    ## MC stats
    ##
    OutputFile = TFile('rootfiles/Predictions_%s.root'%(SampleTypeClean),'recreate')
    for i in sorted(ops.Variables) :
        PlotName = 'Higgs %s %s MC Statistics'%(i,SampleType)
        the_hists['%s, %s'%(i,ops.variations[inom])].Write(CleanNameForMacro(PlotName))
    OutputFile.Close()

    sp_StahlXck = []
    ##
    ## Cross-check with Stahlman
    ##
    if ops.debug : # now using actual minitrees
        print 'Debugging with minitrees...'
        # taken from /afs/cern.ch/atlas/groups/HSG2/H4l_2013/Autumn/MiniTrees/fiducial_minitree_v01
        #minitreedir = 'fiducial_minitree_v01/'
        # new jon fiducial minitree stuff
        #minitreedir = 'fiducial_minitree_v02/'
        #minitreedir = '04032014/' # use this as default!
        filename = GetMinitreeFileName(ops.variations[inom])
        print 'using filename',filename
        fm = GetFile(filename)
        em_gen = fm.Get('tree_incl_gen')
        em_fid = fm.Get('tree_incl_fid')

        for i in sorted(ops.Variables) :

            key = 'Minitree ggH %s'%(i)
            the_hists[key] = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
            the_hists[key].SetDirectory(0)

            h1 = GetJonPlot(em_gen,em_fid
                            ,VarProps[i]['MinitreeDrawStr']
                            ,VarProps[i]['BinStr']
                            ,quantity=ops.quantity
                            )
            rebinme(h1,the_hists['Minitree ggH %s'%(i)])
            gROOT.ProcessLine('delete h1')

        for i in sorted(ops.Variables) :
            # print 'making plot object for',i
            sp_StahlXck.append(PlotObject('Higgs %s'%i,[the_hists['Minitree ggH %s'%(i)]]+list(the_hists['%s, %s'%(i,a)] for a in ops.variations)))
            ###
            ###
            ###
            sp_StahlXck[-1].SetAxisLabels(VarProps[i]['XLabel'],VarProps[i]['YLabel'])
            sp_StahlXck[-1].plots[0].SetMinimum(0)
            sp_StahlXck[-1].MakeRatioPlot(0,list(range(1,len(sp_StahlXck[-1].plots))))
            sp_StahlXck[-1].plots[0].SetName('Minitree %s'%(SampleType))
            sp_StahlXck[-1].plots[1].SetName('Powheg+Pythia8 %s'%(SampleType))
            sp_StahlXck[-1].RecreateLegend(.48,.7,.97,.86,can='RatioPadTop')
            if ops.quantity == 'gen' :
                sp_StahlXck[-1].DrawTextNDC(.48,.88,'Generator-Level',can='RatioPadTop',size=0.050)
            sp_StahlXck[-1].DrawHorizontal(1,can='RatioPadBot')
            sp_StahlXck[-1].SetTopYaxisRange(0,sp_StahlXck[-1].RatioTopPlot0.GetMaximum()*1.3)
            sp_StahlXck[-1].SetBotYaxisRange(VarProps[i]['RatioRange'][0],VarProps[i]['RatioRange'][1])

            if i == 'Njets' : SetNjetsBins(sp_StahlXck[-1].plots[0])

                

            is_generated = {'gen':'Generator'
                            ,'fid':'Fiducial'
                            ,'diff':'Differential'
                            ,'eff':'FidEfficiency'
                            }.get(ops.quantity)
            sp_StahlXck[-1].SaveAll(name='%s_%s_%s_Validation'%(SampleTypeClean,is_generated,i),can='ratio',dir='plots/%s'%(SampleTypeClean))
            ###
            ###
            ###

    if ops.doCorrectionFactorWeights :
        CorrFacts = TFile('rootfilesCorrectionFactorWeights_%s.root'%(SampleTypeClean),'recreate')
        for i in sorted(ops.Variables) :
            key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'scale','all','nominal')
            the_hists['%s, %s'%(i,ops.variations[inom])].Write(key)
        CorrFacts.Close()
        
    if ops.quantity == 'eff' :
        feff = TFile('%s_FiducialAcceptance.root'%(SampleTypeClean),'recreate')
        for i in sorted(ops.Variables) :
            the_hists['%s, %s'%(i,ops.variations[inom])].Write('%s_%s_FiducialAcceptance'%(SampleTypeClean,i))
        feff.Close()

    #
    # Scale Variations
    #
    sp_Scales = []
    if ops.doScaleVariations :
        print 'Running scale variations...'
        #for i in ['pt','Rapidity','jet1pt','m34','Njets','cthstr'] :
        for i in sorted(ops.Variables) :
            PlotName = 'Higgs %s %s ScaleVar'%(i,SampleType)
            for a in ops.variations : 
                NameConvert(the_hists['%s, %s'%(i,a)])
                the_hists['%s, %s'%(i,a)].SetName(the_hists['%s, %s'%(i,a)].GetName().replace('ggH_hfact',''))
                the_hists['%s, %s'%(i,a)].SetName(the_hists['%s, %s'%(i,a)].GetName().replace('ggH',''))
                the_hists['%s, %s'%(i,a)].SetName(the_hists['%s, %s'%(i,a)].GetName().replace('minlo_HJ_mH125',''))
                the_hists['%s, %s'%(i,a)].SetName(the_hists['%s, %s'%(i,a)].GetName().replace('minlo_HJJ_mH125',''))
                the_hists['%s, %s'%(i,a)].SetName(the_hists['%s, %s'%(i,a)].GetName().replace(i+', ',''))
            ###
            ###
            ###
            sp_Scales.append(PlotObject(PlotName,list(the_hists['%s, %s'%(i,a)] for a in ops.variations)))
            sp_Scales[-1].SetAxisLabels(VarProps[i]['XLabel'],VarProps[i]['YLabel'])
            sp_Scales[-1].plots[0].SetMinimum(0)
            sp_Scales[-1].RecreateLegend(.7,.5,.9,.9)
            sp_Scales[-1].MakeRatioPlot(inom,list(range(0,len(sp_Scales[-1].plots))),style='DiffXsec' if not ops.doCorrectionFactorWeights else 'MoreRatio')
            if ops.doCorrectionFactorWeights :
                sp_Scales[-1].SetTopYaxisRange(0,sp_Scales[-1].RatioTopPlot0.GetMaximum()*2.5)
                sp_Scales[-1].SetBotYaxisRange(0.8,1.2)
            else :
                sp_Scales[-1].SetTopYaxisRange(VarProps[i]['HistRange' ][0],VarProps[i]['HistRange' ][1])
                sp_Scales[-1].SetBotYaxisRange(VarProps[i]['RatioRange'][0],VarProps[i]['RatioRange'][1])
            sp_Scales[-1].ratioplots[0].GetYaxis().SetNdivisions(5,5,0)

            if i == 'Njets' : SetNjetsBins(sp_Scales[-1].plots[0])

            if ops.doCorrectionFactorWeights : 
                sp_Scales[-1].can.SetName('CorrectionFactor_'+sp_Scales[-1].can.GetName())

            if ops.quantity == 'eff' :
                feff = TFile('%s_FiducialAcceptance.root'%(SampleTypeClean),'update')
                for a in ops.variations :
                    the_hists['%s, %s'%(i,a)].Write('%s_%s_%s_FiducialAcceptance'%(SampleTypeClean,i,a))
                feff.Close()


            sp_Scales[-1].SaveAll(can='ratio',dir='plots/%s'%(SampleTypeClean))
            ###
            ###
            ###
            if ops.doCorrectionFactorWeights :
                for a in ops.variations :
                    CorrFacts = TFile('rootfiles/CorrectionFactorWeights_%s.root'%(SampleTypeClean),'update')
                    CorrFacts.cd()
                    # print i,a
                    tmp = the_hists['%s, %s'%(i,a)].Clone()
                    key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'scale','all',GetVariationName(tmp))
                    tmp.SetName(key)
                    if i == 'Njets' : SetNjetsBins(tmp)
                    tmp.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
                    for x in range(tmp.GetNbinsX()) :
                        tmp.SetBinError(x+1,0)
                        tmp.SetBinError(x+1,0)
                    tmp.Write()
                    CorrFacts.Close()
                ## variations
            ## doCorrectionFactorWeights
        ## Variables
    ## DoScale

    #
    # Scale envelope
    #
    sp_envelopes = []
    sp_CFScaleEnvelopes = []
    Scale_Envelope = dict()
    dummies = dict()
    if ops.doScaleVariations :
        for i in sorted(ops.Variables) :
            key = '%s, dummy'%(i)
            dummies[i] = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
            Scale_Envelope[i] = envelope(the_hists                                      # dictionary from which to pull
                                     ,list('%s, %s'%(i,a) for a in ops.variations)      # variations from which to take envelope
                                     ,the_hists['%s, %s'%(i,ops.variations[inom])] # nominal hist
                                     )
            Scale_Envelope[i].SetName('%s Scale envelope'%SampleType)
            PlotName = 'Higgs %s %s Scale Envelope'%(i,SampleType)
            OutputFile = TFile('rootfiles/Predictions_%s.root'%(SampleTypeClean),'update')
            Scale_Envelope[i].Write(CleanNameForMacro(PlotName))
            OutputFile.Close()
# #             sp_envelopes.append(PlotObject(PlotName,[dummies[i],Scale_Envelope[i]],drawopt='E1',drawtitle=False))
# #             sp_envelopes[-1].SetAxisLabels(VarProps[i]['XLabel'],VarProps[i]['YLabel'])
# #             sp_envelopes[-1].plots[1].SetDrawOption('pE2sames')
# #             sp_envelopes[-1].plots[1].SetFillStyle(3002)
# #             sp_envelopes[-1].plots[1].SetFillColor(kRed+1)
# #             if ops.doCorrectionFactorWeights :
# #                 yaxis_label = VarProps[i]['GenYLabel']
# #                 yaxis_label = yaxis_label.replace('generator','fid')
# #                 sp_envelopes[-1].SetAxisLabels(VarProps[i]['XLabel'],yaxis_label)
# #                 sp_envelopes[-1].plots[0].SetMaximum(sp_envelopes[-1].ratioplot0.GetMaximum()*2.5)
# #             else :
# #                 sp_envelopes[-1].plots[0].GetYaxis().SetRangeUser(sp_properties[i][0],sp_properties[i][1])
# #             sp_envelopes[-1].RecreateLegend(.5,.75,0.9,0.85,skip=[0])

            if ops.doCorrectionFactorWeights :
                key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'scale','all','plus1sigma')
                plus1sigma  = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
                key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'scale','all','minus1sigma')
                minus1sigma = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
                AsymmErrsToPlusMinusSigma(Scale_Envelope[i],plus1sigma,minus1sigma)
                CorrFacts = TFile('rootfiles/CorrectionFactorWeights_%s.root'%(SampleTypeClean),'update')
                CorrFacts.cd()
                if i == 'Njets' : SetNjetsBins(plus1sigma)
                if i == 'Njets' : SetNjetsBins(minus1sigma)
                #
                # sp_CFScaleEnvelopes
                #
                sp_CFScaleEnvelopes.append(PlotObject(PlotName+'_CF',[the_hists['%s, %s'%(i,ops.variations[inom])],plus1sigma,minus1sigma]))
                sp_CFScaleEnvelopes[-1].MakeRatioPlot(0,[1,2],style='MoreRatio',divide='NoErr')
                sp_CFScaleEnvelopes[-1].SetBotYaxisRange(0.8,1.2)
                sp_CFScaleEnvelopes[-1].SaveAll(can='ratio',dir='plots/%s'%(SampleTypeClean))
                #
                #
                plus1sigma.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
                minus1sigma.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
                for i in range(plus1sigma.GetNbinsX()) :
                    plus1sigma.SetBinError(i+1,0)
                    minus1sigma.SetBinError(i+1,0)
                plus1sigma.Write()
                minus1sigma.Write()
                CorrFacts.Close()



    #
    # PDF variations and eigenvectors
    #
    sp_eigen = []
    sp_pdfs = []
    Env_Eigens = dict()
    PDF_Envelope = dict()
    CT10_Quadrature = dict()
    if ops.doPDFVariations :
        print 'Running pdf/eigen variations...'
        v = ops.variations[inom]
        pdfvariations = list(range(10801,10853))
        if ops.ShortcutEigenvectors : 
            pdfvariations = list(range(10801,10803))
        pdf_mstw_nnpd = ['weight_mstw','weight_nnpd']
        for p in pdfvariations+pdf_mstw_nnpd :
            print ' -- %s'%p
            f = GetFile('var/out/hadded/%s.root'%v)
            e = f.Get('EvtTree')
            e.AddFriend('WeightTree','var/out/hadded/%s_weights.root'%v)
            # Get total number of events

            #
            # Multiplied by the pdf weight
            #
            if 'weight' in str(p) : # for nnpdf
                weight_str = '%s'%(p) 
            else :
                #weight_str = 'EvtTree.weight*WeightTree.w_%d'%(p)
                weight_str = 'WeightTree.w_%d'%(p)

            for i in sorted(ops.Variables) :
                key = '%s, %s %s'%(i,v,p)
                the_hists[key] = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
                the_hists[key].SetDirectory(0)

                h1 = GetMyPlot(e
                               ,VarProps[i]['MyDrawStr'] ## var name in tree
                               ,VarProps[i]['BinStr'] ## hist bins
                               ,CrossSections.get(v)
                               ,quantity=ops.quantity
                               ,weight_str=weight_str
                               )

                rebinme(h1,the_hists['%s, %s %s'%(i,v,p)])
                gROOT.ProcessLine('delete h1')

                if i == 'Njets' : SetNjetsBins(the_hists['%s, %s %s'%(i,v,p)])

                if p not in pdf_mstw_nnpd : 
                    continue

                if ops.quantity == 'eff' :
                    feff = TFile('%s_FiducialAcceptance.root'%(SampleTypeClean),'update')
                    the_hists['%s, %s %s'%(i,v,p)].Write('%s_%s_%s_FiducialAcceptance'%(SampleTypeClean,i,p))
                    feff.Close()

                if ops.doCorrectionFactorWeights :
                    CorrFacts = TFile('rootfiles/CorrectionFactorWeights_%s.root'%(SampleTypeClean),'update')
                    CorrFacts.cd()
                    #print i,p
                    tmp = the_hists['%s, %s %s'%(i,v,p)].Clone()
                    key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'pdf','all',p)
                    tmp.SetName(key)
                    if i == 'Njets' : SetNjetsBins(tmp)
                    tmp.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
                    for x in range(tmp.GetNbinsX()) :
                        tmp.SetBinError(x+1,0)
                        tmp.SetBinError(x+1,0)
                    tmp.Write()
                    CorrFacts.Close()

            ## variables
            # Close file.
            f.Close()
        ## pdf variations (eigen, mstw, nnpd)
        
        ##
        ## ct10 quadrature, pdf envelope
        ##
        for i in sorted(ops.Variables) :
            CT10_Quadrature[i] = eigenvectorQuadrature(the_hists # dictionary from which to pull
                                                  ,'%s, %s'%(i,ops.variations[inom]) # base name
                                                  ,the_hists['%s, %s'%(i,ops.variations[inom])] # nominal hist
                                                  ,Type='CT10_90cl',eigens=pdfvariations)

            PDF_Envelope[i] = envelope(the_hists                                         # dictionary from which to pull
                                   ,list('%s, %s %s'%(i,v,p) for p in pdf_mstw_nnpd) # list of variations to take from dict
                                   ,the_hists['%s, %s'%(i,ops.variations[inom])]            # nominal hist
                                   )

            OutputFile = TFile('rootfiles/Predictions_%s.root'%(SampleTypeClean),'update')
            PlotName = 'Higgs %s %s CT10 Quadrature'%(i,SampleType)
            CT10_Quadrature[i].Write(CleanNameForMacro(PlotName))
            PlotName = 'Higgs %s %s PDF Envelope'%(i,SampleType)
            PDF_Envelope[i].Write(CleanNameForMacro(PlotName))
            OutputFile.Close()

        ##
        ## Make combination of eigen and pdf
        ##
        for i in sorted(ops.Variables) :
            Combined_Pdfs = QuadratureUpDown(PDF_Envelope[i].GetName()+' Total Error',asymlist=[PDF_Envelope[i],CT10_Quadrature[i]])
            OutputFile = TFile('rootfiles/Predictions_%s.root'%(SampleTypeClean),'update')
            PlotName = 'Higgs %s %s Combined PDF Envelope'%(i,SampleType)
            Combined_Pdfs.Write(CleanNameForMacro(PlotName))
            OutputFile.Close()

        ##
        ## Plot eigenvector variations
        ##
        for i in sorted(ops.Variables) :
            PlotName = 'Higgs %s %s EigenVar'%(i,SampleType)
            the_hists['%s, %s'%(i,v)].SetName('CT10 (Nominal)')
            for p in [pdfvariations[0]] : 
                the_hists['%s, %s %s'%(i,v,p)].SetName('Eigenvector Variations')
            #print 'making another plot object for',i,v
            sp_eigen.append(PlotObject(PlotName,[the_hists['%s, %s'%(i,v)]]+list(the_hists['%s, %s %s'%(i,v,p)] for p in pdfvariations)))
            for j in range(len(pdfvariations)) :
                sp_eigen[-1].plots[j+1].SetLineColor(kAzure-2)
                sp_eigen[-1].plots[j+1].SetMarkerColor(kAzure-2)
            sp_eigen[-1].SetAxisLabels(VarProps[i]['XLabel'],VarProps[i]['YLabel'])
            sp_eigen[-1].plots[0].SetMinimum(0)
            sp_eigen[-1].RecreateLegend(.35,.70,.95,.9,skip=list(range(2,100)))
            sp_eigen[-1].MakeRatioPlot(0,list(range(1,len(sp_eigen[-1].plots))),style='DiffXsec' if not ops.doCorrectionFactorWeights else 'MoreRatio',divide='B')
            if ops.doCorrectionFactorWeights :
                sp_eigen[-1].SetTopYaxisRange(0,sp_eigen[-1].ratioplot0.GetMaximum()*1.3)
                sp_eigen[-1].SetBotYaxisRange(0.9,1.1)
            else :
                sp_eigen[-1].SetTopYaxisRange(VarProps[i]['HistRange' ][0],VarProps[i]['HistRange' ][1])
                sp_eigen[-1].SetBotYaxisRange(VarProps[i]['RatioRange'][0],VarProps[i]['RatioRange'][1])
            sp_eigen[-1].RatioPadTop.cd()
            sp_eigen[-1].RatioTopPlot0.Draw('E1sames')

            if i == 'Njets' : SetNjetsBins(sp_eigen[-1].plots[0])

            ##
            ## Now plot pdfs (mstw/nnpd)
            ##
            PlotName = 'Higgs %s %s PDFVar'%(i,SampleType)
            for p in pdf_mstw_nnpd :
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('_1_1',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('ggH',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('minlo_HJ_mH125',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('minlo_HJJ_mH125',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace(i+', ',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('weight_',''))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('mstw','MSTW2008'))
                the_hists['%s, %s %s'%(i,v,p)].SetName(the_hists['%s, %s %s'%(i,v,p)].GetName().replace('nnpd','NNPDF2.3'))

            #print 'making another (nnpd/mstw) plot object for',i,v
            sp_pdfs.append(PlotObject(PlotName,[the_hists['%s, %s'%(i,v)]]+list(the_hists['%s, %s %s'%(i,v,p)] for p in pdf_mstw_nnpd)))
            sp_pdfs[-1].SetAxisLabels(VarProps[i]['XLabel'],VarProps[i]['YLabel'])
            sp_pdfs[-1].plots[0].SetMinimum(0)
            sp_pdfs[-1].RecreateLegend(.5,.65,.9,.9)
            sp_pdfs[-1].MakeRatioPlot(0,list(range(1,len(sp_pdfs[-1].plots))),style='DiffXsec' if not ops.doCorrectionFactorWeights else 'MoreRatio',divide='B')
            if ops.doCorrectionFactorWeights :
                sp_pdfs[-1].SetTopYaxisRange(0,sp_pdfs[-1].ratioplot0.GetMaximum()*1.3)
                sp_pdfs[-1].SetBotYaxisRange(0.9,1.1)
            else :
                sp_pdfs[-1].SetTopYaxisRange(VarProps[i]['HistRange' ][0],VarProps[i]['HistRange' ][1])
                sp_pdfs[-1].SetBotYaxisRange(VarProps[i]['RatioRange'][0],VarProps[i]['RatioRange'][1])

            if i == 'Njets' : SetNjetsBins(sp_pdfs[-1].plots[0])

            if ops.doCorrectionFactorWeights : 
                sp_eigen[-1].can.SetName('CorrectionFactor_'+sp_eigen[-1].can.GetName())
                sp_pdfs[-1].can.SetName('CorrectionFactor_'+sp_pdfs[-1].can.GetName())


            sp_eigen[-1].SaveAll(can='ratio',dir='plots/%s'%(SampleTypeClean))
            sp_pdfs[-1].SaveAll(can='ratio',dir='plots/%s'%(SampleTypeClean))

    if ops.doScaleVariations and ops.doPrintUncertainties :
        for i in sorted(ops.Variables) :
            print 'TABLE: %s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'%i
            print 'Bins &',
            txt = ''
            frac_den = []
            total_unc_up_sq = []
            total_unc_dn_sq = []
            for j in range(Scale_Envelope[i].GetN()) :
                txt += '%2.4f & '%Scale_Envelope[i].GetX()[j]
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'Diff xsec & '.rjust(15),
            for j in range(Scale_Envelope[i].GetN()) :
                txt += '%2.4f & '%Scale_Envelope[i].GetY()[j]
                frac_den.append(Scale_Envelope[i].GetY()[j])
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'MC stat & '.rjust(15),
            for j in range(Scale_Envelope[i].GetN()) :
                val = the_hists['%s, %s'%(i,ops.variations[inom])].GetBinError(j+1)
                total_unc_up_sq.append(math.pow(val,2))
                total_unc_dn_sq.append(math.pow(val,2))
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'scale up & '.rjust(15),
            for j in range(Scale_Envelope[i].GetN()) :
                val = Scale_Envelope[i].GetEYhigh()[j]
                total_unc_up_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'scale down & '.rjust(15),
            for j in range(Scale_Envelope[i].GetN()) :
                val = Scale_Envelope[i].GetEYlow()[j]
                total_unc_dn_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'PDF choice up & '.rjust(15),
            for j in range(PDF_Envelope[i].GetN()) :
                val = PDF_Envelope[i].GetEYhigh()[j] ########################################## FIX
                total_unc_up_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'PDF choice down & '.rjust(15),
            for j in range(PDF_Envelope[i].GetN()) :
                val = PDF_Envelope[i].GetEYlow()[j] ########################################## FIX
                total_unc_dn_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'CT10 Eigen up & '.rjust(15),
            for j in range(CT10_Quadrature[i].GetN()) :
                val = CT10_Quadrature[i].GetEYhigh()[j] ########################################## FIX
                total_unc_up_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'CT10 Eigen dn & '.rjust(15),
            for j in range(CT10_Quadrature[i].GetN()) :
                val = CT10_Quadrature[i].GetEYlow()[j] ########################################## FIX
                total_unc_dn_sq[j] += math.pow(val,2)
                txt += '%2.1f\\%% & '%(100.*val/float(frac_den[j]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'Total err up & '.rjust(15),
            for k in range(len(total_unc_up_sq)) :
                txt += '%2.1f\\%% & '%(100*math.sqrt(total_unc_up_sq[k])/float(frac_den[k]))
            print txt.rstrip(' &')+' \\\\';txt = '';
            print 'Total err dn & '.rjust(15),
            for k in range(len(total_unc_dn_sq)) :
                txt += '%2.1f\\%% & '%(100*math.sqrt(total_unc_dn_sq[k])/float(frac_den[k]))
            print txt.rstrip(' &')+' \\\\';txt = '';

    ##
    ## Compute flat uncertainties
    ## 
    if ops.flat :
        print 'Getting flat uncertainties ...'
        OutputFile = TFile('rootfiles/Predictions_%s.root'%(SampleTypeClean),'update')
        for i in sorted(ops.Variables) :
            ##
            ## scale
            ##
            scaleup = 0.01*CrossSections_Errors[ops.variations[inom]]['QCD_Up']
            scaledn = 0.01*CrossSections_Errors[ops.variations[inom]]['QCD_Dn']
            Scale_Flat_Envelope = FlatErrorToAsymmErrs(the_hists['%s, %s'%(i,ops.variations[inom])].GetName()+' Scale Flat Envelope'
                                                       ,the_hists['%s, %s'%(i,ops.variations[inom])],up_frac=scaleup,dn_frac=scaledn)
            PlotName = 'Higgs %s %s Flat Scale Envelope'%(i,SampleType)
            OutputFile.cd()
            Scale_Flat_Envelope.Write(CleanNameForMacro(PlotName))
            ##
            ## pdf/alphas 
            ##
            pdfup = 0.01*CrossSections_Errors[ops.variations[inom]]['PDF_Up']
            pdfdn = 0.01*CrossSections_Errors[ops.variations[inom]]['PDF_Dn']
            PDF_Flat_Envelope = FlatErrorToAsymmErrs(the_hists['%s, %s'%(i,ops.variations[inom])].GetName()+' PDF Flat Envelope'
                                                     ,the_hists['%s, %s'%(i,ops.variations[inom])],up_frac=pdfup,dn_frac=pdfdn)
            PlotName = 'Higgs %s %s Flat Combined PDF Envelope'%(i,SampleType)
            OutputFile.cd()
            PDF_Flat_Envelope.Write(CleanNameForMacro(PlotName))
        OutputFile.Close()
    ##
    ##
    ##

    sp_PDF_CF = []
    if ops.doCorrectionFactorWeights :
        for i in sorted(ops.Variables) :
            ##
            ## Plus-minus sigma for pdf
            ##
            key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'pdf','all','plus1sigma')
            plus1sigma  = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
            key = '%s_%s_%s_%s'%(VarProps[i]['JonNaming'],'pdf','all','minus1sigma')
            minus1sigma = TH1F(key,key,len(VarProps[i]['Bins'])-1,array('d',VarProps[i]['Bins']))
            AsymmErrsToPlusMinusSigma(PDF_Envelope[i],plus1sigma,minus1sigma)
            CorrFacts = TFile('rootfiles/CorrectionFactorWeights_%s.root'%(SampleTypeClean),'update')
            
            ##
            ## sp_PDF_CF
            ##
            PlotName = 'Higgs %s %s PDFVar'%(i,SampleType)
            sp_PDF_CF.append(PlotObject(PlotName+'_CF',[the_hists['%s, %s'%(i,ops.variations[inom])],plus1sigma,minus1sigma]))
            sp_PDF_CF[-1].MakeRatioPlot(0,[1,2],style='MoreRatio',divide='NoErr')
            sp_PDF_CF[-1].SetBotYaxisRange(0.9,1.1)
            sp_PDF_CF[-1].SaveAll(can='ratio',dir='plots/%s'%(SampleTypeClean))
            #
            #
            if i == 'Njets' : SetNjetsBins(plus1sigma)
            if i == 'Njets' : SetNjetsBins(minus1sigma)
            plus1sigma.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
            minus1sigma.Divide(the_hists['%s, %s'%(i,ops.variations[inom])])
            for i in range(plus1sigma.GetNbinsX()) :
                plus1sigma.SetBinError(i+1,0)
                minus1sigma.SetBinError(i+1,0)
            CorrFacts.cd()
            plus1sigma.Write()
            minus1sigma.Write()
            CorrFacts.Close()
    print 'done.'

if __name__ == "__main__":
    from optparse import OptionParser
    p = OptionParser()
    
    ##
    p.add_option('--process',type='string',default='ggh' ,dest='process',help='variations: ggh, ggh_hfact, tth, wh, zh, vbf, hj, hjj')
    p.add_option('--vars'   ,type='string',default='all' ,dest='vars'   ,help='vars: pt,rap,cth,njets,jetpt,m34')
    p.add_option('--quantity',type='string',default='diff' ,dest='quantity'   ,help='quantity: diff (differential), gen, fid, eff (fiducial efficiency)')

    p.add_option('--debug'    ,action='store_true',default=False,dest='debug'   ,help='debug hists with minitrees')
    ## p.add_option('--debugfid' ,action='store_true',default=False,dest='debugfid',help='debug fiducial hists')
    p.add_option('--scale'    ,action='store_true',default=False,dest='scale',help='do scale variations')
    p.add_option('--pdf'      ,action='store_true',default=False,dest='pdf',help='do pdf variations')
    p.add_option('--cf'       ,action='store_true',default=False,dest='cf',help='make cf weights')

    p.add_option('--flat'     ,action='store_true',default=False,dest='flat',help='Compute flat errors')

    p.add_option('--noshape' ,action='store_true',default=False,dest='noshape',help='do shape+norm')
    p.add_option('--eigen'   ,action='store_true',default=False,dest='eigen',help='run eigenvector')

    (ops,args) = p.parse_args()

    ## 
    ## No capitalization!
    ## 
    ops.variations = {'ggh_hfact':['ggH_hfact_1_1']
                      ,'ggh'      :['ggH_1_1']
                      ,'tth'      :['ttH_1_1']
                      ,'wh'       :['WH_1_1']
                      ,'zh'       :['ZH_1_1']
                      ,'vbf'      :['VBFH125_1_1']
                      ,'hj'       :['minlo_HJ_mH125_1_1']
                      ,'hjj'      :['minlo_HJJ_mH125_1_1']
                      }.get(ops.process)

    ops.Variables = ops.vars
    print ops.Variables
    if ops.Variables == 'all' : 
        ops.Variables = 'pt,rap,cth,njets,jetpt,m34'
    ##ops.Variables = ops.Variables.replace('pt','pt')
    ops.Variables = ops.Variables.replace('rap','Rapidity')
    ops.Variables = ops.Variables.replace('jetpt','jet1pt')
    ##ops.Variables = ops.Variables.replace('m34','m34')
    ops.Variables = ops.Variables.replace('njets','Njets')
    ops.Variables = ops.Variables.replace('cth','cthstr')
    ops.Variables = ops.Variables.split(',')

    print ops.Variables

    ops.doPrintUncertainties = False
    ops.doCombine            = False

    ops.doScaleVariations     = ops.scale
    ops.doPDFVariations       = ops.pdf

    ops.doShapeVariations     = not ops.noshape
    ops.ShortcutEigenvectors  = not ops.eigen

    ops.doDebug               = ops.debug

#     ops.doDifferential         = (ops.quantity == 'diff')
#     ops.doGenerator            = (ops.quantity == 'gen')
#     ops.doFiducial             = (ops.quantity == 'fid')
#     ops.doFiducialEfficiency   = (ops.quantity == 'eff')

    ops.doCorrectionFactorWeights = ops.cf

    if ops.cf :
        ops.quantity             = 'gen'
        ops.variations           = ['ggH_hfact_1_1']
        ops.doScaleVariations    = True
        ops.doPDFVariations      = True
        ops.doShapeVariations    = True
        ops.doCombine            = False
        ops.ShortcutEigenvectors = True

    if ops.doPDFVariations and ops.doScaleVariations and not ops.ShortcutEigenvectors :
        ops.doCombine = True
        ops.doPrintUncertainties = True

    if ops.doScaleVariations :
        scale_vars = ['0.5_0.5','1_0.5','0.5_1','1_1','2_1','1_2','2_2']
        base = ops.variations[0].replace('_1_1','')
        ops.variations = list('%s_%s'%(base,a) for a in scale_vars)

    print ops.variations

    main(ops,args)
