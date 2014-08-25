#!/bin/bash

rm $1_1_1_weights.root

for i in {10801..10852}
  do
  ./../../../get_pdfreweight.exe $1_1_1.root $i
done

# source reweight_sth.sh ttH > tmp_ttH.txt &
# source reweight_sth.sh ZH  > tmp_ZH.txt  &
# source reweight_sth.sh WH  > tmp_WH.txt  &
# source reweight_sth.sh ggH > tmp_ggH.txt &
# source reweight_sth.sh ggH_hfact > tmp_ggH_hfact.txt &
# source reweight_sth.sh VBFH125 > VBFH125.txt &

# source reweight_sth.sh minlo_HJ_mH125  > minlo_HJ_mH125.txt  & 
# source reweight_sth.sh minlo_HJJ_mH125 > minlo_HJJ_mH125.txt &

# ./../../../get_pdfreweight.exe ttH_1_1.root 10801
# ./../../../get_pdfreweight.exe ttH_1_1.root 10802
# ./../../../get_pdfreweight.exe ttH_1_1.root 10803
# ./../../../get_pdfreweight.exe ttH_1_1.root 10804
# ./../../../get_pdfreweight.exe ttH_1_1.root 10805
# ./../../../get_pdfreweight.exe ttH_1_1.root 10806
# ./../../../get_pdfreweight.exe ttH_1_1.root 10807
# ./../../../get_pdfreweight.exe ttH_1_1.root 10808
# ./../../../get_pdfreweight.exe ttH_1_1.root 10809
# ./../../../get_pdfreweight.exe ttH_1_1.root 10810
# ./../../../get_pdfreweight.exe ttH_1_1.root 10811
# ./../../../get_pdfreweight.exe ttH_1_1.root 10812
# ./../../../get_pdfreweight.exe ttH_1_1.root 10813
# ./../../../get_pdfreweight.exe ttH_1_1.root 10814
# ./../../../get_pdfreweight.exe ttH_1_1.root 10815
# ./../../../get_pdfreweight.exe ttH_1_1.root 10816
# ./../../../get_pdfreweight.exe ttH_1_1.root 10817
# ./../../../get_pdfreweight.exe ttH_1_1.root 10818
# ./../../../get_pdfreweight.exe ttH_1_1.root 10819
# ./../../../get_pdfreweight.exe ttH_1_1.root 10820
# ./../../../get_pdfreweight.exe ttH_1_1.root 10821
# ./../../../get_pdfreweight.exe ttH_1_1.root 10822
# ./../../../get_pdfreweight.exe ttH_1_1.root 10823
# ./../../../get_pdfreweight.exe ttH_1_1.root 10824
# ./../../../get_pdfreweight.exe ttH_1_1.root 10825
# ./../../../get_pdfreweight.exe ttH_1_1.root 10826
# ./../../../get_pdfreweight.exe ttH_1_1.root 10827
# ./../../../get_pdfreweight.exe ttH_1_1.root 10828
# ./../../../get_pdfreweight.exe ttH_1_1.root 10829
# ./../../../get_pdfreweight.exe ttH_1_1.root 10830
# ./../../../get_pdfreweight.exe ttH_1_1.root 10831
# ./../../../get_pdfreweight.exe ttH_1_1.root 10832
# ./../../../get_pdfreweight.exe ttH_1_1.root 10833
# ./../../../get_pdfreweight.exe ttH_1_1.root 10834
# ./../../../get_pdfreweight.exe ttH_1_1.root 10835
# ./../../../get_pdfreweight.exe ttH_1_1.root 10836
# ./../../../get_pdfreweight.exe ttH_1_1.root 10837
# ./../../../get_pdfreweight.exe ttH_1_1.root 10838
# ./../../../get_pdfreweight.exe ttH_1_1.root 10839
# ./../../../get_pdfreweight.exe ttH_1_1.root 10840
# ./../../../get_pdfreweight.exe ttH_1_1.root 10841
# ./../../../get_pdfreweight.exe ttH_1_1.root 10842
# ./../../../get_pdfreweight.exe ttH_1_1.root 10843
# ./../../../get_pdfreweight.exe ttH_1_1.root 10844
# ./../../../get_pdfreweight.exe ttH_1_1.root 10845
# ./../../../get_pdfreweight.exe ttH_1_1.root 10846
# ./../../../get_pdfreweight.exe ttH_1_1.root 10847
# ./../../../get_pdfreweight.exe ttH_1_1.root 10848
# ./../../../get_pdfreweight.exe ttH_1_1.root 10849
# ./../../../get_pdfreweight.exe ttH_1_1.root 10850
# ./../../../get_pdfreweight.exe ttH_1_1.root 10851
# ./../../../get_pdfreweight.exe ttH_1_1.root 10852
# end at 52.