import uproot
import ROOT
import numpy as np
import argparse, os
import json
import awkward as ak

parser = argparse.ArgumentParser(description="W+Jets Selection Data vs MC tagger score comparison.")
parser.add_argument("-m", "--mc", required=True, help="Path to W+Jets MC ROOT file")
parser.add_argument("--inclusive", action="store_true", help="Use inclusive tagger")
parser.add_argument("--depth", action="store_true", help="Use depth tagger")
args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

cmsLabel = "#scale[1.0]{#bf{CMS}} #scale[0.8]{#it{Work in Progress}}"

xpos = 0.16
ypos = 0.85

folder = "./outPlots/DataMCTagger/"
os.makedirs(folder, exist_ok=True)
tree_name = "NoSel"

if args.depth:
    tagger_name = "Depth"
    score_var = "jet0_scores_depth_LLPanywhere"
    score_var_holder = "jet0_scores_depth_anywhere_updated" 
    threshold = 0.
elif args.inclusive:
    tagger_name = "Inclusive"
    score_var = "jet0_scores_inc_train80_updated" 
    threshold = 0. 
else:
    raise ValueError("Please specify either --depth or --inclusive")

print(f"Using tagger: {tagger_name}")

data_file1 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Cv1_allscores_NoSel_scores.root")
data_file2 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Cv2_allscores_NoSel_scores.root")
data_file3 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Cv3_allscores_NoSel_scores.root")
data_file4 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Cv4_allscores_NoSel_scores.root")
data_file5 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Dv1_allscores_NoSel_scores.root")
data_file6 = uproot.open("/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.16/minituples_Zmu_2023Dv2_allscores_NoSel_scores.root")

mc_file   = uproot.open(args.mc) 

data_tree1 = data_file1[tree_name]
data_tree2 = data_file2[tree_name]
data_tree3 = data_file3[tree_name]
data_tree4 = data_file4[tree_name]
data_tree5 = data_file5[tree_name]
data_tree6 = data_file6[tree_name]

data_tree_comb = ak.concatenate([
    data_tree1.arrays(library="ak"),
    data_tree2.arrays(library="ak"),
    data_tree3.arrays(library="ak"),
    data_tree4.arrays(library="ak"),
    data_tree5.arrays(library="ak"),
    data_tree6.arrays(library="ak"),
], axis=0)

mc_tree   = mc_file[tree_name]

if tagger_name == "Depth": 
    data_score_comb  = data_tree_comb[score_var_holder].array(library="np")

#    data_score1  = data_tree1[score_var_holder].array(library="np")
#    data_score2  = data_tree2[score_var_holder].array(library="np")
#    data_score3  = data_tree3[score_var_holder].array(library="np")
#    data_score4  = data_tree4[score_var_holder].array(library="np")
#    data_score5  = data_tree5[score_var_holder].array(library="np")
#    data_score6  = data_tree6[score_var_holder].array(library="np")
    mc_score   = mc_tree[score_var_holder].array(library="np")
else: 
    data_score_comb  = data_tree_comb[score_var].array(library="np")

#    data_score1  = data_tree1[score_var].array(library="np")
#    data_score2  = data_tree2[score_var].array(library="np")
#    data_score3  = data_tree3[score_var].array(library="np")
#    data_score4  = data_tree4[score_var].array(library="np")
#    data_score5  = data_tree5[score_var].array(library="np")
#    data_score6  = data_tree6[score_var].array(library="np")
    mc_score   = mc_tree[score_var].array(library="np")

data_pass_comb = data_tree_comb["Pass_WPlusJets"].array(library="np")

#data_pass1 = data_tree1["Pass_WPlusJets"].array(library="np")
#data_pass2 = data_tree2["Pass_WPlusJets"].array(library="np")
#data_pass3 = data_tree3["Pass_WPlusJets"].array(library="np")
#data_pass4 = data_tree4["Pass_WPlusJets"].array(library="np")
#data_pass5 = data_tree5["Pass_WPlusJets"].array(library="np")
#data_pass6 = data_tree6["Pass_WPlusJets"].array(library="np")

mc_pass   = mc_tree["Pass_WPlusJets"].array(library="np")

bins = 10
h_data_comb = ROOT.TH1F("h_data_comb", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)

#h_data1 = ROOT.TH1F("h_data1", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#h_data2 = ROOT.TH1F("h_data2", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#h_data3 = ROOT.TH1F("h_data3", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#h_data4 = ROOT.TH1F("h_data4", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#h_data5 = ROOT.TH1F("h_data5", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#h_data6 = ROOT.TH1F("h_data6", f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)
#
h_mc   = ROOT.TH1F("h_mc",   f"{tagger_name} score;{tagger_name} score;Normalized entries", bins, 0, 1)

h_data_comb.Sumw2()

#h_data1.Sumw2()
#h_data2.Sumw2()
#h_data3.Sumw2()
#h_data4.Sumw2()
#h_data5.Sumw2()
#h_data6.Sumw2()

h_mc.Sumw2()
for val in data_score_comb[(data_pass_comb == 1)]:h_data_comb.Fill(float(val))

#for val in data_score1[(data_pass1 == 1)]:h_data1.Fill(float(val))
#for val in data_score2[(data_pass2 == 1)]:h_data2.Fill(float(val))
#for val in data_score3[(data_pass3 == 1)]:h_data3.Fill(float(val))
#for val in data_score4[(data_pass4 == 1)]:h_data4.Fill(float(val))
#for val in data_score5[(data_pass5 == 1)]:h_data5.Fill(float(val))
#for val in data_score6[(data_pass6 == 1)]:h_data6.Fill(float(val))

for val in mc_score[(mc_pass == 1)]:h_mc.Fill(float(val))

#h_data_raw = h_data.Clone("h_data_raw")
#h_mc_raw   = h_mc.Clone("h_mc_raw")
if h_data_comb.Integral() > 0: h_data_comb.Scale(1.0/h_data_comb.Integral())

#if h_data1.Integral() > 0: h_data1.Scale(1.0/h_data1.Integral())
#if h_data2.Integral() > 0: h_data2.Scale(1.0/h_data2.Integral())
#if h_data3.Integral() > 0: h_data3.Scale(1.0/h_data3.Integral())
#if h_data4.Integral() > 0: h_data4.Scale(1.0/h_data4.Integral())
#if h_data5.Integral() > 0: h_data5.Scale(1.0/h_data5.Integral())
#if h_data6.Integral() > 0: h_data6.Scale(1.0/h_data6.Integral())

if h_mc.Integral() > 0: h_mc.Scale(1.0/h_mc.Integral())

# --- build MC uncertainty band for top pad ---
h_mc_band = h_mc.Clone("h_mc_band")
h_mc_band.SetDirectory(0)
h_mc_band.SetFillColorAlpha(ROOT.kGray+1, 0.35)
h_mc_band.SetLineColor(ROOT.kGray+1)
h_mc_band.SetMarkerSize(0)

# --- build ratio uncertainty band: MC/MC = 1 with relative MC uncertainty ---
h_ratio_band = h_mc.Clone("h_ratio_band")
h_ratio_band.SetDirectory(0)
h_ratio_band.Reset("ICES")

for ibin in range(1, h_mc.GetNbinsX() + 1):
    mc_val = h_mc.GetBinContent(ibin)
    mc_err = h_mc.GetBinError(ibin)

    h_ratio_band.SetBinContent(ibin, 1.0)
    if mc_val > 0:
        h_ratio_band.SetBinError(ibin, mc_err / mc_val)
    else:
        h_ratio_band.SetBinError(ibin, 0.0)

h_ratio_band.SetFillColorAlpha(ROOT.kGray+1, 0.35)
h_ratio_band.SetLineColor(ROOT.kGray+1)
#h_ratio_band.SetMarkerSize(0)


ymax = max(h_data_comb.GetMaximum(), h_mc.GetMaximum())
h_data_comb.SetMaximum(1.9 * ymax)

h_ratio_comb = h_data_comb.Clone("h_ratio_comb")
h_ratio_comb.Divide(h_mc)

#h_ratio1 = h_data1.Clone("h_ratio1")
#h_ratio1.Divide(h_mc)
#
#h_ratio2 = h_data2.Clone("h_ratio2")
#h_ratio2.Divide(h_mc)
#
#h_ratio3 = h_data3.Clone("h_ratio3")
#h_ratio3.Divide(h_mc)
#
#h_ratio4 = h_data4.Clone("h_ratio4")
#h_ratio4.Divide(h_mc)
#
#h_ratio5 = h_data5.Clone("h_ratio5")
#h_ratio5.Divide(h_mc)
#
#h_ratio6 = h_data6.Clone("h_ratio6")
#h_ratio6.Divide(h_mc)


c = ROOT.TCanvas("c", "", 800, 700)
ROOT.gStyle.SetOptStat(0)
pad1 = ROOT.TPad("pad1", "", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0)
pad1.Draw()
pad1.SetLogy()
pad1.cd()
colors = [
    ROOT.kRed,
    ROOT.kBlue,
    ROOT.kCyan,
    ROOT.kGreen+2,
    ROOT.kMagenta,
    ROOT.kOrange+1
]

#markers = [20, 21, 22, 23, 33, 34]
#data_hists  = [h_data1, h_data2, h_data3, h_data4, h_data5, h_data6]
#ratio_hists = [h_ratio1, h_ratio2, h_ratio3, h_ratio4, h_ratio5, h_ratio6]
#for i in range(len(data_hists)):
#    data_hists[i].SetLineColor(colors[i])
#    data_hists[i].SetMarkerColor(colors[i])
#    data_hists[i].SetMarkerStyle(markers[i])
#    data_hists[i].SetLineWidth(2)

h_data_comb.SetLineColor(colors[0])
h_data_comb.SetMarkerColor(colors[0])
h_data_comb.SetMarkerStyle(markers[0])
h_data_comb.SetLineWidth(2)

h_mc.SetLineColor(ROOT.kBlack)
h_mc.SetLineWidth(2)
h_mc.SetTitle("")

h_mc.Draw("HIST")
h_mc_band.Draw("E2 SAME")   # <- error band
h_mc.Draw("HIST SAME")      # redraw line on top

h_data_comb.Draw("E SAME")
#h_data1.Draw("E SAME")
#h_data2.Draw("E SAME")
#h_data3.Draw("E SAME")
#h_data4.Draw("E SAME")
#h_data5.Draw("E SAME")
#h_data6.Draw("E SAME")

cutLabel = f"{tagger_name} DNN score"

legend = ROOT.TLegend(0.5, 0.55, 0.9, 0.9)
legend.SetTextSize(0.045)

#legend.AddEntry(h_data1, "Run 2023Cv1", "l")
#legend.AddEntry(h_data2, "Run 2023Cv2", "l")
#legend.AddEntry(h_data3, "Run 2023Cv3", "l")
#legend.AddEntry(h_data4, "Run 2023Cv4", "l")
#legend.AddEntry(h_data5, "Run 2023Dv1", "l")
#legend.AddEntry(h_data6, "Run 2023Dv2", "l")

legend.AddEntry(h_mc, "W+Jets MC", "l")
legend.AddEntry(h_data_comb, "Combined Run 2023", "lep")

legend.Draw()

stamp = ROOT.TLatex()
stamp.SetNDC()
stamp.SetTextFont(42)
stamp.SetTextSize(0.045)
stamp.DrawLatex(xpos, ypos, cmsLabel)

c.cd()
pad2 = ROOT.TPad("pad2", "", 0, 0.05, 1, 0.3)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.Draw()
pad2.cd()

for i in range(len(ratio_hists)):
    ratio_hists[i].SetLineColor(colors[i])
    ratio_hists[i].SetMarkerColor(colors[i])
    ratio_hists[i].SetMarkerStyle(markers[i])
    ratio_hists[i].SetLineWidth(2)

h_ratio_comb.SetTitle("")

h_ratio_comb.GetYaxis().SetTitle("Data / MC")
h_ratio_comb.GetYaxis().SetTitleSize(0.11)
h_ratio_comb.GetYaxis().SetLabelSize(0.095)
h_ratio_comb.GetYaxis().SetTitleOffset(0.42)
h_ratio_comb.GetYaxis().CenterTitle(True)
h_ratio_comb.GetYaxis().SetNdivisions(505)

h_ratio_comb.GetXaxis().SetTitle(f"{tagger_name} score")
h_ratio_comb.GetXaxis().SetTitleSize(0.12)
h_ratio_comb.GetXaxis().SetLabelSize(0.10)
h_ratio_comb.GetXaxis().SetTitleOffset(1.0)
h_ratio_comb.GetXaxis().SetNdivisions(506)

h_ratio_comb.GetXaxis().SetTickLength(0.08)
h_ratio_comb.GetYaxis().SetTickLength(0.04)

h_ratio_comb.SetMinimum(0.01)
h_ratio_comb.SetMaximum(1.99)


#h_ratio1.SetTitle("")
#
#h_ratio1.GetYaxis().SetTitle("Data / MC")
#h_ratio1.GetYaxis().SetTitleSize(0.11)
#h_ratio1.GetYaxis().SetLabelSize(0.095)
#h_ratio1.GetYaxis().SetTitleOffset(0.42)
#h_ratio1.GetYaxis().CenterTitle(True)
#h_ratio1.GetYaxis().SetNdivisions(505)
#
#h_ratio1.GetXaxis().SetTitle(f"{tagger_name} score")
#h_ratio1.GetXaxis().SetTitleSize(0.12)
#h_ratio1.GetXaxis().SetLabelSize(0.10)
#h_ratio1.GetXaxis().SetTitleOffset(1.0)
#h_ratio1.GetXaxis().SetNdivisions(506)
#
#h_ratio1.GetXaxis().SetTickLength(0.08)
#h_ratio1.GetYaxis().SetTickLength(0.04)
#
#h_ratio1.SetMinimum(0.01)
#h_ratio1.SetMaximum(1.99)

#h_ratio1.GetYaxis().SetTitle("Data/Bkg")
#h_ratio1.GetYaxis().SetTitleSize(0.2)
#h_ratio1.GetYaxis().SetLabelSize(0.2)
#h_ratio1.GetYaxis().SetTitleOffset(0.5)
#h_ratio1.GetXaxis().SetTitle(f"{tagger_name} tagger score")
#h_ratio1.GetXaxis().SetTitleSize(0.2)
#h_ratio1.GetXaxis().SetLabelSize(0.2)
#h_ratio1.GetYaxis().SetNdivisions(5)#404
#h_ratio1.GetXaxis().SetNdivisions(506)
#h_ratio1.SetMinimum(0.01)
#h_ratio1.SetMaximum(1.99)
#h_ratio1.Draw("E")

h_ratio_comb.Draw("E")
h_ratio_band.Draw("E2 SAME")     # <- ratio uncertainty band around 1

#h_ratio2.Draw("E SAME")
#h_ratio3.Draw("E SAME")
#h_ratio4.Draw("E SAME")
#h_ratio5.Draw("E SAME")
#h_ratio6.Draw("E SAME")

line = ROOT.TLine(0, 1.0, 1, 1.0)
line.SetLineColor(ROOT.kGray+2)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw("SAME")

pad2.Update()

outname = f"{folder}/{tagger_name}_Score_DataMC_combined.png"
c.SaveAs(outname)
print(f"Saved score plot: {outname}")

#sf = []
#sf_err = []
#
#for i in range(1, bins+1):
#    d = h_data.GetBinContent(i)
#    m = h_mc.GetBinContent(i)
#    de = h_data.GetBinError(i)
#    me = h_mc.GetBinError(i)
#
#    if m > 0:
#        sf_i = d/m
#        sf_e = sf_i * np.sqrt((de/d)**2 + (me/m)**2) if d>0 else 0
#    else:
#        sf_i = 0
#        sf_e = 0
#
#    sf.append(sf_i)
#    sf_err.append(sf_e)
#
#json_file = f"{folder}/{tagger_name}_Score_SF.json"
#with open(json_file, "w") as f:
#    json.dump({"sf": sf, "sf_err": sf_err}, f, indent=2)
#
#print(f"Saved SFs: {json_file}")
#
