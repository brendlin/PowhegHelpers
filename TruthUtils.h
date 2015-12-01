#ifndef _TRUTH_UTILS_
#define _TRUTH_UTILS_

/*
 *   
 */

#include "Pythia8/Pythia.h"
//#include "Pythia8/Pythia8ToHepMC.h"
#include "Pythia8Plugins/HepMC2.h"
#include "TFile.h"
#include "TTree.h"
#include "TROOT.h"
#include "TLorentzVector.h"
#include "TMath.h"
#include "TH1F.h"
#include "TH2F.h"
#include <map>
#include <vector>
#include "fastjet/PseudoJet.hh"

//#include "HepMCInterface.h"
//#include "HepMC/GenEvent.h"
//#include "HepMC/IO_GenEvent.h"
// Following line to be used with HepMC 2.04 onwards.
//#include "HepMC/Units.h"

using namespace Pythia8;
using namespace std;
using fastjet::PseudoJet;

typedef TString Str;
typedef TLorentzVector TLV;
typedef vector<TLorentzVector> TLVs;
typedef vector<TString> StrV;
typedef vector<double> VecD;
typedef vector<float> VecF;
typedef vector<int> VecI;
typedef unsigned int uint;

void fatal(Str msg) { printf("\nFATAL:\n  %s\n\n",msg.Data()); abort(); }

class MCpart : public TLorentzVector {
public:
 MCpart(double pt, double eta, double phi, double m, int id)
   : _id(id),_index(0) { this->SetPtEtaPhiM(pt,eta,phi,m); }
 MCpart(double pt, double eta, double phi, double m, int id,int index)
   : _id(id),_index(index) { this->SetPtEtaPhiM(pt,eta,phi,m); }
  int ID() const { return _id; }
  int absID() const { return abs(_id); }
  int Index() const { return _index; }
  
private:
  int _id;
  int _index;
};

bool PtSort(MCpart const & L, MCpart const & R) {
  return L.Pt() < R.Pt();
}

bool LepTypeSort(MCpart const & L, MCpart const & R) {
  return L.Pt() < R.Pt();
}

map<Str,float> _fmap; map<Str,int> _imap; TTree *_ot; TTree *_ow;
void MakeIBranch(Str bn) { _ot->Branch(bn, &_imap[bn], bn+"/I"); }
void MakeFBranchXsec(Str bn) { _ow->Branch(bn, &_fmap[bn], bn+"/F"); }
void MakeIBranches(Str b1, Str b2) { MakeIBranch(b1); MakeIBranch(b2); }
void MakeIBranches(Str b1, Str b2, Str b3, Str b4="") { MakeIBranches(b1,b2); MakeIBranch(b3); if (b4!="") MakeIBranch(b4); }
void MakeFBranch(Str bn) { _ot->Branch(bn, &_fmap[bn], bn+"/F"); }
void MakeFBranches(Str b1, Str b2) { MakeFBranch(b1); MakeFBranch(b2); }
void MakeFBranches(Str b1, Str b2, Str b3, Str b4="") { MakeFBranches(b1,b2); MakeFBranch(b3); if (b4!="") MakeFBranch(b4); }

void Make4VecBranches(Str pName) { MakeFBranches(pName+"_pt",pName+"_eta",pName+"_phi",pName+"_m"); }
void Reset4VecBranches(Str pName) { _fmap[pName+"_pt"]=_fmap[pName+"_eta"]=_fmap[pName+"_phi"]=_fmap[pName+"_m"]=-99; }
void Fill4VecBranches(Str pName, const TLV &p) 
{  _fmap[pName+"_pt"]=p.Pt(); _fmap[pName+"_eta"]=p.Eta(); _fmap[pName+"_phi"]=p.Phi(); _fmap[pName+"_m"]=p.M(); }
void Fill4VecBranches(Str pName, const PseudoJet &j) 
{  _fmap[pName+"_pt"]=j.pt(); _fmap[pName+"_eta"]=j.eta(); _fmap[pName+"_phi"]=j.phi_std(); _fmap[pName+"_m"]=j.m(); }

TLorentzVector MakeTLV(PseudoJet jet) { TLorentzVector vec; vec.SetPtEtaPhiM(jet.pt(),jet.eta(),jet.phi(),jet.m()); return vec; }

bool isFromHiggs(const Particle &ptcl, const Event &evt) {
  if (evt[ptcl.mother1()].id()==25) return true;
  if (evt[ptcl.mother2()].id()==25) { printf("Mother 2 is the Higgs!?\n"); return true; }
  if (evt[ptcl.mother1()].id()==ptcl.id()) return isFromHiggs(evt[ptcl.mother1()],evt);  
  if (evt[ptcl.mother2()].id()!=ptcl.id()) return false;
  if (evt[ptcl.mother2()].id()==ptcl.id()) return isFromHiggs(evt[ptcl.mother2()],evt);
  return false;
}

bool isZFromHiggs(const Particle &ptcl, const Event &evt) {
  if (ptcl.id() == 23 && evt[ptcl.mother1()].id()==25) return true;
  if (ptcl.id() == 23 && evt[ptcl.mother2()].id()==25) {
    printf("Mother 2 is the Z??\n");
    return true;
  }
  return false;
}

bool isFromZFromHiggs(const Particle &ptcl, const Event &evt) {
  if (evt[ptcl.mother1()].id()==23 && isFromHiggs(evt[ptcl.mother1()],evt)) return true;
  if (evt[ptcl.mother2()].id()==23 && isFromHiggs(evt[ptcl.mother2()],evt)) {
    printf("Mother 2 is the Z??\n");
    return true;
  }
  if (evt[ptcl.mother1()].id()==ptcl.id()) return isFromZFromHiggs(evt[ptcl.mother1()],evt);
  if (evt[ptcl.mother2()].id()==ptcl.id()) return isFromZFromHiggs(evt[ptcl.mother2()],evt);
  return false;
}

bool isFromZFromHiggsBorn(const Particle &ptcl, const Event &evt) {
  if (evt[ptcl.mother1()].id()==23 && isFromHiggs(evt[ptcl.mother1()],evt)) return true;
  if (evt[ptcl.mother2()].id()==23 && isFromHiggs(evt[ptcl.mother2()],evt)) {
    printf("Mother 2 is the Z??\n");
    return true;
  }
  return false;
}

bool isBornLepton(const Particle &ptcl,const Event &evt){
  if (ptcl.idAbs() == 11  && evt[ptcl.mother1()].idAbs() == 11) return false;
  if (ptcl.idAbs() == 13  && evt[ptcl.mother1()].idAbs() == 13) return false;
  if (ptcl.idAbs() == 11  && evt[ptcl.mother1()].idAbs() == 11) return false;
  if (ptcl.idAbs() == 13  && evt[ptcl.mother1()].idAbs() == 13) return false;
  return true;
}

bool isBornLeptonFromWorZ(const Particle &ptcl,const Event &evt){
  if (ptcl.idAbs() == 11  && evt[ptcl.mother1()].idAbs() == 11) return false;
  if (ptcl.idAbs() == 13  && evt[ptcl.mother1()].idAbs() == 13) return false;
  if (ptcl.idAbs() == 11  && evt[ptcl.mother1()].idAbs() == 11) return false;
  if (ptcl.idAbs() == 13  && evt[ptcl.mother1()].idAbs() == 13) return false;
  if (evt[ptcl.mother1()].idAbs() == 23) return true;
  if (evt[ptcl.mother1()].idAbs() == 24) return true;
  return false;
}

/* bool isFromHiggs(const HepMC::GenParticle &ptcl) { */

/*     for (HepMC::GenVertex::particle_iterator m = ptcl.production_vertex()->particles_begin(HepMC::parents); m != ptcl.production_vertex()->particles_end(HepMC::parents); ++m ) { */
/*       if ((*m)->pdg_id() == 25) return true;        */
/*      } */

/*   return false;   */
/* } */

/* bool isFromW(const HepMC::GenParticle &ptcl) { */

/*     for (HepMC::GenVertex::particle_iterator m = ptcl.production_vertex()->particles_begin(HepMC::parents); m != ptcl.production_vertex()->particles_end(HepMC::parents); ++m ) { */
/*       if (fabs((*m)->pdg_id()) == 24) return true;        */
/*      } */

/*   return false;   */
/* } */

#endif
