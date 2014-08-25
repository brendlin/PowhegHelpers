#include "TCanvas.h"
#include "TMarker.h"
#include "TLatex.h"
#include "TruthUtils.h"

#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"

using fastjet::PseudoJet;

void DrawText(double x, double y, Str txt, int align=22) {
  TLatex *tex = new TLatex(); tex->SetTextAlign(align); tex->SetTextFont(42); tex->SetTextSize(0.024);
  tex->DrawLatex(x,y,txt);
}

void DrawMarker(double x, double y, int ms, int col, double size) {
  static TMarker *m = new TMarker(); m->SetNDC(0); m->SetMarkerStyle(ms); m->SetMarkerColor(col); m->SetMarkerSize(size);
  m->DrawMarker(x,y);
}

Str getPtclName(int id) {
  if (id==21) return "g";
  if (id==22) return "#gamma";
  if (id==11) return "e^{-}";
  if (id==-11) return "e^{+}";
  if (id==13) return "#mu^{-}";
  if (id==-13) return "#mu^{+}";
  int aid=abs(id); Str n="t";
  if (id==0||aid>6) fatal(Form("Don't know how about pdgID %d",id));
  if (aid==1) n="d"; else if (aid==2) n="u"; else if (aid==3) n="s";
  else if (aid==4) n="c"; else if (aid==5) n="b";
  if (id<0) n="#bar{"+n+"}";
  return n;
}

int getPtclColor(int id) {
  int aid=abs(id); if (id==21) return kGray+2; else if (id==22) return kRed+1;
  if (aid<=3) return kBlue; if (aid==5) return kMagenta+3;
  return kBlack;
}

void DrawMCpart(const MCpart &ptcl, bool drawPt=true) {
  DrawMarker(ptcl.Rapidity(),ptcl.Phi(),20,kWhite,1.8);
  Str name(""); //int ms=20, col=kBlack;
  DrawMarker(ptcl.Rapidity(),ptcl.Phi(),24,getPtclColor(ptcl.ID()),1.8);
  DrawText(ptcl.Rapidity()+0.02,ptcl.Phi(),getPtclName(ptcl.ID()));

  if (drawPt)
    DrawText(ptcl.Rapidity()+0.12,ptcl.Phi(),Form("%.1f",ptcl.Pt()),12);
}


void DrawEvent(vector<PseudoJet> fjInputs, const fastjet::JetDefinition &antikt,
	       vector<MCpart> ems, vector<MCpart> partons, double pTcut, Str pname) {
  printf("\n  Producing event display: %s\n\n",pname.Data());

  static bool first = true;
  static vector<PseudoJet> ghosts;
  static TCanvas *can = new TCanvas("","",1000,600); 
  can->SetTopMargin(0.04); can->SetRightMargin(0.14); can->SetLeftMargin(0.08); can->SetBottomMargin(0.1);
  
  double etaMax = 5, dEta=0.02;
  int Neta(etaMax/dEta), Nphi=200;
  static TH2F *h_Eflow = new TH2F("Eflow","",Neta/2,-etaMax,etaMax,Nphi/2,-TMath::Pi(),TMath::Pi());
  static TH2F *h_jets  = new TH2F("jets","",Neta*2,-etaMax,etaMax,Nphi,-TMath::Pi(),TMath::Pi());
  
  if (first) {
    h_jets->SetStats(0); h_jets->SetXTitle("#it{y}"); h_jets->SetYTitle("#it{#phi}"); 
    h_jets->SetZTitle("jet #it{p}_{T} [GeV]");
    
    // Ghosts
    TLorentzVector ghost;
    for (int ieta=-Neta;ieta<Neta;++ieta)
      for (int iphi=0;iphi<Nphi;++iphi) {
	double phi=TMath::TwoPi()*(0.5+iphi)/Nphi, eta=dEta*(0.5+ieta);
	//printf("%.2f %.2f\n",phi,eta);
	ghost.SetPtEtaPhiM(1e-6,eta,phi,0);
	ghosts.push_back(PseudoJet(ghost.Px(),ghost.Py(),ghost.Pz(),ghost.E()));
      }
  }
  first=false;
  
  h_Eflow->Reset(); h_jets->Reset(); double max=0;
  for (size_t i=0;i<fjInputs.size();++i) {
    if (fjInputs[i].pt()>max) max=fjInputs[i].pt();
    h_Eflow->Fill(fjInputs[i].rap(),fjInputs[i].phi_std(),fjInputs[i].pt());
  }

  //printf("%d ghosts\n",(int)ghosts.size());
  for (size_t i=0;i<ghosts.size();++i) fjInputs.push_back(ghosts[i]);
  
  fastjet::ClusterSequence clustSeqAntikt(fjInputs, antikt);
  vector<PseudoJet> jets = sorted_by_pt( clustSeqAntikt.inclusive_jets(pTcut) );
  
  
  // Get good jets
  vector<TLorentzVector> tlvJets;
  for (unsigned i = 0; i < jets.size(); ++i) tlvJets.push_back(TLorentzVector(jets[i].px(),jets[i].py(),jets[i].pz(),jets[i].e()));
  
  if ( jets.size()&&jets[0].pt()>max) max=jets[0].pt();
  for (unsigned i = 0; i < jets.size(); ++i) {
    size_t Nconst = jets[i].constituents().size();
    for (size_t ci=0;ci<Nconst;++ci) {
      const PseudoJet &c = jets[i].constituents()[ci];
      if ( fabs(c.pt()-1e-6)<2e-7 ) h_jets->Fill(c.rap(),c.phi_std(),jets[i].pt());
    }
  }
  
  //h_jets->SetMaximum(max); h_Eflow->SetMaximum(max);
  h_jets->GetZaxis()->SetRangeUser(0,1.05*max); h_Eflow->GetZaxis()->SetRangeUser(0,1.05*max);
  h_jets->Draw("colz"); h_Eflow->Draw("colz same");

  //for (unsigned i = 0; i < jets.size(); ++i) 
  // DrawText(jets[i].rap(),jets[i].phi_std(),Form("%.1f GeV",jets[i].pt()));
  
  for (size_t pi=0;pi<ems.size();++pi) 
    DrawMCpart(ems[pi]);
  for (size_t pi=0;pi<partons.size();++pi) 
    DrawMCpart(partons[pi]);

  /*
  for (size_t i=0;i<fjInputs.size();++i) {
    if (fjInputs[i].pt()<1e-3) continue;
    if (fjInputs[i].pt()<1)
      DrawMarker(fjInputs[i].eta(),fjInputs[i].phi_std(),22,kBlue,0.8);
    else if (fjInputs[i].pt()<5)
      DrawMarker(fjInputs[i].eta(),fjInputs[i].phi_std(),22,kGreen+1,0.8);
    else if (fjInputs[i].pt()<10)
      DrawMarker(fjInputs[i].eta(),fjInputs[i].phi_std(),22,kOrange+2,0.8);
    else 
      DrawMarker(fjInputs[i].eta(),fjInputs[i].phi_std(),22,kRed,0.8);
  }
  */
  
  can->Print(pname);
}
