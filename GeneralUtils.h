
#include "TEnv.h"
#include "TColor.h"

template <class T> void add(vector<T> &vec, T a) { vec.push_back(a); };
template <class T> void add(vector<T> &v, T a, T b) { add(v,a); add(v,b); };
template <class T> void add(vector<T> &v, T a, T b, T c) { add(v,a,b); add(v,c); };
template <class T> void add(vector<T> &v, T a, T b, T c, T d) { add(v,a,b); add(v,c,d); };
template <class T> void add(vector<T> &vec, T a[]) { 
  uint n=sizeof(a)/sizeof(a[0]);
  for (uint i=0;i<n;++i) vec.push_back(a[i]);
}
template <class T> vector<T> vec(T a) { vector<T> v; add(v,a); return v; };
template <class T> vector<T> vec(T a, T b) { vector<T> v; add(v,a,b); return v; };
template <class T> vector<T> vec(T a, T b, T c) { vector<T> v; add(v,a,b,c); return v; };



#ifndef _GENERAL_UTILS_
#define _GENERAL_UTILS_

///////////////////////////////////////////////////////////////////////////////////////

void error(Str msg) {
  printf("ERROR:\n\n  %s\n\n",msg.Data()); 
  abort();
}


TEnv *OpenSettingsFile(Str fileName) {
  if (fileName=="") error("No config file name specified. Cannot open file!");
  TEnv *settings = new TEnv();
  int status=settings->ReadFile(fileName.Data(),EEnvLevel(0));
  if (status!=0) error(Form("Cannot read file %s",fileName.Data()));
  return settings;
}

StrV Vectorize(Str str, Str sep=" ") {
  StrV result; TObjArray *strings = str.Tokenize(sep.Data());
  if (strings->GetEntries()==0) { delete strings; return result; }
  TIter istr(strings);
  while (TObjString* os=(TObjString*)istr()) { 
    if (os->GetString()[0]=='#') break; 
    add(result,os->GetString()); 
  }
  delete strings; return result;
}

VecD VectorizeD(Str str, Str sep) {
  VecD result; StrV vecS = Vectorize(str,sep);
  for (uint i=0;i<vecS.size();++i) 
    result.push_back(atof(vecS[i]));
  return result;
}

VecF VectorizeF(Str str, Str sep) {
  VecF result; StrV vecS = Vectorize(str,sep);
  for (uint i=0;i<vecS.size();++i) 
    result.push_back(atof(vecS[i]));
  return result;
}

#endif
