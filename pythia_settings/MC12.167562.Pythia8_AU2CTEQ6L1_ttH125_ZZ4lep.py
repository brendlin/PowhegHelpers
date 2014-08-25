evgenConfig.description = "PYTHIA8 ttH H->ZZ->4l with AU2 CT10"
evgenConfig.keywords = ["SMhiggs", "ttH", "Z","leptonic"]

include("MC12JobOptions/Pythia8_AU2_CTEQ6L1_Common.py")
include("MC12JobOptions/Pythia8_Photos.py")

topAlg.Pythia8.Commands += ['25:m0 = 125',
                            '25:mWidth = 0.00407',
                            '25:doForceWidth = true',
                            '25:onMode = off',#decay of Higgs
                            '25:onIfMatch = 23 23',
                            'HiggsSM:gg2Httbar = on',
                            'HiggsSM:qqbar2Httbar = on',
                            '23:onMode = off',#decay of Z
                            '23:mMin = 2.0',
                            '23:onIfMatch = 11 11',
                            '23:onIfMatch = 13 13',
                            '23:onIfMatch = 15 15'
                            ]
