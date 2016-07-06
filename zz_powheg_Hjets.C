#include <iostream>

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"

#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"

#include "TruthUtils.h"
#include "GeneralUtils.h"
#include "event_display.h"
#include <TSystem.h>

#include "LHAPDF/LHAPDF.h"
//#include "PDFTool.h"

using fastjet::PseudoJet;
using namespace Pythia8;
using namespace std;

class Scaling : public PDF{
  public:
    Scaling(int idBeamIn = 2212) : PDF(idBeamIn) {}

  private:
    void xfUpdate(int id, double x, double Q2);
};
void Scaling::xfUpdate(int, double x, double ) {
  double dv  = 4. * x * pow3(1. - x);
  double uv  = 2. * dv;
  double gl  = 2.  * pow5(1. - x);
  double sea = 0.4 * pow5(1. - x);
  xg    = gl;
  xu    = uv + 0.18 * sea;
  xd    = dv + 0.18 * sea;
  xubar = 0.18 * sea;
  xdbar = 0.18 * sea;
  xs    = 0.08 * sea;
  xc    = 0.04 * sea;
  xb    = 0.02 * sea;
  xuVal = uv;
  xuSea = xubar;
  xdVal = dv;
  xdSea = xdbar;
  idSav = 9;
};

/***************************************
 *     Hard-coded settings (for now)
 */

// Jet pT cut for fastjet (affects what jets are drawn)
double jetPtCut=10;

// How many events to draw?
int N2draw=0, Ndrawn=0;

// bool doMLM = false;

// Fastjet analysis - select algorithm and parameters
fastjet::JetDefinition antikt(fastjet::antikt_algorithm, 0.4, fastjet::E_scheme, fastjet::Best);

// ATLAS truth jets ignores mu and nu by default
bool ignoreMuNu = false;

int higgsDecayProduct = 23; // Z

bool debug = false;

/*
 * End of settings
 **************************************
 */


/*
 *   Object selection
 */
bool isGoodTruthJet(PseudoJet jet);
bool isGoodATLASJet(PseudoJet jet);
bool isGoodPtCutJet(PseudoJet jet, double PtCut);
bool hasGoodPhotons(vector<TLorentzVector> gams);
bool isGoodPhoton(TLorentzVector gam, double ptcut);
float minDR(TLorentzVector &gam1, TLorentzVector &gam2, TLorentzVector &jet1, TLorentzVector &jet2);
float GetPhotonPTt(TLorentzVector gam1, TLorentzVector gam2);
void shortList(Event& event);
void listParticle(int i,const Particle& pt);
// std::vector<float> get_m12m34m14m23cthstr(vector<TLorentzVector>& vec,int is2mu2e);
//std::vector<float> get_m12m34m14m23cthstr(vector<MCpart>& vec,int is2mu2e);
// std::vector<float> get_m12m34cthstrFromZs(vector<MCpart>& vec,MCpart& Higgs);
bool dressElectrons(vector<MCpart>& leps,vector<MCpart>& phots);
bool passDeltaRJetElec(PseudoJet jet,vector<MCpart> leps);
bool passLeptonDeltaRCut(vector<MCpart> leps);
std::vector<MCpart> chooseBornLeptons(std::vector<MCpart> leps,std::vector<float>& vars);
std::vector<MCpart> chooseFidLeptons(std::vector<MCpart> leps);
vector<MCpart> ElectronMuonCuts(vector<MCpart> leps);

int main(int argc, char* argv[]) {
  printf("\n=~=~=~=~=~=~=~=~=~=~=\n  POWHEG HJETS\n");
/*
  printf("Setting up PDFTool\n");
  PDFTool* pdftool = new PDFTool(4000000.,1,-1,10800); // do not set reweightPdf
  //pdftool->setPdfset(10800); // set initial pdfset
  //MSTW2008nlo90cl         21141
  //NNPDF23_nlo_as_0118    229800
  printf("Setting up PDFTool done.\n");
*/
  //
  // Arguments
  //
  // 1. Pythia settings file
  // 2. Les Houche input file (if you are generating events specify GENERATE)
  // 3. Number of events to run over
  // 4. Output file name (optional - except if you're generating events. In which case it is required.)
  // Generating events: must specify file name as such:
  // path/to/file/process_R_F_seed.root
  
  if(argc < 2) 
    fatal(Str("You need to provide 2 arguments:\n")+
	  "  1. Pythia settings file\n  2. Les Houche input file\n  3. Number of events to run over (optional)\n  4. Output file name (optional)\n\n"+
	  "  Example:\n    "+argv[0]+" qcd.baseline.cmnd pwgevents-0001.lhe H2jets.root");
  int nEvents = argc > 3 ? atol(argv[3]) : -1;
  if (argc>3&&nEvents==0) fatal(Str("Cannot extract a number from argument ")+argv[3]);


  // Figure out what we run over
  Str ifn       = argv[2]; // just for the info. actual file is read in directly from argv
  Str in_fn     = "UNSPECIFIED"; // just for info
  Str scale_str = "UNSPECIFIED"; // just for info
  Str process   = "UNSPECIFIED"; // needed!
  Str seed      = "UNSPECIFIED"; // seed (for generation)
  Str fact      = "UNSPECIFIED"; // fact (for generation)
  Str reno      = "UNSPECIFIED"; // renorm (for generation)
  int file_num = 0;
  std::cout << ifn.Data() << std::endl;
  if (ifn == "GENERATE") {
    // need to get hard process --> Npartons
    if (argc < 5) fatal("Generating events - must specify in an input file!");
    if (nEvents < 1) fatal("Generating events - must specify nEvents!");
    // output file should be of the form "var/out/ggH_1_1_0001.root" i.e. process_R_F_Seed
    Str tmp_parsed = Str(argv[4]).ReplaceAll("_","/"); // var/out/ggH/1/1/0001.root
    std::cout << "tmp_parsed: " << tmp_parsed    << std::endl;
    seed    = gSystem->BaseName(Str(tmp_parsed).ReplaceAll                           (".root",""));
    fact    = gSystem->BaseName(Str(tmp_parsed).ReplaceAll                  ("/"+seed+".root",""));
    reno    = gSystem->BaseName(Str(tmp_parsed).ReplaceAll         ("/"+fact+"/"+seed+".root",""));
    process = gSystem->BaseName(Str(tmp_parsed).ReplaceAll("/"+reno+"/"+fact+"/"+seed+".root",""));
    file_num = atoi(seed.Data());
    std::cout << "seed    : " << seed    << std::endl;
    std::cout << "fact    : " << fact    << std::endl;
    std::cout << "reno    : " << reno    << std::endl;
    std::cout << "process : " << process << std::endl;
  }
  else {
    in_fn     = gSystem->BaseName(ifn);
    scale_str = gSystem->BaseName(Str(ifn).ReplaceAll              ("/"+in_fn,""));
    process   = gSystem->BaseName(Str(ifn).ReplaceAll("/"+scale_str+"/"+in_fn,""));
    file_num = atoi(in_fn(in_fn.First('_')+1,4).Data());
    //scale_str = "ggH_1_1";
    //process = "VBF_H";
    //file_num = 20;
    std::cout << "LHE file : " << ifn << std::endl;
    std::cout << "in_fn    : " << in_fn << std::endl;
    std::cout << "scale_str: " << scale_str << std::endl;
    std::cout << "process  : " << process << std::endl;
  }

  int Npartons = -1; 
  if      (process=="gg_H"   ) Npartons=1;
  else if (process=="gg_HJ"  ) Npartons=2;
  else if (process=="gg_HJJ" ) Npartons=3;
  else if (process=="vbf_H"  ) Npartons=3;
  else if (process=="VBF_H"  ) Npartons=3;
  // mine
  else if (process=="ggH"            ) Npartons=1;
  else if (process=="ggH_12509"      ) Npartons=1;
  else if (process=="ggH8TeV"        ) Npartons=1;
  else if (process=="ggH13TeV"        ) Npartons=1;
  else if (process=="ggH_hfact"      ) Npartons=1;
  else if (process=="gg_H_hfact"     ) Npartons=1;
  else if (process=="minlo_HJ_mH125" ) Npartons=2;
  else if (process=="minlo_HJJ_mH125") Npartons=3;
  else if (process=="VBFH125"        ) Npartons=3;
  else if (process=="VBF_12509"      ) Npartons=3;
  else if (process=="VBF8TeV"        ) Npartons=3;
  else if (process=="VBF13TeV"        ) Npartons=3;
  // more
  else if (process=="WH")  Npartons=2;
  else if (process=="ZH")  Npartons=2;
  else if (process=="ttH") Npartons=3;
  else if (process=="bbH") Npartons=3;
  else if (process=="WH_mH125")  Npartons=2;
  else if (process=="ZH_mH125")  Npartons=2;
  else if (process=="ttH_mH125") Npartons=3;
  else fatal("Don't know about process "+process+" extracted from input LHE file: "+ifn);

  if (file_num<1) fatal("Cannot extract file number from input file "+in_fn+" (full path: "+ifn+")");

  Str sampleName = process+"_"+scale_str+"QCDscale_"+Str(gSystem->BaseName(argv[1])).ReplaceAll(".cmnd","")+"PythiaSettings";
  Str ofn = argc > 4 ? argv[4] : sampleName+".root";

  int mySeed = atoi(seed.Data());
  if (ifn=="GENERATE" && mySeed==0) fatal("cannot convert "+seed+" to integer, or no seed specified.");

  printf("\n");
  printf("  Les Houches input file:     %s\n",in_fn.Data());
  printf("  Pythia settings:            %s\n",argv[1]);
  printf("  Hard process:               %s\n",process.Data());
  printf("  N final-state partons:      %d\n",Npartons);
  printf("  File number:                %d\n",file_num);
  printf("  QCD scale variation:        %s\n",scale_str.Data());
  printf("  Sample name:                %s\n",sampleName.Data());
  printf("  Output file name:           %s\n",ofn.Data());
  printf("\n");
  printf("Generation specs:\n");
  printf("  process:                    %s\n",process.Data());
  printf("  renormMultFac:              %s\n",reno.Data());
  printf("  factorMultFac:              %s\n",fact.Data());
  printf("  seed:                       %s\n",seed.Data());
  printf("\n");

  // Generator. 
  Str pythia_dir("./xmldoc");
  if (gSystem->AccessPathName(pythia_dir)) 
    fatal("Cannot find "+pythia_dir+". Make a soft link\n  ln -s PATH-TO-PYTHIA/xmldoc .");
  Pythia pythia(pythia_dir.Data(),false);

  // Read in commands from external file.
  pythia.readFile(argv[1]); 
  if (ifn=="GENERATE") {
    pythia.settings.readString(Form("Random:seed = %d",12345+mySeed));
    pythia.settings.readString(Form("SigmaProcess:renormMultFac = %1.1f",atof(reno.Data())));
    pythia.settings.readString(Form("SigmaProcess:factorMultFac = %1.1f",atof(fact.Data())));
    pythia.init();
  }
  else {
    pythia.readString("Beams:frameType = 4");
    PDF* pdfAPtr = new Scaling(2212);
    PDF* pdfBPtr = new Scaling(2212);
    pythia.setPDFPtr(pdfAPtr,pdfBPtr);
    pythia.readString("Beams:eCM = 13000.");
    pythia.readString(Form("Beams:LHEF = %s",argv[2]));
    pythia.init();
  }
  if (nEvents == -1) nEvents=pythia.mode("Main:numberOfEvents");
  pythia.settings.listChanged();
  
  printf("  N events to process:        %d\n",nEvents);
  Event& event = pythia.event;
  std::cout<<"Test N events to process:\t"<<event.size()<<std::endl;
  // Event& event_partons = pythia_partons.event; 

  vector<PseudoJet> stbl_ptcls;
  // vector<PseudoJet> final_partons;
  vector<PseudoJet> jets; 
  //vector<PseudoJet> goodjets; // removed to avoid confusion
  vector<PseudoJet> good_jets_truth_fid;
  vector<PseudoJet> good_jets_truth;
  // vector<PseudoJet> partons;
  // vector<PseudoJet> partonjets;
  // vector<PseudoJet> goodpartonjets;
  // vector<PseudoJet> goodPtCutspartonjets;
  vector<MCpart> Hzz_leptons_finalstate; // Final state particles
  vector<MCpart> Hzz_leptons_born;       // Born (just before Zs) (truth-matched to Zs)
  vector<MCpart> all_born_leptons;       // all born leptons (even from parton showers)
  //vector<MCpart> fid_born_leptons;     // all born leptons (even from parton showers) which pass kin cuts
  vector<MCpart> chosen_born_leptons;    // 4 chosen, paired particles
  vector<MCpart> jet_overlap_leptons;    // final state, must pass electron / muon kin cuts
  vector<MCpart> Z_particles;            // for Z kinematics
  vector<MCpart> Higgs;
  vector<MCpart> fsr_photons;
  vector<MCpart> powheg_partons;
  
  int nFSRevents = 0;
    
  // output File and TTree
  TFile *OutputFile = new TFile(ofn,"RECREATE");
  _ot = new TTree("EvtTree","EvtTree",99);  
  
  TH1F *CutFlow = new TH1F("cut_flow","cut_flow;",11,0,11);
  CutFlow->GetXaxis()->SetBinLabel(1 ,"All events"    );
  CutFlow->GetXaxis()->SetBinLabel(2 ,"Pt/Eta/Leptons");
  CutFlow->GetXaxis()->SetBinLabel(3 ,"SFOS"          );
  CutFlow->GetXaxis()->SetBinLabel(4 ,"Pairing"       );
  CutFlow->GetXaxis()->SetBinLabel(5 ,"Pt"            );
  CutFlow->GetXaxis()->SetBinLabel(6 ,"Z1 mass (m12)" );
  CutFlow->GetXaxis()->SetBinLabel(7 ,"Z2 mass (m34)" );
  CutFlow->GetXaxis()->SetBinLabel(8 ,"DeltaR"        );
  CutFlow->GetXaxis()->SetBinLabel(9 ,"Jpsi"          );
  CutFlow->GetXaxis()->SetBinLabel(10,"m4l"           );
  CutFlow->GetXaxis()->SetBinLabel(11,"Has 2 jets"    );

  TH1F *CutFlowCum = new TH1F("cut_flow_cum","cut_flow_cum;",11,0,11);
  CutFlowCum->GetXaxis()->SetBinLabel(1 ,"All events"    );
  CutFlowCum->GetXaxis()->SetBinLabel(2 ,"Pt/Eta/Leptons");
  CutFlowCum->GetXaxis()->SetBinLabel(3 ,"SFOS"          );
  CutFlowCum->GetXaxis()->SetBinLabel(4 ,"Pairing"       );
  CutFlowCum->GetXaxis()->SetBinLabel(5 ,"Pt"            );
  CutFlowCum->GetXaxis()->SetBinLabel(6 ,"Z1 mass (m12)" );
  CutFlowCum->GetXaxis()->SetBinLabel(7 ,"Z2 mass (m34)" );
  CutFlowCum->GetXaxis()->SetBinLabel(8 ,"DeltaR"        );
  CutFlowCum->GetXaxis()->SetBinLabel(9 ,"Jpsi"          );
  CutFlowCum->GetXaxis()->SetBinLabel(10,"m4l"           );
  CutFlowCum->GetXaxis()->SetBinLabel(11,"Has 2 jets"    );

  TH1F* TotalEvents = new TH1F("TotalEvents","TotalEvents",2,0,2);
  TotalEvents->GetXaxis()->SetBinLabel(1,"2mu2e");
  TotalEvents->GetXaxis()->SetBinLabel(2,"4e/4mu");

  TH1F* EventType = new TH1F("event_type","event_type",8,0,8);
  EventType->Sumw2();
  EventType->GetXaxis()->SetBinLabel(1,"4mu");
  EventType->GetXaxis()->SetBinLabel(2,"2mu2e");
  EventType->GetXaxis()->SetBinLabel(3,"4e");
  EventType->GetXaxis()->SetBinLabel(4,"2e2mu");
  EventType->GetXaxis()->SetBinLabel(5,"4tau");
  EventType->GetXaxis()->SetBinLabel(6,"2tau2mu");
  EventType->GetXaxis()->SetBinLabel(7,"2tau2e");
  EventType->GetXaxis()->SetBinLabel(8,"Unknown");

  TH1F* EventTypeJPsi = new TH1F("event_type_jpsi","event_type_jpsi",8,0,8);
  EventTypeJPsi->Sumw2();
  EventTypeJPsi->GetXaxis()->SetBinLabel(1,"4mu");
  EventTypeJPsi->GetXaxis()->SetBinLabel(2,"2mu2e");
  EventTypeJPsi->GetXaxis()->SetBinLabel(3,"4e");
  EventTypeJPsi->GetXaxis()->SetBinLabel(4,"2e2mu");
  EventTypeJPsi->GetXaxis()->SetBinLabel(5,"4tau");
  EventTypeJPsi->GetXaxis()->SetBinLabel(6,"2tau2mu");
  EventTypeJPsi->GetXaxis()->SetBinLabel(7,"2tau2e");
  EventTypeJPsi->GetXaxis()->SetBinLabel(8,"Unknown");

  TH1F* EventTypeFinal = new TH1F("event_type_4leps","event_type_4leps",8,0,8);
  EventTypeFinal->GetXaxis()->SetBinLabel(1,"4mu");
  EventTypeFinal->GetXaxis()->SetBinLabel(2,"2mu2e");
  EventTypeFinal->GetXaxis()->SetBinLabel(3,"4e");
  EventTypeFinal->GetXaxis()->SetBinLabel(4,"2e2mu");
  EventTypeFinal->GetXaxis()->SetBinLabel(5,"4tau");
  EventTypeFinal->GetXaxis()->SetBinLabel(6,"2tau2mu");
  EventTypeFinal->GetXaxis()->SetBinLabel(7,"2tau2e");
  EventTypeFinal->GetXaxis()->SetBinLabel(8,"Unknown");
  gROOT->cd();
  
  // Initialize TTree
  //MakeIBranches("evtnum","QCDscale","process");
  Make4VecBranches("H"); // For the reconstructed Higgs
  MakeFBranches("H_rap","H_m34","H_m12","H_cthstr");
  Make4VecBranches("H_truth"); // for the truth-matched higgs events
  MakeFBranches("H_truth_rap","H_truth_m34","H_truth_m12","H_truth_cthstr");
  Make4VecBranches("lep1");
  Make4VecBranches("lep2");
  Make4VecBranches("lep3");
  Make4VecBranches("lep4");
  //Make4VecBranches("parton1"); 
  //Make4VecBranches("parton2"); 
  //Make4VecBranches("parton3");
  Make4VecBranches("jet1_truth_fid");
  //Make4VecBranches("jet2");
  //Make4VecBranches("jet3");

  //MakeFBranch("DR_parton1_jet1");
  //MakeFBranches("m_jj","Dy_jj","Deta_jj","Dphi_jj");
  //MakeFBranches("Dphi_gg_jj","pT_jj","pT_ggjj","minDR_gj");
  //MakeFBranches("pTt","eta_Zepp","y_Zepp","y_Zepp4vec");
  //MakeIBranch("Npartons");
  //MakeIBranch("Njets_30GeV_truth");
  MakeIBranch("Njets_30GeV_truth_fid");
  //MakeFBranch("xsec");
  MakeFBranch("weight");
  MakeFBranch("weight_mstw");
  MakeFBranch("weight_nnpd");
  MakeIBranch("is2mu2e");
  MakeIBranch("PassesCuts");

  // For pdf reweighting, to be done later
  MakeFBranches("mcevt_pdf_scale2","mcevt_pdf_x1","mcevt_pdf_x2");
  MakeIBranches("mcevt_pdf_id1","mcevt_pdf_id2");
  //Nominal PDF is CT14
  MakeFBranch("weight_0");
  
  //8 scale variations (1, 0.5, 2) x (1,0.5,2).  (1,1) is weight_0
  MakeFBranch("weight_1001");
  MakeFBranch("weight_1002");
  MakeFBranch("weight_1003");
  MakeFBranch("weight_1004");
  MakeFBranch("weight_1005");
  MakeFBranch("weight_1006");
  MakeFBranch("weight_1007");
  MakeFBranch("weight_1008");
  //1 thru 56 are CT14 eigenvector variations
  MakeFBranch("weight_2001");MakeFBranch("weight_2002");MakeFBranch("weight_2003");MakeFBranch("weight_2004");
  MakeFBranch("weight_2005");MakeFBranch("weight_2006");MakeFBranch("weight_2007");MakeFBranch("weight_2008");
  MakeFBranch("weight_2009");MakeFBranch("weight_2010");
  MakeFBranch("weight_2011");MakeFBranch("weight_2012");MakeFBranch("weight_2013");MakeFBranch("weight_2014");
  MakeFBranch("weight_2015");MakeFBranch("weight_2016");MakeFBranch("weight_2017");MakeFBranch("weight_2018");
  MakeFBranch("weight_2019");MakeFBranch("weight_2020");
  MakeFBranch("weight_2021");MakeFBranch("weight_2022");MakeFBranch("weight_2023");MakeFBranch("weight_2024");
  MakeFBranch("weight_2025");MakeFBranch("weight_2026");MakeFBranch("weight_2027");MakeFBranch("weight_2028");
  MakeFBranch("weight_2029");MakeFBranch("weight_2030");
  MakeFBranch("weight_2031");MakeFBranch("weight_2032");MakeFBranch("weight_2033");MakeFBranch("weight_2034");
  MakeFBranch("weight_2035");MakeFBranch("weight_2036");MakeFBranch("weight_2037");MakeFBranch("weight_2038");
  MakeFBranch("weight_2039");MakeFBranch("weight_2040");
  MakeFBranch("weight_2041");MakeFBranch("weight_2042");MakeFBranch("weight_2043");MakeFBranch("weight_2044");
  MakeFBranch("weight_2045");MakeFBranch("weight_2046");MakeFBranch("weight_2047");MakeFBranch("weight_2048");
  MakeFBranch("weight_2049");MakeFBranch("weight_2050");
  MakeFBranch("weight_2051");MakeFBranch("weight_2052");MakeFBranch("weight_2053");MakeFBranch("weight_2054");
  MakeFBranch("weight_2055");MakeFBranch("weight_2056");
  //CT10 PDF
  MakeFBranch("weight_2057");
  //MMHT2014
  MakeFBranch("weight_2058");
  //NNPDF3.0
  MakeFBranch("weight_2059");
  
  
  // _fmap["xsec"] = xsecs[scale_shift_index]; 
  // _imap["Npartons"] = powheg_partons.size();

  for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
    
    if (iEvent&&iEvent%100==0) { printf("  Processed %5.1fk / %5.1fk events\n",1e-3*iEvent,1e-3*nEvents); cout << flush; }
    if (debug) { 
      printf("  %%%%%%%\n");
      printf("  %%%%%%%\n");
      printf("  %%%%%%%\n");
      printf("  Processed %d / %5.1fk events\n",iEvent,1e-3*nEvents);
      printf("  %%%%%%%\n");
      printf("  %%%%%%%\n");
      printf("  %%%%%%%\n");
    }
    
    // Generate event. 
    if (!pythia.next()) break;

    // Test pdf stuff
    if (debug) {
      printf("scalup  : %2.2f \n",pythia.info.scalup());
      printf("scalup^2: %2.2f \n",pow(pythia.info.scalup(),2));
      printf("QFac    : %2.2f \n",pythia.info.QFac() );
      printf("Q2Fac   : %2.2f \n",pythia.info.Q2Fac());
      printf("x1pdf : %2.2f \n",pythia.info.x1pdf() );
      printf("x2pdf : %2.2f \n",pythia.info.x2pdf() );
      printf("id1pdf: %d    \n",pythia.info.id1pdf());
      printf("id2pdf: %d    \n",pythia.info.id2pdf());
      printf("pdf1  : %2.2f \n",pythia.info.pdf1()  );
      printf("pdf2  : %2.2f \n",pythia.info.pdf2()  );
    }
    if ((pythia.info.scalup()-pythia.info.QFac())/pythia.info.QFac()>0.001){
      printf("QFac    : %2.2f \n",pythia.info.QFac() );
      printf("scalup  : %2.2f \n",pythia.info.scalup());
      printf("Warning: scalup != QFac\n");
    }
    // End Test pdf stuff

    if (false){
      std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
      std::cout << "% event.list()" << std::endl;
      std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
      shortList(event);
      //event.list();
      
//       std::cout << " " << std::endl;
//       std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
//       std::cout << "% event_partons.list()" << std::endl;
//       std::cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << std::endl;
      //shortList(event_partons);
      //event_partons.list();
    }

    double mcevt_pdf_scale2 = pythia.info.Q2Fac();
    double mcevt_pdf_x1    = pythia.info.x1pdf();
    double mcevt_pdf_x2    = pythia.info.x2pdf();
    int mcevt_pdf_id1      = pythia.info.id1pdf();
    int mcevt_pdf_id2      = pythia.info.id2pdf();
    _fmap["mcevt_pdf_scale2"] = mcevt_pdf_scale2;
    _fmap["mcevt_pdf_x1"] = mcevt_pdf_x1;
    _fmap["mcevt_pdf_x2"] = mcevt_pdf_x2;
    _imap["mcevt_pdf_id1"] = mcevt_pdf_id1;
    _imap["mcevt_pdf_id2"] = mcevt_pdf_id2;
/*
    pdftool->setEventInfo(mcevt_pdf_scale2,mcevt_pdf_x1,mcevt_pdf_x2,mcevt_pdf_id1,mcevt_pdf_id2);
    double w_mstw = pdftool->pdf(21141);
    double w_nnpd = pdftool->pdf(229800);
    if ((abs(w_mstw) > 10000) || (w_mstw != w_mstw)) {
      printf("Error! weight is %2.2f. Setting to 0.\n",w_mstw);
      w_mstw = 0;
    }
    if ((abs(w_nnpd) > 10000) || (w_nnpd != w_nnpd)) {
      printf("Error! weight is %2.2f. Setting to 0.\n",w_nnpd);
      w_nnpd = 0;
    }
*/
    LHAPDF::setVerbosity(0);
    if (iEvent&&iEvent%100==0) LHAPDF::setVerbosity(1);
    if (iEvent&&iEvent%100==0) printf(">>>>>>>>>>>>> ");
    const LHAPDF::PDF* testpdf = LHAPDF::mkPDF("CT14nlo",0);
    //const LHAPDF::PDF* testpdf = LHAPDF::mkPDF("cteq6l1",0);
    const double xf = testpdf->xfxQ2(mcevt_pdf_id1,mcevt_pdf_x1,mcevt_pdf_scale2);
    if (iEvent&&iEvent%100==0) printf("<<<<<<<<<<<<< xf = %2.5f >>>>>>>>>>>>>>\n",xf);

    _fmap["weight"] = pythia.info.weight();
    double mergingweight = pythia.info.mergingWeight();
    double weight = _fmap["weight"];
    
    int nwgt = pythia.info.getWeightsDetailedSize();
    if (iEvent&&iEvent%100==0){
    	printf("<<<<<<<<<<<<< weight = %2.5f >>>>>>>>>>>>>>\n",weight);
    	printf("<<<<<<<<<<<<< MergingWeight = %2.5f >>>>>>>>>>>>>>\n",mergingweight);
    	printf("<<<<<<<<<<<<< nwgt = %d >>>>>>>>>>>>>>\n",nwgt);
    }
    for(int iwgt = 0;iwgt<nwgt;iwgt++){
      string key;
      string weight_str;
      ostringstream convert;
      double wgt_value = 0;
      if(iwgt == 0){
	convert << iwgt;
	key = convert.str();
    weight_str = "weight_"+key;
	wgt_value = pythia.info.getWeightsDetailedValue(key);
    _fmap[weight_str] = wgt_value;
      }
      else if(0<iwgt && iwgt<9){
	convert << iwgt+1000;
	key = convert.str();
    weight_str = "weight_"+key;
	wgt_value = pythia.info.getWeightsDetailedValue(key);
    _fmap[weight_str] = wgt_value;
      }
      else{
	convert << 2001+(iwgt-9);
	key = convert.str();
    weight_str = "weight_"+key;
	wgt_value = pythia.info.getWeightsDetailedValue(key);
    _fmap[weight_str] = wgt_value;
      }
//      printf("\twgt id=\'%s\'\t%2.5f\n",key,wgt_value);
      std::cout<<"\twgt id="<<key<<"\t"<<wgt_value<<std::endl;
    }
    double w_mstw = 1.;
    double w_nnpd = 1.;

    _fmap["weight_mstw"] = _fmap["weight"]*w_mstw;
    _fmap["weight_nnpd"] = _fmap["weight"]*w_nnpd;
    if (debug){
      printf("weight ct10   : %2.5f\n",_fmap["weight"]);
      printf("weight mstw   : %2.5f\n",_fmap["weight_mstw"]);
      printf("weight nnpd   : %2.5f\n",_fmap["weight_nnpd"]);
    }
    
    //event.list();
    CutFlow->Fill(0.,weight); // All events

    // Clear Hgg photons and other vectors
    Hzz_leptons_finalstate.clear();
    Hzz_leptons_born.clear();
    all_born_leptons.clear();    
    jet_overlap_leptons.clear();
    Z_particles.clear();
    Higgs.clear();
    fsr_photons.clear();
    powheg_partons.clear();
    /*final_partons.clear();*/
    stbl_ptcls.clear();
    // partons.clear();
    // partonjets.clear();
    jets.clear();
    //goodjets.clear();
    good_jets_truth_fid.clear();
    good_jets_truth.clear();
    // goodpartonjets.clear();
    // goodPtCutspartonjets.clear();
    
    // Save the Powheg partons
    for (int i=6;i<6+Npartons;++i) {
      const Particle &ptcl = event[i];
      if (ptcl.status()<-29) continue;
      powheg_partons.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id()));
    }

    bool ZZ_4l_filtered = false;
    if (debug) printf("Event number %d\n",iEvent);

    //
    // Get electrons / muons from Zs as daughters
    //
    bool has_e  = false; // attached to born
    bool has_mu = false; // attached to born
    for (int i = 0; i < event.size(); ++i) {
      const Particle &ptcl = event[i];
      //
      // From the Higgs
      //
      if (ptcl.idAbs() == 25){
	if(debug) printf("Found a Higgs! pt %2.2f status %d\n",ptcl.pT(),ptcl.status());
      }
      if (ptcl.idAbs() == 25 && event[ptcl.daughter1()].id() != 25 && event[ptcl.daughter2()].id() != 25){
	if(debug) printf("Found the Higgs! pt %2.2f status %d\n",ptcl.pT(),ptcl.status());
	Higgs.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id()));
	int gd1 = event[event[ptcl.daughter1()].daughter1()].idAbs();
	int gd2 = event[event[ptcl.daughter2()].daughter1()].idAbs();
	if (gd1 == 13 && gd2 == 13) EventType->Fill(0.,weight); // 4mu
	else if (gd1 == 13 && gd2 == 11) EventType->Fill(1.,weight); // 2mu2e
	else if (gd1 == 11 && gd2 == 13) EventType->Fill(2.,weight); // 2e2mu
	else if (gd1 == 11 && gd2 == 11) EventType->Fill(3.,weight); // 4e
	else if (gd1 == 15 && gd2 == 15) EventType->Fill(4.,weight); // 4tau
	else if ((gd1 == 15 && gd2 == 13) || (gd1 == 13 && gd2 == 15)) EventType->Fill(5.,weight); // 2tau2mu
	else if ((gd1 == 15 && gd2 == 11) || (gd1 == 11 && gd2 == 15)) EventType->Fill(6.,weight); // 2tau2e
	else EventType->Fill(7.,weight); // unknown
      }
      //
      // Two z's from the Higgs (for m34)
      //
      if (isZFromHiggs(ptcl,event)){
	int d1 = event[ptcl.daughter1()].idAbs();
	int d2 = event[ptcl.daughter2()].idAbs();
	if(debug) printf("d1: %d d2: %d\n",d1,d2);
	if (d1 != 11 && d1 != 13) {
	  if(debug) printf("Daugher1 is not a muon or electron! Skipping event.\n");
	  ZZ_4l_filtered = true;
	  break;
	}
	if (d2 != 11 && d2 != 13) {
	  if(debug) printf("Daugher2 is not a muon or electron! Skipping event.\n");
	  ZZ_4l_filtered = true;
	  break;
	}
	Z_particles.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id()));
      }
      //
      // Truth-matched to higgs
      //
      if ((ptcl.idAbs() == 11 || ptcl.idAbs() == 13) && isFromZFromHiggsBorn(ptcl,event) ) {
	if (debug) printf("It is one of them.\n");
	Hzz_leptons_born.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id())); 
	has_e  = ptcl.idAbs() == 11 ? true : has_e ;
	has_mu = ptcl.idAbs() == 13 ? true : has_mu;
      }
      //
      // All born leptons (even from parton showers)
      // apparently mother has to be from W or Z (see GetBornLeptons)
      // This was added a bit later.
      //
      if ((ptcl.idAbs() == 11 || ptcl.idAbs() == 13) && isBornLeptonFromWorZ(ptcl,event) ) {
	if (debug) printf("Found a born lepton! Index %d, mother types %d %d \n",i,event[ptcl.mother1()].id()
			  ,event[ptcl.mother2()].id());
	all_born_leptons.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id()));
      }

      //
      // Now do the final particle stuff we're used to doing
      //
      if (!ptcl.isFinal()) continue; // Final state only
      //stblSum+=ptcl.p();

      // For deltaR with jets
      if (ptcl.idAbs() == 11 || ptcl.idAbs() == 13){
	if (debug) printf("Found lepton: id %d status %d\n",ptcl.id(),ptcl.status(),isFromZFromHiggs(ptcl,event));
	jet_overlap_leptons.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id()));
      }
      // Put the higgs final state particles
//       if ((ptcl.idAbs() == 11 || ptcl.idAbs() == 13) && isFromZFromHiggs(ptcl,event) ) {
// 	if (debug) printf("It is one of them.\n");
// 	Hzz_leptons_finalstate.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id())); 
//       }
      if (fabs(ptcl.eta())<5 
	  && !(ptcl.idAbs() == 12) // NOT electron neutrinos
	  && !(ptcl.idAbs() == 13) // NOT muons
	  && !(ptcl.idAbs() == 14) // NOT muon neutrinos
	  && !(ptcl.idAbs() == 16) // NOT tau neutrinos
	  ) {
	// Save it as a stable particle
	stbl_ptcls.push_back( PseudoJet(ptcl.px(), ptcl.py(), ptcl.pz(), ptcl.e()) );
	if (ptcl.id() == 22) {
	  fsr_photons.push_back(MCpart(ptcl.pT(),ptcl.eta(),ptcl.phi(),ptcl.m(),ptcl.id(),i));
	}
      }
    }
    //
    // checks
    // First check: whether the 2 Zs go to leptons. For filtering ZH.
    //
    if (ZZ_4l_filtered) {
      if(debug) printf("Daugher2 is not a muon or electron! ACTUALLY skipping the event.\n");
      delete testpdf;
      iEvent--;
      continue;
    }
    //
    // The following are sanity checks. The program stops if some are not satisfied.
    //
    if (debug) printf("Event number %d not filtered!\n",iEvent);
    if (Hzz_leptons_born.size()>4) fatal(Form("Evt: %d %d final leptons\n",iEvent,int(Hzz_leptons_born.size())));
    if (Hzz_leptons_born.size()<4) fatal(Form("Evt: %d %d final leptons\n",iEvent,int(Hzz_leptons_born.size())));
    if (Z_particles.size() > 2 || Z_particles.size() < 2) fatal(Form("Evt: %d %d Zs\n",iEvent,int(Z_particles.size())));
    if (Higgs.size() > 1 || Higgs.size() < 1) fatal(Form("Evt: %d %d Higgses \n",iEvent,int(Higgs.size())));
    //
    // Ok, at this point we need to start counting events.
    //
    if (debug) printf("~~~~~~~~~~~~~~~~~~~~~~ start of event data storage.\n");
    
    int is2mu2e_truth = (has_e && has_mu) ? 1:0;
    std::vector<float> kin_vars_truth;
    // We do not want them from the Z particles, because of interference.
    vector<MCpart> higgs_lep4 = chooseBornLeptons(Hzz_leptons_born,kin_vars_truth); // UH these (Hzz_leptons_born) are the truth-matched born leptons.
    if (debug) printf("m12 %2.2f m34 %2.2f jpsis %2.2f %2.2f cth %2.2f is2mu2e %d\n",
		      kin_vars_truth[0],kin_vars_truth[1],kin_vars_truth[2],kin_vars_truth[3],kin_vars_truth[4],is2mu2e_truth);
    
    TotalEvents->Fill(is2mu2e_truth);

    Fill4VecBranches("H_truth",Higgs[0]);
    _fmap["H_truth_rap"] = Higgs[0].Rapidity();
    _fmap["H_truth_m12"] = kin_vars_truth[0]; // ALLOW FOR MISPAIRING!
    _fmap["H_truth_m34"] = kin_vars_truth[1]; // ALLOW FOR MISPAIRING!
    _fmap["H_truth_cthstr"] = kin_vars_truth[4];

    _imap["is2mu2e"] = is2mu2e_truth;
    _imap["PassesCuts"] = 0;

    // Fiducial - correctly filled later.
    Reset4VecBranches("H");
    _fmap["H_rap"]=-1.;
    _fmap["H_m34"]=-1.;
    _fmap["H_m12"]=-1.;
    _fmap["H_cthstr"]=-1.;

    _fmap["m_jj"]       = -1.;
    _fmap["Dy_jj"]      = -1.;
    _fmap["Deta_jj"]    = -1.;
    _fmap["Dphi_jj"]    = -1.;
    _fmap["pT_jj"]      = -1.;
    _fmap["Dphi_gg_jj"] = -1.;
    _fmap["pT_ggjj"]    = -1.;
    _fmap["minDR_gj"]   = -1.;
    _fmap["eta_Zepp"]   = -1.;
    _fmap["y_Zepp"]     = -1.;
    _fmap["y_Zepp4vec"] = -1.;

    // _imap["QCDscale"] = scale;
    //_imap["evtnum"]      = file_num*1e6 + iEvent;

    Reset4VecBranches("lep1");
    Reset4VecBranches("lep2");
    Reset4VecBranches("lep3");
    Reset4VecBranches("lep4");

    //
    // Pt ordered TLVs
    vector<double> ordered_pt;
    for (int i = 0; i < higgs_lep4.size(); ++i) {
      if (debug) printf("Lep: %2.2f %2.2f %2.2f %2.2f\n",higgs_lep4[i].Pt(),higgs_lep4[i].Eta()
			,higgs_lep4[i].Phi(),higgs_lep4[i].M());
      ordered_pt.push_back(higgs_lep4[i].Pt());
    }
    // std::sort default is ascending order
    std::sort(ordered_pt.begin(),ordered_pt.begin()+4);
    vector<TLorentzVector> leptons_ptordered;
    leptons_ptordered.push_back(TLorentzVector());
    leptons_ptordered.push_back(TLorentzVector());
    leptons_ptordered.push_back(TLorentzVector());
    leptons_ptordered.push_back(TLorentzVector());

    //bool pt0isMuon;
    for (int i = 0; i < higgs_lep4.size(); ++i) {
      //printf("ordered pt i %2.2f\n",ordered_pt[i]);
      //printf("lep pt i %2.2f\n",leptons[i].Pt());
      //
      // This is reverse ordered. I.e. highest pt lepton is 1st lepton.
      if (higgs_lep4[i].Pt() == ordered_pt[0]) {leptons_ptordered[3] = higgs_lep4[i];}
      if (higgs_lep4[i].Pt() == ordered_pt[1]) {leptons_ptordered[2] = higgs_lep4[i];}
      if (higgs_lep4[i].Pt() == ordered_pt[2]) {leptons_ptordered[1] = higgs_lep4[i];}
      if (higgs_lep4[i].Pt() == ordered_pt[3]) {leptons_ptordered[0] = higgs_lep4[i];}
    }
    if (leptons_ptordered[0].Pt() < leptons_ptordered[1].Pt()) fatal("Pt ordering failed!\n");
    if (leptons_ptordered[1].Pt() < leptons_ptordered[2].Pt()) fatal("Pt ordering failed!\n");
    if (leptons_ptordered[2].Pt() < leptons_ptordered[3].Pt()) fatal("Pt ordering failed!\n");

    Fill4VecBranches("lep1",leptons_ptordered[0]); 
    Fill4VecBranches("lep2",leptons_ptordered[1]);
    Fill4VecBranches("lep3",leptons_ptordered[2]);
    Fill4VecBranches("lep4",leptons_ptordered[3]);

    Reset4VecBranches("jet1_truth_fid");
    //Reset4VecBranches("jet2");
    //Reset4VecBranches("jet3");

    //
    // Dress electrons - we STILL do not dress muons
    // Have to do this before selecting jets
    //
    //nFSRevents += (dressElectrons(jet_overlap_leptons,fsr_photons) ? 1 : 0);
    if (debug) {
      printf("jet_overlap_leptons.size() %d\n",jet_overlap_leptons.size());
      for (int i = 0; i < jet_overlap_leptons.size(); ++i) {
	printf("Overlap Lep: %2.2f %2.2f %2.2f %2.2f\n",jet_overlap_leptons[i].Pt(),jet_overlap_leptons[i].Eta()
	       ,jet_overlap_leptons[i].Phi(),jet_overlap_leptons[i].M());
      }
    }
    jet_overlap_leptons = ElectronMuonCuts(jet_overlap_leptons);
    if (debug){
      printf("Applied electron muon cuts.\n");
      printf("jet_overlap_leptons.size() %d\n",jet_overlap_leptons.size());
      for (int i = 0; i < jet_overlap_leptons.size(); ++i) {
	printf("Overlap Lep: %2.2f %2.2f %2.2f %2.2f\n",jet_overlap_leptons[i].Pt(),jet_overlap_leptons[i].Eta()
	       ,jet_overlap_leptons[i].Phi(),jet_overlap_leptons[i].M());
      }
    }

    // Run anti-kT algorithm with R = 0.4
    if (debug) printf("Run Anti-kT algorithm\n");
    fastjet::ClusterSequence clustSeqAntikt(stbl_ptcls, antikt);
    jets = sorted_by_pt( clustSeqAntikt.inclusive_jets(jetPtCut) );
    if (debug) printf("Run Anti-kT algorithm finished\n");

    for (size_t i = 0; i < jets.size(); ++i) {
      //
      // delta-R cut for jets is with DRESSED final-state leptons (jet_overlap_leptons)
      // CURRENT minitrees are non-dressed, so we currently do not dress. But this will change.
      bool passDeltaR = passDeltaRJetElec(jets[i],jet_overlap_leptons); // jet_overlap_leptons
      // This is what we are using for njet distribution
      if (!passDeltaR) continue;
      if( isGoodTruthJet(jets[i]) ) good_jets_truth.push_back(jets[i]);
      if( isGoodATLASJet(jets[i]) ) good_jets_truth_fid.push_back(jets[i]);
      
      if (isGoodATLASJet(jets[i]) && !isGoodTruthJet(jets[i])) 
	printf("Error! Jet is a good ATLAS jet but not a truth jet! Whaaat?\n");
      
    }

    _imap["Njets_30GeV_truth_fid"] = good_jets_truth_fid.size(); 
    //_imap["Njets_30GeV_truth"] = good_jets_truth.size(); 

    if (good_jets_truth_fid.size()>0) Fill4VecBranches("jet1_truth_fid",good_jets_truth_fid[0]);
    //if (good_jets_truth_fid.size()>1) Fill4VecBranches("jet2",good_jets_truth_fid[1]); // comment for now
    //if (good_jets_truth_fid.size()>2) Fill4VecBranches("jet3",good_jets_truth_fid[2]); // comment for now

    //
    // Have to choose fiducial leptons now. Possible now that events will fail to reconstruct
    // the Higgs. In which case, fill the event, and continue.
    //
    if (debug) printf("Evt: %d: %d born leptons\n",iEvent,int(all_born_leptons.size()));
    vector<MCpart> fid_born_leptons = chooseFidLeptons(all_born_leptons);
    if (debug) printf("Number of fiducial (kin cuts) born leptons: %d \n",fid_born_leptons.size());
    if (fid_born_leptons.size()<4) {
      if (debug) printf("Evt: %d has %d fiducial born leptons. skipping.\n",iEvent,int(fid_born_leptons.size())); 
      _ot->Fill();
      continue; 
    };
    CutFlow->Fill(1.,weight);// Pt/Eta/Leptons

    
    int n_electrons_pos = 0;
    int n_electrons_neg = 0;
    int n_muons_pos = 0;
    int n_muons_neg = 0;
    for (int i = 0; i < fid_born_leptons.size(); ++i) {
      if (fid_born_leptons[i].ID() == -11) n_electrons_pos++;
      if (fid_born_leptons[i].ID() ==  11) n_electrons_neg++;
      if (fid_born_leptons[i].ID() == -13) n_muons_pos++;
      if (fid_born_leptons[i].ID() ==  13) n_muons_neg++;
    }
    bool pass_SFOS = ((n_electrons_pos >=2 && n_electrons_neg >=2) 
		      || (n_muons_pos >=2 && n_muons_neg >=2) 
		      || (n_muons_pos >=1 && n_muons_neg >=1 && n_electrons_pos >=1 && n_electrons_neg >=1));
    if (!pass_SFOS){
      _ot->Fill();
      continue;
    }
    CutFlow->Fill(2.,weight);// SFOS

    std::vector<float> kin_vars;
    // 0: m12
    // 1: m34
    // 2: m14
    // 3: m23
    // 4: cth
    // 5: is2mu2e
    vector<MCpart> chosen_born_leptons = chooseBornLeptons(fid_born_leptons,kin_vars);
    if (chosen_born_leptons.size() < 4){
      printf("Evt: %d fails os, sf requirement. skipping.\n",iEvent); 
      _ot->Fill();
      continue;
    }
    CutFlow->Fill(3.,weight);// Pairing

    bool is2mu2e_fid = (kin_vars[5] > 0.);

    if (debug) printf("NEW m12 %2.2f m34 %2.2f jpsis %2.2f %2.2f cth %2.2f is2mu2e_fid %d\n",
		      kin_vars[0],kin_vars[1],kin_vars[2],kin_vars[3],kin_vars[4],is2mu2e_fid);
    if (debug) printf("Number of fiducial (kin cuts), chosen (z1,z2) born leptons: %d \n",chosen_born_leptons.size());

    // start of denominator of fiducial acceptance

    if (debug) printf("ZZ invariant mass: %2.2f\n",((TLorentzVector)Z_particles[0]+(TLorentzVector)Z_particles[1]).Pt());
    if (debug) printf("Start Cutflow.\n");
    
    //
    // Pick which class of lepton you want to run the fiducial cutflow
    // options are:
    // chosen_born_leptons (born, but chosen from all leps)
    // Hzz_leptons_born (4 leptons are matched to higgs)
    // Hzz_leptons_finalstate (final state, dressed (for electrons))
    //
    //vector<MCpart> fiducial_cutflow_leps = chosen_born_leptons;
    

    //
    // Now do kinematic cuts (HZZ CutFlow)
    //

    int PassesCuts = 1;
    //
    // Lepton pt, eta
    if (debug) printf("Checking lepton pt/eta\n");
    bool pass_leppt = true;
    if (debug) printf("ID %d Eta %2.2f\n",chosen_born_leptons.at(0).absID(),chosen_born_leptons.at(0).Eta());
    if (debug) printf("ID %d Eta %2.2f\n",chosen_born_leptons.at(1).absID(),chosen_born_leptons.at(1).Eta());
    if (debug) printf("ID %d Eta %2.2f\n",chosen_born_leptons.at(2).absID(),chosen_born_leptons.at(2).Eta());
    if (debug) printf("ID %d Eta %2.2f\n",chosen_born_leptons.at(3).absID(),chosen_born_leptons.at(3).Eta());
    if (ordered_pt[1] < 10.) pass_leppt = false;
    if (ordered_pt[2] < 15.) pass_leppt = false;
    if (ordered_pt[3] < 20.) pass_leppt = false;
    if (debug) printf("Pt: %d\n",pass_leppt);
    if (!pass_leppt) PassesCuts = 0;
    if (PassesCuts) CutFlow->Fill(4.,weight); // Pt
    if (debug && PassesCuts) printf("Passes lepton pt/eta\n");

    if (!(50. < kin_vars[0] && kin_vars[0] < 106.)) PassesCuts = 0;
    if (debug && PassesCuts) printf("Passes m12\n");
    if (PassesCuts) CutFlow->Fill(5.,weight); // Z1 mass

    if (!(12. < kin_vars[1] && kin_vars[1] < 115.)) PassesCuts = 0;
    if (debug && PassesCuts) printf("Passes m34\n");
    if (PassesCuts) CutFlow->Fill(6.,weight); // Z2 mass

    int PassesDeltaRNew = (int)passLeptonDeltaRCut(chosen_born_leptons);
    PassesCuts = PassesCuts & PassesDeltaRNew;
    if (PassesCuts) CutFlow->Fill(7.,weight); // DeltaR

    // Jpsi
    if (!is2mu2e_fid && kin_vars[2] <= 5.) PassesCuts = 0;
    if (!is2mu2e_fid && kin_vars[3] <= 5.) PassesCuts = 0;
    if (debug && PassesCuts) printf("Passes jpsi\n");
    if (PassesCuts){
      CutFlow->Fill(8.,weight); // J/Psi
      int gd1 = chosen_born_leptons.at(0).absID();
      int gd2 = chosen_born_leptons.at(2).absID();
      if (gd1 == 13 && gd2 == 13) EventTypeJPsi->Fill(0.,weight); // 4mu
      else if (gd1 == 13 && gd2 == 11) EventTypeJPsi->Fill(1.,weight); // 2mu2e
      else if (gd1 == 11 && gd2 == 13) EventTypeJPsi->Fill(2.,weight); // 2e2mu
      else if (gd1 == 11 && gd2 == 11) EventTypeJPsi->Fill(3.,weight); // 4e
      else if (gd1 == 15 && gd2 == 15) EventTypeJPsi->Fill(4.,weight); // 4tau
      else if ((gd1 == 15 && gd2 == 13) || (gd1 == 13 && gd2 == 15)) EventTypeJPsi->Fill(5.,weight); // 2tau2mu
      else if ((gd1 == 15 && gd2 == 11) || (gd1 == 11 && gd2 == 15)) EventTypeJPsi->Fill(6.,weight); // 2tau2e
      else EventTypeJPsi->Fill(7.,weight); // unknown
    }
    //
    // m4l
    TLorentzVector H = ((TLorentzVector)chosen_born_leptons[0]+
			(TLorentzVector)chosen_born_leptons[1]+
			(TLorentzVector)chosen_born_leptons[2]+
			(TLorentzVector)chosen_born_leptons[3]);
    float m4l = H.M();
    
    if (debug) printf("m4l: %2.2f\n",m4l);
    if (!(118. < m4l && m4l < 129.)) PassesCuts = 0;
    if (debug && PassesCuts) printf("Passes m4l!\n");
    if (PassesCuts){
      CutFlow->Fill(9.,weight); // m4l
      int gd1 = chosen_born_leptons.at(0).absID();
      int gd2 = chosen_born_leptons.at(2).absID();
      if (gd1 == 13 && gd2 == 13) EventTypeFinal->Fill(0.,weight); // 4mu
      else if (gd1 == 13 && gd2 == 11) EventTypeFinal->Fill(1.,weight); // 2mu2e
      else if (gd1 == 11 && gd2 == 13) EventTypeFinal->Fill(2.,weight); // 2e2mu
      else if (gd1 == 11 && gd2 == 11) EventTypeFinal->Fill(3.,weight); // 4e
      else if (gd1 == 15 && gd2 == 15) EventTypeFinal->Fill(4.,weight); // 4tau
      else if ((gd1 == 15 && gd2 == 13) || (gd1 == 13 && gd2 == 15)) EventTypeFinal->Fill(5.,weight); // 2tau2mu
      else if ((gd1 == 15 && gd2 == 11) || (gd1 == 11 && gd2 == 15)) EventTypeFinal->Fill(6.,weight); // 2tau2e
      else EventTypeFinal->Fill(7.,weight); // unknown
    }
    if (debug) printf("PassesCuts: %d\n",PassesCuts);
    _imap["PassesCuts"] = PassesCuts;

    if (debug) printf("End Cutflow.\n");
    //
    // END HZZ Cutflow
    //
        
    // Draw event display for the first N2draw events
    if (debug) printf("Event displays\n");
    if ( Ndrawn++ < N2draw ) {
      DrawEvent(stbl_ptcls,antikt,chosen_born_leptons,powheg_partons,jetPtCut,sampleName+Form("_Event%d.png",iEvent));
    }
    if (debug) printf("Event displays done\n");

    // // Save output
    Fill4VecBranches("H",H); 
    _fmap["H_rap"]=H.Rapidity();
    _fmap["H_m34"]=kin_vars[1];
    _fmap["H_m12"]=kin_vars[0];
    _fmap["H_cthstr"]=kin_vars[4];
    if (debug) printf("H pt %2.2f (truth) %2.2f (reco)\n",_fmap["H_truth_pt"],_fmap["H_pt"]);

    if (good_jets_truth_fid.size() > 1 ) { // Jet preselection
      CutFlow->Fill(10.,weight); // Has 2 jets

      // ignore for now!
//       TLV jet1, jet2;
//       jet1.SetPtEtaPhiM(goodjets[0].pt(),goodjets[0].eta(),goodjets[0].phi(),goodjets[0].m());
//       jet2.SetPtEtaPhiM(goodjets[1].pt(),goodjets[1].eta(),goodjets[1].phi(),goodjets[1].m());
      
//       _fmap["m_jj"]       = (jet1+jet2).M();
//       _fmap["Dy_jj"]      = fabs(jet1.Rapidity()-jet2.Rapidity());
//       _fmap["Deta_jj"]    = fabs(jet1.Eta()-jet2.Eta());
//       _fmap["Dphi_jj"]    = fabs(jet1.DeltaPhi(jet2));
//       _fmap["pT_jj"]      = (jet1+jet2).Pt();
//       _fmap["Dphi_gg_jj"] = fabs(H.DeltaPhi(jet1+jet2));
//       _fmap["pT_ggjj"]    = (H+jet1+jet2).Pt();
//       _fmap["minDR_gj"]   = -99.; //minDR(gam1,gam2,jet1,jet2);      
//       _fmap["eta_Zepp"]   = H.Eta() - ((jet1.Eta() + jet2.Eta())/2);
//       _fmap["y_Zepp"]     = H.Rapidity() - ((jet1.Rapidity() + jet2.Rapidity())/2);
//       _fmap["y_Zepp4vec"] = H.Rapidity() - (jet1+jet2).Rapidity();
    }     

    _ot->Fill();
    
  delete testpdf;
  } // for each event

  printf("Number of FSR events: %d",nFSRevents);
  CutFlowCum->SetBinContent(1,1.);
  for(int i=1;i<CutFlow->GetNbinsX();++i){
    CutFlowCum->SetBinContent(i+1,CutFlow->GetBinContent(i+1)/float(CutFlow->GetBinContent(i)));
  }

  //pythia.stat(); 
  printf("\n  Saving output to %s\n\n",OutputFile->GetName());
  OutputFile->Write(); OutputFile->Close();
 
  // Done.
  printf("\n=~=~=~=~=~=~=~=~=~=~=\n");
  return 0;
}

bool isGoodPhoton(TLorentzVector gam, double ptcut) {
  // 1.56 is the new cut!
  if( !(fabs(gam.Eta()) <= 2.37 && !(1.37 < fabs(gam.Eta()) && fabs(gam.Eta()) < 1.52))) return false;
  return gam.Pt() > ptcut;
} 

// This is for the truth definition (taken from Jon's code)
bool isGoodTruthJet(PseudoJet jet) {
  if (fabs(jet.eta()) < 2.4 && jet.pt() > 25.) return true;
  if (2.4 < fabs(jet.eta()) && fabs(jet.eta()) < 4.5 && jet.pt() > 30.) return true;
  return false;
}

// This is for the fiducial definition
bool isGoodATLASJet(PseudoJet jet) {
  // Do not understand this
  //if ( jet.pt() < 25.0 || fabs(jet.eta()) > 4.5 ) return false;
  //if ( fabs(jet.eta()) < 2.5 ) return true;
  //return jet.pt() > 30.0;
  return (fabs(jet.rapidity()) < 4.4 && jet.pt() > 30.0);
}

bool isGoodPtCutJet(PseudoJet jet, double PtCut) {
  return jet.pt() > PtCut;
}

float minDR(TLorentzVector &gam1, TLorentzVector &gam2, TLorentzVector &jet1, TLorentzVector &jet2) {
  double j1g = jet1.DeltaR(gam1) < jet1.DeltaR(gam2) ? jet1.DeltaR(gam1) : jet1.DeltaR(gam2);
  double j2g = jet2.DeltaR(gam1) < jet2.DeltaR(gam2) ? jet2.DeltaR(gam1) : jet2.DeltaR(gam2);
  return j1g > j2g ? j2g : j1g;
}

float GetPhotonPTt(TLorentzVector gam1, TLorentzVector gam2) {
  double pxthrust = gam1.Px() - gam2.Px(), pythrust = gam1.Py() - gam2.Py();
  double norm = sqrt(pxthrust*pxthrust + pythrust*pythrust);
  pxthrust /= norm; pythrust /= norm;
  return 2 * fabs( gam1.Px()*pythrust - gam1.Py()*pxthrust );
}

void shortList(Event& event){
  std::cout << "Short Event Description" << std::endl;
  std::cout << "no    "
	    << "    id   name            status     mothers   daughters     colou"
	    << "rs      p_x        p_y        p_z         e          m " << std::endl;
  for (int i=0;i<event.size();++i) {
    const Particle &ptcl = event[i];
    //if (ptcl.status()<-29) continue;
    if (ptcl.idAbs()    !=11 // e
	&& ptcl.idAbs() !=13 // mu
	&& ptcl.id()    !=23 // Z
	&& ptcl.id()    !=25 // H
	&& ptcl.id()    !=22) continue; // Gamma
    listParticle(i,ptcl);
    if (ptcl.idAbs() == 11 || ptcl.idAbs() == 13) {
      if (ptcl.mother1()) {
	std::cout << ">";
	listParticle(ptcl.mother1(),event[ptcl.mother1()]);
      }
      if (ptcl.mother2()) {
	std::cout << ">";
	listParticle(ptcl.mother2(),event[ptcl.mother2()]);
      }
    }
  }
  std::cout << "End Short Event Description" << std::endl;
  return;
}

void listParticle(int i,const Particle& pt){
  bool useFixed = (pt.e() < 1e5);
  std::cout << setw(6) << i << setw(10) << pt.id() << "   " << left 
	    << setw(18) << pt.nameWithStatus(18) << right << setw(4) 
	    << pt.status() << setw(6) << pt.mother1() << setw(6) 
	    << pt.mother2() << setw(6) << pt.daughter1() << setw(6) 
	    << pt.daughter2() << setw(6) << pt.col() << setw(6) << pt.acol()
	    << ( (useFixed) ? fixed : scientific ) << setprecision(3) 
	    << setw(11) << pt.px() << setw(11) << pt.py() << setw(11) 
	    << pt.pz() << setw(11) << pt.e() << setw(11) << pt.m() << std::endl;
  return;
}

// Fiducial Cutflow: Muons. Bare Muons.

// Muons: Born level

// Fiducial Cutflow: Electrons. Dressed.
bool dressElectrons(vector<MCpart>& leps,vector<MCpart>& phots){
  //std::cout << "Photons size: " << phots.size() << std::endl;
  if (!phots.size()) return 0;
  bool isDressed = false;
  for (int i = 0; i < leps.size(); ++i){
    if (leps[i].absID() != 11) continue;
    for (int j = 0; j < phots.size(); ++j){
      // if (phots[j].Pt() == 0.) {
      // 	std::cout << "Empty photon!" << std::endl;
      // 	continue;
      // }
      if (leps[i].DeltaR(phots[j]) >= 0.1) continue;
      double orig_pt = leps[i].Pt();
      if (debug) printf("Lepton is being dressed by photon of index %d \n",phots[j].Index());
      if (debug) printf("Lep pre-dressing: %2.2f %2.2f %2.2f %2.2f\n",leps[i].Pt(),leps[i].Eta()
		       ,leps[i].Phi(),leps[i].M());
      //std::cout << "Lep pt " << leps[i].Pt() << " mass " << leps[i].M() << std::endl;
      //std::cout << "pho pt " << phots[j].Pt() << " mass " << phots[j].M() << std::endl;
      TLorentzVector tmp = leps[i]+phots[j];
      //std::cout << "tmp pt " << tmp.Pt() << " mass " << tmp.M() << std::endl;
      leps[i].SetPtEtaPhiM(tmp.Pt(),tmp.Eta(),tmp.Phi(),tmp.M());
      if (debug && fabs(leps[i].Pt() - orig_pt) <0.01) std::cout << "Negligible change" << std::endl;
      else isDressed = true;
      //std::cout << "Lep pt new " << leps[i].Pt() << std::endl;
      if (debug) printf("Lep pos-dressing: %2.2f %2.2f %2.2f %2.2f\n",leps[i].Pt(),leps[i].Eta()
		       ,leps[i].Phi(),leps[i].M());      
    }
  }
  return isDressed;
}

bool passDeltaRJetElec(PseudoJet jet, vector<MCpart> leps){
  bool passDeltaR = true;
  for (int j=0;j<leps.size();++j){
    if (!(leps.at(j).absID() == 11)) continue;
    TLV tmpjet;
    tmpjet.SetPtEtaPhiM(jet.pt(),jet.eta(),jet.phi(),jet.m());
    if (debug) printf("%2.2f\n",tmpjet.DeltaR(leps.at(j)));
    if (tmpjet.DeltaR(leps.at(j))<0.2) passDeltaR = false;
  }
  if (debug) printf("Jet Pass DR: %d\n",int(passDeltaR));
  return passDeltaR;
}

bool passLeptonDeltaRCut(vector<MCpart> leps){
  for (int i = 0; i < leps.size(); ++i) {
    for (int j = 0; j < leps.size(); ++j) {
      if (i >= j) continue;
      if (leps[i].absID() == leps[j].absID()) { // SF
	if (leps[i].DeltaR(leps[j]) < 0.1) return false;
      }
      else { // OF
	if (leps[i].DeltaR(leps[j]) < 0.2) return false;
      }
    }
  }
  return true;
}


// Electrons Born level

// chooseBornLeptons
// The output of this does not have to be ordered in any way.
// vars:
// 0. M12 is pair closest to z mass
// 1. M34 is the other pair
// 2. M14 is for checking for jpsi
// 3. M23 same (does not matter the order, 3 and 4)
// 4. cthstr (cosine theta star)
std::vector<MCpart> chooseBornLeptons(std::vector<MCpart> leps,std::vector<float>& vars){
  //
  // Z1 first
  double smallest_mass_diff = 9999.;
  int index1 = -1;
  int index2 = -1;
  float m12 = -1.;
  for (int i = 0; i < leps.size(); ++i) {
    for (int j = 0; j < leps.size(); ++j) {
      if (i >= j) continue;
      if (leps[i].ID() != -leps[j].ID()) continue; // SF, os
      float tmp_mass  = ((TLorentzVector)leps[i]+(TLorentzVector)leps[j]).M();
      float mass_diff = fabs(tmp_mass - 91.188);
      if (mass_diff < smallest_mass_diff){
	smallest_mass_diff = mass_diff;
	m12 = tmp_mass;
	index1 = i;
	index2 = j;
      }
    }
  }
  vector<MCpart> tmp;
  int index3 = -1;
  int index4 = -1;
  float m34 = -1.;
  smallest_mass_diff = 9999.;
  for (int i = 0; i < leps.size(); ++i) {
    for (int j = 0; j < leps.size(); ++j) {
      if (i >= j) continue;
      if (i == index1 || i == index2) continue;
      if (j == index1 || j == index2) continue;
      if (leps[i].ID() != -leps[j].ID()) continue; // SF, os
      float tmp_mass  = ((TLorentzVector)leps[i]+(TLorentzVector)leps[j]).M();
      float mass_diff = fabs(tmp_mass - 91.188);
      if (mass_diff < smallest_mass_diff){
	smallest_mass_diff = mass_diff;
	m34 = tmp_mass;
	index3 = i;
	index4 = j;
      }
    }
  }
  if (index3 == -1 || index4 == -1) {
    if (debug) std::cout << "Failed! 2 os, same-flavor pairs do not exist" << std::endl;
    return tmp;
  }
  tmp.push_back(leps[index1]);
  tmp.push_back(leps[index2]);
  tmp.push_back(leps[index3]);
  tmp.push_back(leps[index4]);

  TLorentzVector Z1 = (TLorentzVector)leps[index1]+(TLorentzVector)leps[index2];
  TLorentzVector Z2 = (TLorentzVector)leps[index3]+(TLorentzVector)leps[index4];
  TLorentzVector H = Z1+Z2;

  float m14 = ((TLorentzVector)leps[index1]+(TLorentzVector)leps[index4]).M();
  float m23 = ((TLorentzVector)leps[index2]+(TLorentzVector)leps[index3]).M();

  if (debug) std::cout << "Found Z1 with mass " << Z1.M() << std::endl;
  if (debug) std::cout << "Found Z2 with mass " << Z2.M() << std::endl;  

  bool hase    = (leps[index1].absID() == 11);
  hase = hase || (leps[index3].absID() == 11);
  bool hasmu     = (leps[index1].absID() == 13);
  hasmu = hasmu || (leps[index3].absID() == 13);
  float is2mu2e = (hase && hasmu) ? 1.0 : 0.0;
  // 1. boost Z1 to Higgs reference
  Z1.Boost(-H.BoostVector());
  // 2. Get the 3-vector
  // 3. Unit 3-vector
  // 4. Z-component == cthstr
  float cth = Z1.Vect().Unit().Z();

  vars.push_back(m12);
  vars.push_back(m34);
  vars.push_back(m14);
  vars.push_back(m23);
  vars.push_back(cth);
  vars.push_back(is2mu2e);
  return tmp;
}

std::vector<MCpart> chooseFidLeptons(std::vector<MCpart> leps){
  vector<MCpart> tmp;
  for (int i = 0; i < leps.size(); ++i) {
    if (leps.at(i).absID() == 13 && fabs(leps.at(i).Eta()) > 2.7 ) continue;
    if (leps.at(i).absID() == 11 && fabs(leps.at(i).Eta()) > 2.47) continue;
    if (leps.at(i).absID() == 13 && leps.at(i).Pt()<5.) continue;
    if (leps.at(i).absID() == 11 && leps.at(i).Pt()<7.) continue;
    if (debug) printf("Adding a fiducial lepton with id %d and Pt %2.2f\n",leps.at(i).ID(),leps.at(i).Pt());
    tmp.push_back(leps.at(i));
  }
  return tmp;
}

vector<MCpart> ElectronMuonCuts(vector<MCpart> leps){
  vector<MCpart> tmp;
  for (int i = 0; i < leps.size(); ++i) {
    if (leps.at(i).absID() == 13 && fabs(leps.at(i).Eta()) > 2.7) continue;
    if (leps.at(i).absID() == 11 && fabs(leps.at(i).Eta()) > 2.47) continue;
    if (leps.at(i).absID() == 13 && leps.at(i).Pt() < 5.) continue;
    if (leps.at(i).absID() == 11 && leps.at(i).Pt() < 7.) continue;
    tmp.push_back(leps.at(i));
  }
  return tmp;
}
