topAlg.Pythia8.Commands += [
        "Tune:pp = 5",
            "PDF:useLHAPDF = on",
            "PDF:LHAPDFset = cteq6ll.LHpdf",
            "MultipartonInteractions:bProfile = 4",
            "MultipartonInteractions:a1 = 0.00",
            "MultipartonInteractions:pT0Ref = 2.13",
            "MultipartonInteractions:ecmPow = 0.21",
            "BeamRemnants:reconnectRange = 2.21",
            "SpaceShower:rapidityOrder=0"]
evgenConfig.tune = "AU2 CTEQ6L1"

## this is from MC12JobOptions/common/Pythia8_Base_Fragment.py
topAlg.Pythia8.Commands += [
        "Main:timesAllowErrors = 500",
            "6:m0 = 172.5",
            "23:m0 = 91.1876",
            "23:mWidth = 2.4952",
            "24:m0 = 80.399",
            "24:mWidth = 2.085",
            "StandardModel:sin2thetaW = 0.23113",
            "StandardModel:sin2thetaWbar = 0.23146",
            "ParticleDecays:limitTau0 = on",
            "ParticleDecays:tau0Max = 10.0"]

## MC12JobOptions/trunk/common/Pythia8_Photos.py
## Photos++ QED config for Pythia8
## Disable native QED FSR
assert hasattr(topAlg, "Pythia8")
topAlg.Pythia8.Commands += ["TimeShower:QEDshowerByL = off"]
## Enable Photos++
include("MC12JobOptions/Photospp_Fragment.py")


## MC12JobOptions/trunk/common/Photospp_Fragment.py
## Photos++ QED config
from Photospp_i.Photospp_iConf import Photospp_i
topAlg += Photospp_i("Photospp")
topAlg.Photospp.InfraRedCutOff = 1E-7
evgenConfig.generators += ["Photospp"]
