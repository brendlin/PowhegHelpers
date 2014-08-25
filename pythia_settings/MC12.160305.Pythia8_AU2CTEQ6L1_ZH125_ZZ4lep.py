###
### For reference only!
###

evgenConfig.description = "PYTHIA8 ZH H->ZZ->4lep with AU2 CTEQ6L1"
evgenConfig.keywords = ["SMhiggs", "ZH", "Z","leptonic"]

#include("MC12JobOptions/Pythia8_AU2_CT10_Common.py")
include("MC12JobOptions/Pythia8_AU2_CTEQ6L1_Common.py")
include("MC12JobOptions/Pythia8_Photos.py" )

topAlg.Pythia8.Commands += ['25:m0 = 125',
                            '25:mWidth = 0.00407',
                            '25:onMode = off',
                            '25:doForceWidth = true',
                            '25:onIfMatch = 23 23',
                            'HiggsSM:ffbar2HZ = on',
                            '23:mMin = 2.0',
                            '23:onMode = off',
                            '23:onIfAny = 1 2 3 4 5 6 11 12 13 14 15 16'
                            ]

include("MC12JobOptions/XtoVVDecayFilter.py")
topAlg.XtoVVDecayFilter.PDGGrandParent = 25
topAlg.XtoVVDecayFilter.PDGParent = 23
topAlg.XtoVVDecayFilter.StatusParent = 22
topAlg.XtoVVDecayFilter.PDGChild1 = [11,13,15]
topAlg.XtoVVDecayFilter.PDGChild2 = [11,13,15]
