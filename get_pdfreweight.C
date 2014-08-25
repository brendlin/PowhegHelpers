#include <iostream>
//#include <TSystem.h>
#include "TruthUtils.h"
#include "PDFTool.h"

int main(int argc, char* argv[]) {

  if(argc < 3) fatal("Need to specify an input file and a pdf.");
  
  printf("Setting up PDFTool\n");
  PDFTool* pdftool = new PDFTool(4000000.,1,-1,10800); // do not set reweightPdf
  printf("Setting up PDFTool done.\n");

  TFile *InputFile = new TFile(Str(argv[1]),"READ");
  TTree *InTree = (TTree*)InputFile->Get("EvtTree");
  float weight          ; InTree->SetBranchAddress("weight"          ,&weight);
  float mcevt_pdf_scale2; InTree->SetBranchAddress("mcevt_pdf_scale2",&mcevt_pdf_scale2);
  float mcevt_pdf_x1    ; InTree->SetBranchAddress("mcevt_pdf_x1"    ,&mcevt_pdf_x1    );
  float mcevt_pdf_x2    ; InTree->SetBranchAddress("mcevt_pdf_x2"    ,&mcevt_pdf_x2    );
  int mcevt_pdf_id1      ; InTree->SetBranchAddress("mcevt_pdf_id1"   ,&mcevt_pdf_id1   );
  int mcevt_pdf_id2      ; InTree->SetBranchAddress("mcevt_pdf_id2"   ,&mcevt_pdf_id2   );
  TFile *OutputFile = new TFile(Str(argv[1]).ReplaceAll(".root","")+"_weights.root","UPDATE");    
  TTree *OutputTree;  
  bool isFirstTree = !OutputFile->Get("WeightTree");
  if (isFirstTree) OutputTree = new TTree("WeightTree","WeightTree");
  else OutputTree = (TTree*)OutputFile->Get("WeightTree");
  std::cout << "Is first tree?" << isFirstTree << std::endl;
  int pdfname = atoi(argv[2]);
  char pdfstr [50];
  int n;
  n=sprintf (pdfstr,"w_%d",pdfname);
  float pdfweight;
  TBranch *newBranch1 = OutputTree->Branch(pdfstr, &pdfweight, Str(pdfstr)+"/F");
//   for(int j=10801;j<10803;++j){
//     char pdfstr [50];
//     int n;
//     n = sprintf(pdfstr,"%d",j);
//     MakeIBranch(pdfstr);
//   }
  Long64_t nentries = InTree->GetEntries();
  for (Long64_t i = 0; i < nentries; i++){
    InTree->GetEntry(i);
//     std::cout << "mcevt_pdf_scale2" << " " << mcevt_pdf_scale2 << std::endl;
//     std::cout << "mcevt_pdf_x1"     << " " << mcevt_pdf_x1     << std::endl;
//     std::cout << "mcevt_pdf_x2"     << " " << mcevt_pdf_x2     << std::endl;
//     std::cout << "mcevt_pdf_id1"    << " " << mcevt_pdf_id1    << std::endl;
//     std::cout << "mcevt_pdf_id2"    << " " << mcevt_pdf_id2    << std::endl;
    pdftool->setEventInfo(mcevt_pdf_scale2,mcevt_pdf_x1,mcevt_pdf_x2,mcevt_pdf_id1,mcevt_pdf_id2);
    pdfweight = weight*pdftool->pdf(pdfname);
    if ((abs(pdfweight) > 10000) || (pdfweight != pdfweight)) {
      printf("Error! weight is %2.2f. Setting to 0.\n",pdfweight);
      pdfweight = 0;
    }
    //std::cout << pdfweight << std::endl;
    if (isFirstTree) OutputTree->Fill();
    else newBranch1->Fill();
  }
  OutputFile->cd();
  if (isFirstTree) OutputTree->Write();
  else OutputTree->Write("",TObject::kOverwrite);
  InputFile->Close();
  OutputFile->Close();
}
