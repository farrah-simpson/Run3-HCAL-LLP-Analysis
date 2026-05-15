#!/bin/bash

# find-replace v5.4 -> vx

echo "LLP MC"
hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_HToSSTo4B_350_160_CTau10000_scores.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/HToSSTo4B_MH350_MS160_CTau10000_L1triggers_v5/*NoSel_scores.root
hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_HToSSTo4B_350_80_CTau500_scores.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/HToSSTo4B_MH350_MS80_CTau500_L1triggers_v5/*NoSel_scores.root
hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_HToSSTo4B_250_120_CTau10000_scores.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/HToSSTo4B_MH250_MS120_CTau10000_L1triggers_v5/*NoSel_scores.root
hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_HToSSTo4B_125_50_CTau3000_scores.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/HToSSTo4B_MH125_MS50_CTau3000_L1triggers_v5/*NoSel_scores.root

# ================================================================================= #

echo "2023 displaced jet skim"
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Bv1.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Bv1_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Cv1.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Cv1_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Cv2.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Cv2_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Cv3.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Cv3_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Cv4.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Cv4_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Dv1.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Dv1_2025_04_08/*NoSel_scores.root
# hadd -j /eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v5.4/minituple_v5.4_LLPskim_Run2023Dv2.root /eos/user/g/gkopp/LLP_Analysis/MiniTuples/v5.4/LLPskim_2023Dv2_2025_04_08/*NoSel_scores.root