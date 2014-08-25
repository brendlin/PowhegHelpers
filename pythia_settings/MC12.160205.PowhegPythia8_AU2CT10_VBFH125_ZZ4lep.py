evgenConfig.description = "POWHEG+PYTHIA8 VBF H->ZZ->4l with AU2 CT10"
evgenConfig.keywords = ["SMhiggs", "VBF", "Z","leptonic"]
evgenConfig.inputfilecheck = "VBFH_SM_M125"

include("MC12JobOptions/PowhegPythia8_AU2_CT10_Common.py")
# ... Photos
include ( "MC12JobOptions/Pythia8_Photos.py" )

topAlg.Pythia8.Commands += ['25:onMode = off',#decay of Higgs
                            '25:onIfMatch = 23 23',
                            '23:onMode = off',#decay of Z
                            '23:mMin = 2.0',
                            '23:onIfMatch = 11 11',
                            '23:onIfMatch = 13 13',
                            '23:onIfMatch = 15 15'
                            ]
