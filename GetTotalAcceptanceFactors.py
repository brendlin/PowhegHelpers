#!/bin/python

#Written by Michaela Queitsch-Maitland, 2015

from ROOT import *
import sys, subprocess, getopt
from array import array
import math

def acc(t,weight):
    h = TH1D("h","",1,0,1)
    t.Draw("0.5>>h","PassesCuts*"+weight)
    num=h.Integral()
    den = t.Draw("0.5>>h","1.0*"+weight)
    den=h.Integral()

    return num/den

def tot_acc(iw,tggF,tVBF,tWH,tZH,tttH):
    acc_ggF = acc(tggF,"weight_"+str(iw))
    acc_VBF = acc(tVBF,"weight_"+str(iw))
    acc_WH = acc(tWH,"weight")
    acc_ZH = acc(tZH,"weight")
    acc_ttH = acc(tttH,"weight")

    sum = 0
    for xsec in xsecs:
        sum += xsec

    tot = (acc_ggF*xsecs[0]+acc_VBF*xsecs[1]+acc_WH*xsecs[2]+acc_ZH*xsecs[3]+acc_ttH*xsecs[4])/sum

    return tot

xsecs=[43.92,3.748,1.380,0.8696,0.5085]

#fggF = TFile.Open("13TeV_RelIsoCut/Hyy_PowhegPythia8_ggF.root","read")
fggF = TFile.Open("var/out/hadded/ggF_1_1_13TeV.root","read")
tggF = fggF.Get("EvtTree")

#fVBF = TFile.Open("13TeV_RelIsoCut/Hyy_PowhegPythia8_VBF.root","read")
fVBF = TFile.Open("var/out/hadded/VBF_1_1_13TeV.root","read")
tVBF = fVBF.Get("EvtTree")

#fWH = TFile.Open("13TeV_RelIsoCut/Hyy_Pythia8_WH.root","read")
fWH = TFile.Open("var/out/hadded/WH_1_1_13TeV.root","read")
tWH = fWH.Get("EvtTree")

#fZH = TFile.Open("13TeV_RelIsoCut/Hyy_Pythia8_ZH.root","read")
fZH = TFile.Open("var/out/hadded/ZH_1_1_13TeV.root","read")
tZH = fZH.Get("EvtTree")

#fttH = TFile.Open("13TeV_RelIsoCut/Hyy_Pythia8_ttH.root","read")
fttH = TFile.Open("var/out/hadded/ttH_1_1_13TeV.root","read")
tttH = fttH.Get("EvtTree")

acc_VBF = acc(tVBF,"weight_0")
acc_ggF = acc(tggF,"weight_0")
acc_WH = acc(tWH,"weight")
acc_ZH = acc(tZH,"weight")
acc_ttH = acc(tttH,"weight")

print "ggF:",acc_ggF
print "VBF:",acc_VBF
print "WH:",acc_WH
print "ZH:",acc_ZH
print "ttH:",acc_ttH

sum = 0
for xsec in xsecs:
    sum += xsec

acc_tot = (acc_ggF*xsecs[0]+acc_VBF*xsecs[1]+acc_WH*xsecs[2]+acc_ZH*xsecs[3]+acc_ttH*xsecs[4])/sum

print "total:",acc_tot
print "total:",tot_acc(0,tggF,tVBF,tWH,tZH,tttH)

xsecs=[43.92,2*3.748,2*1.380,2*0.8696,0.5085]
vh_up=100*(tot_acc(0,tggF,tVBF,tWH,tZH,tttH)-acc_tot)/acc_tot
xsecs=[43.92,0.5*3.748,0.5*1.380,0.5*0.8696,0.5085]
vh_dn=100*(tot_acc(0,tggF,tVBF,tWH,tZH,tttH)-acc_tot)/acc_tot
xsecs=[43.92,3.748,1.380,0.8696,5*0.5085]
tth_up=100*(tot_acc(0,tggF,tVBF,tWH,tZH,tttH)-acc_tot)/acc_tot
xsecs=[43.92,3.748,1.380,0.8696,0.5*0.5085]
tth_dn=100*(tot_acc(0,tggF,tVBF,tWH,tZH,tttH)-acc_tot)/acc_tot
xsecs=[43.92,3.748,1.380,0.8696,0.5085]

comp_up=0
comp_dn=0

if vh_up>0 and vh_up>comp_up:
    comp_up=vh_up
if vh_dn>0 and vh_dn>comp_up:
    comp_up=vh_dn
if tth_up>0 and tth_up>comp_up:
    comp_up=tth_up
if tth_dn>0 and tth_dn>comp_up:
    comp_up=tth_dn

if vh_up<0 and vh_up<comp_dn:
    comp_dn=vh_up
if vh_dn<0 and vh_dn<comp_dn:
    comp_dn=vh_dn
if tth_up<0 and tth_up<comp_dn:
    comp_dn=tth_up
if tth_dn<0 and tth_dn<comp_dn:
    comp_dn=tth_dn

print vh_up,vh_dn,tth_up,tth_dn
print comp_up,comp_dn

qcd_ggF = []
pdf_ggF = []

qcd=[]
pdf=[]

qcd_VBF = []
pdf_VBF = []

for i in range(1,9):
#    print "weight_100"+str(i)
    qcd_ggF.append(acc(tggF,"weight_100"+str(i)))
    qcd_VBF.append(acc(tVBF,"weight_100"+str(i)))
    qcd.append( tot_acc("100"+str(i),tggF,tVBF,tWH,tZH,tttH) )

for i in range(1,60):
#    print "weight_200"+str(i)
    if i < 10:
        pdf_ggF.append(acc(tggF,"weight_200"+str(i)))
        pdf_VBF.append(acc(tVBF,"weight_200"+str(i)))
        pdf.append( tot_acc("200"+str(i),tggF,tVBF,tWH,tZH,tttH) )
    else:
        pdf_ggF.append(acc(tggF,"weight_20"+str(i)))
        pdf_VBF.append(acc(tVBF,"weight_20"+str(i)))
        pdf.append( tot_acc("20"+str(i),tggF,tVBF,tWH,tZH,tttH) )

qcd_up_ggF = 0
qcd_dn_ggF = 0

pdf_up_ggF = 0
pdf_dn_ggF = 0

qcd_up_VBF = 0
qcd_dn_VBF = 0

pdf_up_VBF = 0
pdf_dn_VBF = 0

qcd_up_tot=0
qcd_dn_tot=0

for x in qcd:
    syst=100*(x-acc_tot)/acc_tot
    if syst > qcd_up_tot:
        qcd_up_tot = syst
    if syst < qcd_dn_tot:
        qcd_dn_tot = syst

for x in qcd_ggF:
    syst = 100*(x-acc_ggF)/acc_ggF
    if syst > qcd_up_ggF:
        qcd_up_ggF = syst
    if syst < qcd_dn_ggF:
        qcd_dn_ggF = syst

for x in qcd_VBF:
    syst = 100*(x-acc_VBF)/acc_VBF
    if syst > qcd_up_VBF:
        qcd_up_VBF = syst
    if syst < qcd_dn_VBF:
        qcd_dn_VBF = syst

print "tot QCD up:   ",qcd_up_tot
print "tot QCD down: ",qcd_dn_tot

print "ggF QCD up:   ",qcd_up_ggF
print "ggF QCD down: ",qcd_dn_ggF

print "VBF QCD up:   ",qcd_up_VBF
print "VBF QCD down: ",qcd_dn_VBF

hessian_pdf_ggF = [0,0]
hessian_pdf_VBF = [0,0]
other_pdf_ggF = [0,0]
other_pdf_VBF = [0,0]

hessian_pdf_tot=[0,0]
other_pdf_tot=[0,0]

up=0
dn=0

# hessian combination of uncertainties using adjacent variations as pairs
for ivar in range(1,56,2):
#    print ivar
#    print ivar+1

    xip = pdf_ggF[ivar]-acc_ggF
    xim = pdf_ggF[ivar+1]-acc_ggF
    up += pow(max(0,xip,xim),2)
    dn += pow(max(0,-xip,-xim),2)

for ivar in [58,59]:
    if pdf_ggF[ivar-1]>acc_ggF and (100*(pdf_ggF[ivar-1]-acc_ggF)/acc_ggF)>other_pdf_ggF[0]:
        other_pdf_ggF[0] = 100*(pdf_ggF[ivar-1]-acc_ggF)/acc_ggF
    elif (100*(pdf_ggF[ivar-1]-acc_ggF)/acc_ggF)<other_pdf_ggF[1]:
        other_pdf_ggF[1] = 100*(pdf_ggF[ivar-1]-acc_ggF)/acc_ggF

    if pdf_VBF[ivar-1]>acc_VBF and (100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF)>other_pdf_VBF[0]:
        other_pdf_VBF[0] = 100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF
    elif (100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF)<other_pdf_VBF[1]:
        other_pdf_VBF[1] = 100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF

    if pdf[ivar-1]>acc_tot and (100*(pdf[ivar-1]-acc_tot)/acc_tot)>other_pdf_tot[0]:
        other_pdf_tot[0] = 100*(pdf[ivar-1]-acc_tot)/acc_tot
    elif (100*(pdf[ivar-1]-acc_tot)/acc_tot)<other_pdf_tot[1]:
        other_pdf_tot[1] = 100*(pdf[ivar-1]-acc_tot)/acc_tot

up = math.sqrt(up)/acc_ggF
dn = math.sqrt(dn)/acc_ggF

hessian_pdf_ggF[0] = up*100/1.642
hessian_pdf_ggF[1] = dn*100/1.642

up=0
dn=0

# hessian combination of uncertainties using adjacent variations as pairs
for ivar in range(1,56,2):
#    print ivar
#    print ivar+1

    xip = pdf_VBF[ivar]-acc_VBF
    xim = pdf_VBF[ivar+1]-acc_VBF
    up += pow(max(0,xip,xim),2)
    dn += pow(max(0,-xip,-xim),2)

up = math.sqrt(up)/acc_VBF
dn = math.sqrt(dn)/acc_VBF

hessian_pdf_VBF[0] = up*100/1.642
hessian_pdf_VBF[1] = dn*100/1.642

up=0
dn=0

# hessian combination of uncertainties using adjacent variations as pairs
for ivar in range(1,56,2):
#    print ivar
#    print ivar+1

    xip = pdf[ivar]-acc_tot
    xim = pdf[ivar+1]-acc_tot
    up += pow(max(0,xip,xim),2)
    dn += pow(max(0,-xip,-xim),2)

for ivar in [58,59]:
    if pdf[ivar-1]>acc_tot and (100*(pdf[ivar-1]-acc_tot)/acc_tot)>other_pdf_tot[0]:
        other_pdf_tot[0] = 100*(pdf[ivar-1]-acc_tot)/acc_tot
    elif (100*(pdf[ivar-1]-acc_tot)/acc_tot)<other_pdf_tot[1]:
        other_pdf_tot[1] = 100*(pdf[ivar-1]-acc_tot)/acc_tot

    if pdf_VBF[ivar-1]>acc_VBF and (100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF)>other_pdf_VBF[0]:
        other_pdf_VBF[0] = 100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF
    elif (100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF)<other_pdf_VBF[1]:
        other_pdf_VBF[1] = 100*(pdf_VBF[ivar-1]-acc_VBF)/acc_VBF

up = math.sqrt(up)/acc_tot
dn = math.sqrt(dn)/acc_tot

hessian_pdf_tot[0] = up*100/1.642
hessian_pdf_tot[1] = dn*100/1.642

#for pdf in pdf_ggF:
#    syst = 100*(pdf-acc_ggF)/acc_ggF
#    print "ggF pdf: ",syst
#    if syst > pdf_up_ggF:
#        pdf_up_ggF = syst
#    if syst < pdf_dn_ggF:
#        pdf_dn_ggF = syst

#for pdf in pdf_VBF:
#    syst = 100*(pdf-acc_VBF)/acc_VBF
#    print "VBF pdf: ",syst
#    if syst > pdf_up_VBF:
#        pdf_up_VBF = syst
#    if syst < pdf_dn_VBF:
#        pdf_dn_VBF = syst

#print "ggF PDF up:   ",pdf_up_ggF
#print "ggF PDF down: ",pdf_dn_ggF

print "tot hessian PDF up:   ",hessian_pdf_tot[0]
print "tot hessian PDF down: ",hessian_pdf_tot[1]

print "tot other PDF up:   ",other_pdf_tot[0]
print "tot other PDF down: ",other_pdf_tot[1]

print "tot total up: ",math.sqrt(pow(hessian_pdf_tot[0],2)+pow(other_pdf_tot[0],2))
print "tot total down: ",math.sqrt(pow(hessian_pdf_tot[1],2)+pow(other_pdf_tot[1],2))


print "ggF hessian PDF up:   ",hessian_pdf_ggF[0]
print "ggF hessian PDF down: ",hessian_pdf_ggF[1]

print "ggF other PDF up:   ",other_pdf_ggF[0]
print "ggF other PDF down: ",other_pdf_ggF[1]

print "ggF total up: ",math.sqrt(pow(hessian_pdf_ggF[0],2)+pow(other_pdf_ggF[0],2))
print "ggF total down: ",math.sqrt(pow(hessian_pdf_ggF[1],2)+pow(other_pdf_ggF[1],2))

print "VBF hessian PDF up:   ",hessian_pdf_VBF[0]
print "VBF hessian PDF down: ",hessian_pdf_VBF[1]

print "VBF other PDF up:   ",other_pdf_VBF[0]
print "VBF other PDF down: ",other_pdf_VBF[1]

print "VBF total up: ",math.sqrt(pow(hessian_pdf_VBF[0],2)+pow(other_pdf_VBF[0],2))
print "VBF total down: ",math.sqrt(pow(hessian_pdf_VBF[1],2)+pow(other_pdf_VBF[1],2))

xsecs_orig=[43.92,3.748,1.380,0.8696,0.5085]


#print "VBF PDF up:   ",pdf_up_VBF
#print "VBF PDF down: ",pdf_dn_VBF

#for mode in [tggF,tVBF]:
#    for weight in weights:
#        print weight
