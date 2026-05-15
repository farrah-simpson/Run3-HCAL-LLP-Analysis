#!/bin/bash

# Update these!
output_basedir=/eos/home-g/gkopp/LLP_Analysis/MiniTuples/v5.4/
proxypath=~/private/x509up_u101898

for input_file in ../Ntuples_v5/InputFiles_HToSSTo4B_MH*L1triggers_v5.txt; do

  filetag=`basename $input_file .txt | sed 's/^InputFiles_//'`
  echo "Submitting job for: $input_files"
  echo "python3 condor_run.py -i $input_file -o $output_basedir$filetag -p $proxypath  -f $filetag"
  python3 condor_run.py -i $input_file -o $output_basedir$filetag -p $proxypath  -f $filetag

done
