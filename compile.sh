#!/bin/sh

swdir=`pwd`/../

code=zz_powheg_Hjets.C
code2=get_pdfreweight.C
exec=zz_powheg_hgg.exe
exec2=get_pdfreweight.exe

#   # Set to paths
# pythia="-I$swdir/Pythia8/include -I$swdir/Pythia8/include/Pythia8 -L$swdir/Pythia8/lib/archive -I$swdir/HepMC/include -lpythia8 -lpythia8tohepmc -L$swdir/HepMC/lib -lHepMC -lgfortran "
# # -lgfortranbegin
fastjet="-I$swdir/fastjet/include -L$swdir/fastjet/lib/ -lfastjet"
# lhapdf="-L/afs/cern.ch/sw/lcg/external/MCGenerators/lhapdf/5.8.9/x86_64-slc6-gcc46-opt/lib/archive -lLHAPDF"
# #lhapdf="-L$swdir/LHApdf/lib/ -lLHAPDF"
# yaml="-L$swdir/yaml/lib/"
# root="$($ROOTSYS/bin/root-config --cflags --glibs) -lTreePlayer"
# #CXXFLAGS="-O2 -ansi -pedantic -W -Wall -Wshadow $flagsNlibs"
# boost="-L$swdir/Boost/lib -lboost_filesystem"
# CXXFLAGS="$flagsNlibs"

# flags=" $pythia $fastjet $lhapdf $root $yaml $boost $CXXFLAGS"

flags="-O2 -ansi -pedantic -W -Wall -Wshadow -Wno-shadow"

includes="-I/$swdir/Pythia8//include -I$swdir/HepMC/include"
libs="-L$swdir/Pythia8/lib/archive -lpythia8 -lpythia8tohepmc"
libs+=" -L$swdir/lhapdf/lib -lLHAPDF"
#libs+=" -L/afs/cern.ch/sw/lcg/external/MCGenerators/lhapdf/5.8.9/x86_64-slc5-gcc43-opt/lib/archive -lLHAPDF"
#libs+=" -L/afs/cern.ch/sw/lcg/external/MCGenerators/lhapdf/5.8.9/x86_64-slc6-gcc46-opt/lib/archive -lLHAPDF"
libs+=" -L$swdir/HepMC/lib -lHepMC -lgfortran -lgfortranbegin"
#libs+=" -L$swdir/Boost/lib -lboost_filesystem"
#libs+=" -L$swdir/Yaml/lib -lyaml-cpp"

# code=Pythia8_LHE_to_HEPMC2.cc
# exec=${code/cc/exe}
# mkdir -p bin

root="$($ROOTSYS/bin/root-config --cflags --glibs) -lTreePlayer"
g++ $includes $code -o $exec $libs $fastjet $root
g++ $includes $code2 -o $exec2 $libs $fastjet $root


# echo "Compilation flags"
# echo $flags
# g++ $flags $code -o $exec $INCL

settings=pythia_settings/zz_nominal.cmnd
  # set to -1 or ignore for all events
Nevts=20

ggF_H0j=/disk/userdata00/atlas_data2/kurb/Minlo/data/LesHouches/gg_H/ggH_1_1/pwgevents-0001.lhe
ggF_H1j=~/data/LesHouches/gg_HJ/baseline/pwgevents-0001.lhe
ggF_H2j=~/data/LesHouches/gg_HJJ/baseline/pwgevents-0001.lhe
vbf=~/data/LesHouches/vbf_H/baseline/pwgevents-0001.lhe


echo ./$exec $settings $ggF_H0j $Nevts test.root # > gg_H.log
#./$exec $settings $ggF_H0j $Nevts # > gg_H.log

#./$exec $settings $ggF_H1j $Nevts > gg_HJ.log
#./$exec $settings $ggF_H2j $Nevts > gg_HJJ.log
#./$exec $settings $vbf $Nevts 

