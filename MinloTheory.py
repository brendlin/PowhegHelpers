import math
from array import array
from ROOT import TGraphAsymmErrors

def IntegralOfDifferentialHist(hist) :
    integral = 0
    for i in range(hist.GetNbinsX()) :
        #print 'integral +=',hist.GetBinContent(i+1),'*',hist.GetBinWidth(i+1)
        integral += hist.GetBinContent(i+1)*hist.GetBinWidth(i+1)
    #print 'integral:',integral
    return integral

def envelope(thedict,thelist,nominal) :
    #
    # Takes the nominal and makes an envelope around it
    #
    diff_up = nominal.Clone()
    key = 'diff_up'
    diff_up.SetNameTitle(key,key)
    diff_dn = nominal.Clone()
    key = 'diff_dn'
    diff_dn.SetNameTitle(key,key)
    for i in range(diff_up.GetNbinsX()) :
        diff_up.SetBinContent(i+1,0)
        diff_dn.SetBinContent(i+1,0)
    #
    for var in thelist :
        if var == 'dummy' : continue
        for i in range(nominal.GetNbinsX()) :
            curr_diff_up = diff_up.GetBinContent(i+1)
            curr_diff_dn = diff_dn.GetBinContent(i+1)
            nominal_bc   = nominal.GetBinContent(i+1)
            thisvar_bc   = thedict[var].GetBinContent(i+1)
            diff_up.SetBinContent(i+1,max(curr_diff_up,thisvar_bc-nominal_bc))
            diff_dn.SetBinContent(i+1,min(curr_diff_dn,thisvar_bc-nominal_bc))
            
    nbins = nominal.GetNbinsX()
    x   = array('d',list(nominal.GetBinCenter (a+1)     for a in range(nominal.GetNbinsX())))
    xup = array('d',list(nominal.GetBinWidth  (a+1)/2.  for a in range(nominal.GetNbinsX())))
    xdn = array('d',list(nominal.GetBinWidth  (a+1)/2.  for a in range(nominal.GetNbinsX())))
    y   = array('d',list(nominal.GetBinContent(a+1)     for a in range(nominal.GetNbinsX())))
    yup = array('d',list(diff_up.GetBinContent(a+1)     for a in range(nominal.GetNbinsX())))
    ydn = array('d',list(diff_dn.GetBinContent(a+1)*-1. for a in range(nominal.GetNbinsX())))
    result = TGraphAsymmErrors(nbins,x,y,xdn,xup,ydn,yup)
    result.GetXaxis().SetTitle(nominal.GetXaxis().GetTitle())
    result.GetYaxis().SetTitle(nominal.GetYaxis().GetTitle())
    result.SetLineWidth(2)
    result.SetName(nominal.GetName()+' Envelope')
    return result

def ConvertNeventsToDSigma(h) :
    for i in range(h.GetNbinsX()) :
        orig   = h.GetBinContent(i+1)
        orig_e = h.GetBinError(i+1)
        bin_width = h.GetBinLowEdge(i+2)-h.GetBinLowEdge(i+1)
        #print 'divide bin',i+1,'by',bin_width
        h.SetBinContent(i+1,orig/float(bin_width))
        h.SetBinError(i+1,orig_e/float(bin_width))

def NameConvert(the_hist) :
    the_str = the_hist.GetName()
    if 'ggH' in the_str :
        the_str = the_str.replace('_0.5_0.5','R_{dn}, F_{dn}'  )
        the_str = the_str.replace('_0.5_1'  ,'R_{nom}, F_{dn}' )
        the_str = the_str.replace('_1_0.5'  ,'R_{dn}, F_{nom}' )
        the_str = the_str.replace('_1_1'    ,'R_{nom}, F_{nom}')
        the_str = the_str.replace('_1_2'    ,'R_{up}, F_{nom}' )
        the_str = the_str.replace('_2_1'    ,'R_{nom}, F_{up}' )
        the_str = the_str.replace('_2_2'    ,'R_{up}, F_{up}'  )
    else :
        the_str = the_str.replace('_0.5_0.5','R_{dn}, F_{dn}'  )
        the_str = the_str.replace('_0.5_1'  ,'R_{dn}, F_{nom}' )
        the_str = the_str.replace('_1_0.5'  ,'R_{nom}, F_{dn}' )
        the_str = the_str.replace('_1_1'    ,'R_{nom}, F_{nom}')
        the_str = the_str.replace('_1_2'    ,'R_{nom}, F_{up}' )
        the_str = the_str.replace('_2_1'    ,'R_{up}, F_{nom}' )
        the_str = the_str.replace('_2_2'    ,'R_{up}, F_{up}'  )
    the_hist.SetName(the_str)
    return

def GetVariationName(the_hist) :
    name = the_hist.GetName()
    if 'R_{dn}, F_{dn}'   in name : return 'RDownFDown'
    if 'R_{nom}, F_{dn}'  in name : return 'RNomFDown' 
    if 'R_{dn}, F_{nom}'  in name : return 'RDownFNom' 
    if 'R_{nom}, F_{nom}' in name : return 'RNomFNom'  
    if 'R_{up}, F_{nom}'  in name : return 'RUpFNom'   
    if 'R_{nom}, F_{up}'  in name : return 'RNomFUp'   
    if 'R_{up}, F_{up}'   in name : return 'RUpFUp'    
    return 'UNKNOWN'

def AsymmErrsToPlusMinusSigma(asymm,up,dn) :
    for i in range(asymm.GetN()) :
        up.SetBinContent(i+1,asymm.GetY()[i]+asymm.GetEYhigh()[i])
        dn.SetBinContent(i+1,asymm.GetY()[i]-asymm.GetEYlow()[i])
        up.SetBinError(i+1,0)
        dn.SetBinError(i+1,0)
    return

def HistToAsymmErrs(name,hist) :
    X      = []
    EXlow  = []
    EXhigh = []
    Y      = []
    EYlow  = []
    EYhigh = []
    for i in range(hist.GetNbinsX()) :
        X     .append(hist.GetBinCenter (i+1))
        EXlow .append(hist.GetBinWidth  (i+1)/2.)
        EXhigh.append(hist.GetBinWidth  (i+1)/2.)
        Y     .append(hist.GetBinContent(i+1))
        EYlow .append(hist.GetBinError  (i+1))
        EYhigh.append(hist.GetBinError  (i+1))
    a_X      = array('d',X      )
    a_EXlow  = array('d',EXlow  )
    a_EXhigh = array('d',EXhigh )
    a_Y      = array('d',Y      )
    a_EYlow  = array('d',EYlow  )
    a_EYhigh = array('d',EYhigh )
    asymm = TGraphAsymmErrors(len(a_X),a_X,a_Y,a_EXlow,a_EXhigh,a_EYlow,a_EYhigh)
    asymm.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    asymm.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    asymm.SetLineWidth(2)
    asymm.SetName(name)
    return asymm    

def FlatErrorToAsymmErrs(name,nomhist,up_frac=0.,dn_frac=0.) :
    nom_2_asymm = HistToAsymmErrs(nomhist.GetName()+' FlatErrorToAsymmErrs Asymm',nomhist)
    EYlow  = []
    EYhigh = []
    for i in range(nom_2_asymm.GetN()) :
        EYlow.append(nom_2_asymm.GetY()[i]*dn_frac)
        EYhigh.append(nom_2_asymm.GetY()[i]*up_frac)
    a_EYlow  = array('d',EYlow  )
    a_EYhigh = array('d',EYhigh )    
    result = TGraphAsymmErrors(nom_2_asymm.GetN(),nom_2_asymm.GetX(),nom_2_asymm.GetY()
                               ,nom_2_asymm.GetEXlow(),nom_2_asymm.GetEXhigh()
                               ,a_EYlow,a_EYhigh)
    result.GetXaxis().SetTitle(nom_2_asymm.GetXaxis().GetTitle())
    result.GetYaxis().SetTitle(nom_2_asymm.GetYaxis().GetTitle())
    result.SetLineWidth(2)
    result.SetName(name)
    return result

def LinearUpDown(name,asymlist=[],hists=[],AddHists=False) :
    for i in range(len(hists)) :
        asymlist.append(HistToAsymmErrs(hists[i].GetName()+' LinearUpDown Asymm',hists[i]))

    nbins = asymlist[0].GetN()
    total_unc_up = []
    total_unc_dn = []
    for i in range(nbins) :
        total_unc_up.append(0)
        total_unc_dn.append(0)
    #
    # asym err hists
    #
    for i in range(nbins) :
        for j in range(len(asymlist)) :
            total_unc_up[i] += asymlist[j].GetEYhigh()[i]
            total_unc_dn[i] += asymlist[j].GetEYlow()[i]

    y = []
    for i in range(nbins) :
        y.append(asymlist[0].GetY()[i])
        if AddHists :
            for j in range(1,len(asymlist)) :
                y[-1] += asymlist[j].GetY()[i]

    ybincontent = array('d',y)
    yup = array('d',total_unc_up)
    ydn = array('d',total_unc_dn)
    result = TGraphAsymmErrors(asymlist[0].GetN(),asymlist[0].GetX(),ybincontent
                               ,asymlist[0].GetEXlow(),asymlist[0].GetEXhigh()
                               ,ydn,yup)
    result.GetXaxis().SetTitle(asymlist[0].GetXaxis().GetTitle())
    result.GetYaxis().SetTitle(asymlist[0].GetYaxis().GetTitle())
    result.SetLineWidth(2)
    result.SetName(name)
    return result
        
    return

def QuadratureUpDown(name,asymlist=[],hists=[],AddHists=False) : # These are TGraphAsymmErrors
    asymlist1 = []
    for i in asymlist :
        asymlist1.append(i)
    for i in range(len(hists)) :
        asymlist1.append(HistToAsymmErrs(hists[i].GetName()+' QuadratureUpDown Asymm',hists[i]))
    nbins = asymlist1[0].GetN()
    total_unc_up_sq = []
    total_unc_dn_sq = []
    for i in range(nbins) :
        total_unc_up_sq.append(0)
        total_unc_dn_sq.append(0)
    #
    # asym err hists
    #
    for i in range(nbins) :
        for j in range(len(asymlist1)) :
            E_up = asymlist1[j].GetEYhigh()[i]
            E_dn = asymlist1[j].GetEYlow()[i]
            total_unc_up_sq[i] += math.pow(E_up,2)
            total_unc_dn_sq[i] += math.pow(E_dn,2)
#     #
#     # hists
#     #
#     for i in range(nbins) :
#         for j in range(len(hists)) :
#             E_up = hists[j].GetBinError(i+1)
#             E_dn = hists[j].GetBinError(i+1)
#             total_unc_up_sq[i] += math.pow(E_up,2)
#             total_unc_dn_sq[i] += math.pow(E_dn,2)
    #
    # sqrt
    #
    for i in range(nbins) :
        total_unc_up_sq[i] = math.sqrt(total_unc_up_sq[i])
        total_unc_dn_sq[i] = math.sqrt(total_unc_dn_sq[i])

    y = []
    for i in range(nbins) :
        y.append(asymlist1[0].GetY()[i])
        if AddHists :
            for j in range(1,len(asymlist1)) :
                y[-1] += asymlist1[j].GetY()[i]

    ybincontent = array('d',y)
    yup = array('d',total_unc_up_sq)
    ydn = array('d',total_unc_dn_sq)
    result = TGraphAsymmErrors(asymlist1[0].GetN(),asymlist1[0].GetX(),ybincontent
                               ,asymlist1[0].GetEXlow(),asymlist1[0].GetEXhigh()
                               ,ydn,yup)
    result.GetXaxis().SetTitle(asymlist1[0].GetXaxis().GetTitle())
    result.GetYaxis().SetTitle(asymlist1[0].GetYaxis().GetTitle())
    result.SetLineWidth(2)
    result.SetName(name)
    return result


def eigenvectorQuadrature(thedict,thebase,nominal,Type='MSTW_68cl',eigens=[]) :
    # SOME CLs are 90%; convert to 1sigma by 1/1.64485
    #
    # Takes the nominal and finds the error from the eigenvectors
    #
    diff_up_squared = nominal.Clone()
    key = 'diff_up_squared'
    diff_up_squared.SetNameTitle(key,key)
    diff_dn_squared = nominal.Clone()
    key = 'diff_dn_squared'
    diff_dn_squared.SetNameTitle(key,key)
    for i in range(diff_up_squared.GetNbinsX()) :
        diff_up_squared.SetBinContent(i+1,0)
        diff_dn_squared.SetBinContent(i+1,0)
    #
    neigens = 20
    if Type == 'CT10_90cl' :
        neigens = 26
    for ev in range(neigens) :
        for i in range(nominal.GetNbinsX()) :
            nom       = nominal.GetBinContent(i+1)
            if Type == 'CT10_90cl' and (10800+2*ev+1 not in eigens or 10800+2*ev+2 not in eigens) :
                continue
#             if Type == 'MSTW_90cl' :
#                 cl_scale  = float(1.64485)
#                 upeigen   = thedict[thebase.replace('P1','P1%02d'%(2*ev+1))].GetBinContent(i+1)
#                 dneigen   = thedict[thebase.replace('P1','P1%02d'%(2*ev+2))].GetBinContent(i+1)
            elif Type == 'MSTW_68cl' :
                cl_scale  = float(1.)
                upeigen   = thedict[thebase.replace('P1','P1%02d'%(2*ev+1))].GetBinContent(i+1)
                dneigen   = thedict[thebase.replace('P1','P1%02d'%(2*ev+2))].GetBinContent(i+1)
            elif Type == 'CT10_90cl' :
                cl_scale  = float(1.64485)
                upeigen   = thedict[thebase+' %s'%(10800+2*ev+1)].GetBinContent(i+1)
                dneigen   = thedict[thebase+' %s'%(10800+2*ev+2)].GetBinContent(i+1)                
            else :
                print 'ERROR IN EIGENVALUE CALCULATION!'
            diff_up_squared.AddBinContent(i+1,pow(max(upeigen-nom,dneigen-nom,0),2))
            diff_dn_squared.AddBinContent(i+1,pow(max(nom-upeigen,nom-dneigen,0),2))

    nbins = nominal.GetNbinsX()
    x   = array('d',list(nominal.GetBinCenter (a+1)     for a in range(nominal.GetNbinsX())))
    xup = array('d',list(nominal.GetBinWidth  (a+1)/2.  for a in range(nominal.GetNbinsX())))
    xdn = array('d',list(nominal.GetBinWidth  (a+1)/2.  for a in range(nominal.GetNbinsX())))
    y   = array('d',list(nominal.GetBinContent(a+1)     for a in range(nominal.GetNbinsX())))
    yup = array('d',list(math.sqrt(diff_up_squared.GetBinContent(a+1))/cl_scale for a in range(nominal.GetNbinsX())))
    ydn = array('d',list(math.sqrt(diff_dn_squared.GetBinContent(a+1))/cl_scale for a in range(nominal.GetNbinsX())))
    result = TGraphAsymmErrors(nbins,x,y,xdn,xup,ydn,yup)
    return result

def rebinme(hfine,hcoarse) :
    for i in range(hcoarse.GetNbinsX()) :
        total = 0
        error = 0
        error2 = 0
        ##### invinverror = 0
        ##### inverror2 = 0
        den = float(hcoarse.GetBinWidth(i+1))
        for j in range(hfine.GetNbinsX()) :
            #print 'bin edges: ',hfine.GetBinLowEdge(j+1),hfine.GetBinLowEdge(j+2),'?'
            #print 'against:',hcoarse.GetBinLowEdge(i+1),hcoarse.GetBinLowEdge(i+2)
            if not (hfine.GetBinLowEdge(j+2)<=hcoarse.GetBinLowEdge(i+2)+0.00001) : continue
            if not (hfine.GetBinLowEdge(j+1)>=hcoarse.GetBinLowEdge(i+1)-0.00001) : continue
            #print 'bin edges: ',hfine.GetBinLowEdge(j+1),hfine.GetBinLowEdge(j+2),'are a go'
            num = float(hfine.GetBinWidth(j+1))
            total     +=      num*hfine.GetBinContent(j+1)/den
            error2    +=     (num*hfine.GetBinError(j+1)/den)**2
            #error2    +=     (num/den)*(hfine.GetBinError(j+1))**2
            #error2    +=     (den/num)*(hfine.GetBinError(j+1))**2
            #error2    +=     (den*hfine.GetBinError(j+1)/num)**2
            #error2    +=     (hfine.GetBinError(j+1))**2
            ##### inverror2 += 1./((num*hfine.GetBinError(j+1)/den)**2)
        error = math.sqrt(error2)
        #### invinverror = 1./math.sqrt(inverror2)
        hcoarse.SetBinContent(i+1,total)
        hcoarse.SetBinError(i+1,error)

    return

class CalcCrossSec :
    def __init__(self,name) :
        self.name = name
        self.InverseWeightSquared = 0
        self.SumElementOverWeightSquared = 0

    def Reset(self) :
        self.InverseWeightSquared = 0
        self.SumElementOverWeightSquared = 0

    def GetError(self) :
        if self.InverseWeightSquared == 0 : 
            return 0.        
        return 1./float(math.sqrt(self.InverseWeightSquared))

    def GetMeasurement(self) :
        if self.InverseWeightSquared == 0 : 
            return 0.
        return self.SumElementOverWeightSquared/float(self.InverseWeightSquared)

    def AddMeasurement(self,xsec,error) :
        if xsec == 0 and error == 0 :
            return
        self.SumElementOverWeightSquared += xsec/float(math.pow(error,2))
        self.InverseWeightSquared += 1./float(math.pow(error,2))
        return
