import argparse
import os
import numpy as np
import uproot
import ROOT

parser = argparse.ArgumentParser(description="Data vs MC plots for input variables.")
parser.add_argument("-d", "--data", required=True, help="Path to data ROOT file")
parser.add_argument("-m", "--mc", required=True, help="Path to MC ROOT file")
parser.add_argument("-o", "--outdir", default="./outPlots/DataMCInputs/", help="Output directory")
args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

cmsLabel = "#scale[1.0]{#bf{CMS}} #scale[0.8]{#it{Work in Progress}}"
xpos = 0.16
ypos = 0.85

os.makedirs(args.outdir, exist_ok=True)
tree_name = "PerJet_NoSel"

FEATURES = [
    "perJet_Eta",
    "perJet_Mass",
    "perJet_S_phiphi",
    "perJet_S_etaeta",
    "perJet_S_etaphi",
    "perJet_Tracks_dR",
    "perJet_Track0dR", "perJet_Track0dEta", "perJet_Track0dPhi",
    "perJet_Track1dR", "perJet_Track1dEta", "perJet_Track1dPhi",
    "perJet_Track2dR", "perJet_Track2dEta", "perJet_Track2dPhi",
    "perJet_Frac_Track0Pt", "perJet_Frac_Track1Pt", "perJet_Frac_Track2Pt",
    "perJet_EnergyFrac_Depth1", "perJet_EnergyFrac_Depth2",
    "perJet_EnergyFrac_Depth3", "perJet_EnergyFrac_Depth4",
    "perJet_LeadingRechitD",
    "perJet_Frac_LeadingRechitE", "perJet_Frac_SubLeadingRechitE", "perJet_Frac_SSubLeadingRechitE",
    "perJet_AllRechitE",
    "perJet_NeutralHadEFrac", "perJet_ChargedHadEFrac", "perJet_PhoEFrac",
    "perJet_EleEFrac", "perJet_MuonEFrac"
]

# Pretty axis labels
X_TITLES = {
    "perJet_Eta": "jet #eta",
    "perJet_Mass": "jet mass",
    "perJet_S_phiphi": "jet S_{#phi#phi}",
    "perJet_S_etaeta": "jet S_{#eta#eta}",
    "perJet_S_etaphi": "jet S_{#eta#phi}",
    "perJet_Tracks_dR": "#DeltaR(leading track, subleading track)",
    "perJet_Track0dR": "#DeltaR(jet, leading track)",
    "perJet_Track0dEta": "#Delta#eta(jet, leading track)",
    "perJet_Track0dPhi": "#Delta#phi(jet, leading track)",
    "perJet_Track1dR": "#DeltaR(jet, subleading track)",
    "perJet_Track1dEta": "#Delta#eta(jet, subleading track)",
    "perJet_Track1dPhi": "#Delta#phi(jet, subleading track)",
    "perJet_Track2dR": "#DeltaR(jet, sub-subleading track)",
    "perJet_Track2dEta": "#Delta#eta(jet, sub-subleading track)",
    "perJet_Track2dPhi": "#Delta#phi(jet, sub-subleading track)",
    "perJet_Frac_Track0Pt": "leading track fractional p_{T}",
    "perJet_Frac_Track1Pt": "subleading track fractional p_{T}",
    "perJet_Frac_Track2Pt": "sub-subleading track fractional p_{T}",
    "perJet_EnergyFrac_Depth1": "HCAL depth 1 energy fraction",
    "perJet_EnergyFrac_Depth2": "HCAL depth 2 energy fraction",
    "perJet_EnergyFrac_Depth3": "HCAL depth 3 energy fraction",
    "perJet_EnergyFrac_Depth4": "HCAL depth 4 energy fraction",
    "perJet_LeadingRechitD": "leading rechit depth",
    "perJet_Frac_LeadingRechitE": "leading rechit fractional energy",
    "perJet_Frac_SubLeadingRechitE": "subleading rechit fractional energy",
    "perJet_Frac_SSubLeadingRechitE": "sub-subleading rechit fractional energy",
    "perJet_AllRechitE": "total HCAL rechit energy",
    "perJet_NeutralHadEFrac": "neutral hadron energy fraction",
    "perJet_ChargedHadEFrac": "charged hadron energy fraction",
    "perJet_PhoEFrac": "photon energy fraction",
    "perJet_EleEFrac": "electron energy fraction",
    "perJet_MuonEFrac": "muon energy fraction",
}

# Manual binning where natural limits are known
BINNING = {
    "perJet_Eta": (30, -2.0, 2.0),
    "perJet_Mass": (30, 0.0, 200.0),
    "perJet_S_phiphi": (30, 0.0, 0.3),
    "perJet_S_etaeta": (15, 0.0, 0.25),
    "perJet_S_etaphi": (30, 0.0, 0.15),
    "perJet_Tracks_dR": (30, 0.0, 1.5),
    "perJet_Track0dR": (30, 0.0, 1.0),
    "perJet_Track1dR": (15, 0.0, 0.7),
    "perJet_Track2dR": (30, 0.0, 1.0),
    "perJet_Track0dEta": (30, -0.5, 0.5),
    "perJet_Track1dEta": (30, -0.5, 0.5),
    "perJet_Track2dEta": (30, -0.5, 0.5),
    "perJet_Track0dPhi": (30, -0.5, 0.5),
    "perJet_Track1dPhi": (30, -0.5, 0.5),
    "perJet_Track2dPhi": (30, -0.5, 0.5),
    "perJet_Frac_Track0Pt": (30, 0.0, 1.0),
    "perJet_Frac_Track1Pt": (30, 0.0, 1.0),
    "perJet_Frac_Track2Pt": (30, 0.0, 1.0),
    "perJet_EnergyFrac_Depth1": (30, 0.0, 1.0),
    "perJet_EnergyFrac_Depth2": (30, 0.0, 1.0),
    "perJet_EnergyFrac_Depth3": (30, 0.0, 1.0),
    "perJet_EnergyFrac_Depth4": (30, 0.0, 1.0),
    "perJet_LeadingRechitD": (5, 0.5, 5.5),
    "perJet_Frac_LeadingRechitE": (30, 0.0, 1.0),
    "perJet_Frac_SubLeadingRechitE": (30, 0.0, 1.0),
    "perJet_Frac_SSubLeadingRechitE": (30, 0.0, 1.0),
    "perJet_AllRechitE": (30, 0.0, 500.0),
    "perJet_NeutralHadEFrac": (30, 0.0, 1.0),
    "perJet_ChargedHadEFrac": (30, 0.0, 1.0),
    "perJet_PhoEFrac": (30, 0.0, 1.0),
    "perJet_EleEFrac": (30, 0.0, 1.0),
    "perJet_MuonEFrac": (30, 0.0, 1.0),
}

def sanitize_name(name):
    return name.replace("/", "_").replace(" ", "_")

def flatten_array(arr):
    arr = np.asarray(arr)
    if arr.dtype == object:
        pieces = []
        for x in arr:
            x = np.asarray(x)
            if x.size > 0:
                pieces.append(x.reshape(-1))
        return np.concatenate(pieces) if pieces else np.array([], dtype=float)
    return arr.reshape(-1)

def finite_values(arr):
    arr = flatten_array(arr)
    return arr[np.isfinite(arr)]

def choose_binning(var, data_vals, mc_vals):
    if var in BINNING:
        return BINNING[var]

    vals = np.concatenate([data_vals, mc_vals]) if (len(data_vals) + len(mc_vals)) > 0 else np.array([0.0, 1.0])
    vals = vals[np.isfinite(vals)]
    if len(vals) == 0:
        return (30, 0.0, 1.0)

    xmin = np.percentile(vals, 1)
    xmax = np.percentile(vals, 99)

    if xmin == xmax:
        xmin -= 1.0
        xmax += 1.0

    return (30, float(xmin), float(xmax))

def fill_hist(hist, values):
    for val in values:
        hist.Fill(float(val))

def make_plot(var, data_vals, mc_vals, outdir):
    bins, xmin, xmax = choose_binning(var, data_vals, mc_vals)
    xtitle = X_TITLES.get(var, var)

    h_data = ROOT.TH1F(f"h_data_{sanitize_name(var)}", "", bins, xmin, xmax)
    h_mc   = ROOT.TH1F(f"h_mc_{sanitize_name(var)}", "", bins, xmin, xmax)
    h_data.Sumw2()
    h_mc.Sumw2()

    fill_hist(h_data, data_vals)
    fill_hist(h_mc, mc_vals)

    if h_data.Integral() > 0:
        h_data.Scale(1.0 / h_data.Integral())
    if h_mc.Integral() > 0:
        h_mc.Scale(1.0 / h_mc.Integral())

    ymax = max(h_data.GetMaximum(), h_mc.GetMaximum(), 1e-4)

    c = ROOT.TCanvas(f"c_{sanitize_name(var)}", "", 800, 700)

    pad1 = ROOT.TPad(f"pad1_{sanitize_name(var)}", "", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)
    pad1.Draw()
    pad1.SetLogy()
    pad1.cd()

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(0.8)

    h_mc.SetLineColor(ROOT.kRed)
    h_mc.SetLineStyle(2)
    h_mc.SetLineWidth(2)

    h_data.SetTitle("")
    h_data.GetYaxis().SetTitle("Normalized entries")
    h_data.SetMaximum(5.0 * ymax)
    h_data.SetMinimum(max(1e-5, 0.1 * min([x for x in [h_data.GetMinimum(1e-9), h_mc.GetMinimum(1e-9)] if x > 0] + [1e-5])))

    h_data.Draw("E")
    h_mc.Draw("HIST SAME")

    legend = ROOT.TLegend(0.60, 0.70, 0.85, 0.85)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.AddEntry(h_data, "Data (Z #rightarrow #mu#mu)", "lep")
    legend.AddEntry(h_mc, "W+jets MC", "l")
    legend.Draw()

    stamp = ROOT.TLatex()
    stamp.SetNDC()
    stamp.SetTextFont(42)
    stamp.SetTextSize(0.045)
    stamp.DrawLatex(xpos, ypos, cmsLabel)

    label = ROOT.TLatex()
    label.SetNDC()
    label.SetTextFont(42)
    label.SetTextSize(0.04)
    label.DrawLatex(0.16, 0.79, xtitle)

    c.cd()
    pad2 = ROOT.TPad(f"pad2_{sanitize_name(var)}", "", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.3)
    pad2.Draw()
    pad2.cd()

    h_ratio = h_data.Clone(f"h_ratio_{sanitize_name(var)}")
    h_ratio.Divide(h_mc)

    h_ratio.SetTitle("")
    h_ratio.GetYaxis().SetTitle("Data/MC")
    h_ratio.GetYaxis().SetTitleSize(0.09)
    h_ratio.GetYaxis().SetLabelSize(0.08)
    h_ratio.GetYaxis().SetTitleOffset(0.5)
    h_ratio.GetYaxis().SetNdivisions(5)

    h_ratio.GetXaxis().SetTitle(xtitle)
    h_ratio.GetXaxis().SetTitleSize(0.10)
    h_ratio.GetXaxis().SetLabelSize(0.09)
    h_ratio.GetXaxis().SetNdivisions(506)

    ratio_min = h_ratio.GetMinimum()
    ratio_max = h_ratio.GetMaximum()
    max_dev = max(abs(ratio_max - 1), abs(ratio_min - 1))

    h_ratio.SetMinimum(1 - max_dev)
    h_ratio.SetMaximum(1 + max_dev)
    h_ratio.SetMarkerStyle(20)
    h_ratio.Draw("E")

    line = ROOT.TLine(xmin, 1.0, xmax, 1.0)
    line.SetLineColor(ROOT.kGray + 2)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw("SAME")

    pad2.Update()

    outname = os.path.join(outdir, f"{sanitize_name(var)}_DataMC.png")
    c.SaveAs(outname)
    print(f"Saved: {outname}")

    # clean up
    del c, pad1, pad2, h_data, h_mc, h_ratio

print("Opening files...")
data_file = uproot.open(args.data)
mc_file   = uproot.open(args.mc)

data_tree = data_file[tree_name]
mc_tree   = mc_file[tree_name]

print("Reading selection...")
data_pass = data_tree["Pass_WPlusJets"].array(library="np")
mc_pass   = mc_tree["Pass_WPlusJets"].array(library="np")

for var in FEATURES:
    print(f"Processing {var} ...")

    if var not in data_tree.keys():
        print(f"  -> Skipping {var}: not found in data tree")
        continue
    if var not in mc_tree.keys():
        print(f"  -> Skipping {var}: not found in MC tree")
        continue

    data_arr = data_tree[var].array(library="np")
    mc_arr   = mc_tree[var].array(library="np")

    # event selection
    data_sel = data_arr[data_pass == 1]
    mc_sel   = mc_arr[mc_pass == 1]

    data_vals = finite_values(data_sel)
    mc_vals   = finite_values(mc_sel)

    if len(data_vals) == 0 and len(mc_vals) == 0:
        print(f"  -> Skipping {var}: no valid entries after selection")
        continue

    make_plot(var, data_vals, mc_vals, args.outdir)

print("Done.")
