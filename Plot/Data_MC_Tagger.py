# To run: python Data_MC_overlay.py <path to data output of ../DisplacedHcalJetAnalyzer/util/DisplacedHcalJetAnalyzer.C> <path to MC output> 

import uproot
import awkward as ak
import numpy as np
import sys, os, argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams

debug = False

parser=argparse.ArgumentParser(description="Compare W+Jets Data vs MC tagger distributions.")

parser.add_argument("-d", "--data", help="Path to data ROOT file")
#parser.add_argument("-m", "--mc", help="Path to W+Jets MC ROOT file")
parser.add_argument("--inclusive",action="store_true", help="use inclusive tagger score") 
parser.add_argument("--depth",action="store_true", help="use depth tagger score") 

args = parser.parse_args()

rcParams.update({
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "axes.linewidth": 1.2,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 12,
    "legend.frameon": False,
    "figure.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

cmsLabel = r"$\bf{CMS}$ $\it{Run\ 3\ MC\ vs.\ Data}$"

xpos = 0.45
ypos = 0.85

folder = "./outPlots/DataMCTagger/"
os.makedirs(folder, exist_ok=True)

print("Starting plotting script")

infile_data = uproot.open(args.data)
#infile_MC = uproot.open(args.MC)

tree_name = "NoSel"

tagger_label = "inclusive" if args.inclusive else "depth"
print(f"Using {tagger_label} tagger distributions")

dept_score_threshold = 0.5
incl_score_threshold = 0.5 #we can use thresholds or use continuous score distributions

if args.depth:
    tagger_name = "Depth"
    score_var = "jet0_scores_depth_anywhere"
    threshold = dept_score_threshold
elif args.inclusive:
    tagger_name = "Inclusive"
    score_var = "jet0_scores_inc_train80" 
    threshold = incl_score_threshold
else:
    raise ValueError("Please specify either --depth or --inclusive")

variables = {
    "jet0_Pt": {"xlabel": "Leading jet $p_T$ [GeV]", "bins": np.linspace(0, 300, 50)},
    "jet0_Eta": {"xlabel": "Leading jet $\\eta$", "bins": np.linspace(-1.5, 1.5, 50)},
}

print("Making plots!")
for variable,label in variables.items():
    data_tree = infile_data[tree_name]
#    MC_tree = infile_MC[tree_name]
    
    data_score  = np.asarray(data_tree[score_var].array(library="np"))
#    mc_score  = np.asarray(mc_tree[score_var].array(library="np"))

    data_pass  = np.asarray(data_tree["Pass_WPlusJets"].array(library="np"))
    data_vals  = np.asarray(data_tree[variable].array(library="np"))
    data_mask = (data_pass == 1) & (data_score > threshold)
    data_vals = data_vals[data_mask]

#    mc_vals = np.asarray(mc_tree[variable].array(library="np"))
#    mc_vals   = np.asarray(mc_vals[mc_score>threshold])

    data_hist, bins = np.histogram(data_vals, bins=label["bins"], density=True)
#    mc_hist,   _    = np.histogram(mc_vals,   bins=label["bins"], density=True)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

#    ratio = np.divide(data_hist, mc_hist, out=np.zeros_like(data_hist), where=mc_hist > 0)

    # Plot
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(8, 7), gridspec_kw={'height_ratios':[3,1]}, sharex=True) 
    ax.step(bin_centers, data_hist, where="mid", label="Data", color="black", linewidth=1.6)
#    ax.step(bin_centers, mc_hist,   where="mid", label="MC", color="red",   linestyle="--", linewidth=1.6)

    ax.set_ylabel("Normalized entries")
    ax.legend()
    ax.text(xpos, ypos, cmsLabel, transform=ax.transAxes,
            fontsize=14, color="black", fontweight="bold")

#    rax.step(bin_centers, ratio, where="mid", color="black")
#    rax.axhline(1.0, color="red", linestyle="--")
#    rax.set_xlabel(label["xlabel"])
#    rax.set_ylabel("Data/MC")
#    rax.set_ylim(0.5, 1.5)

    # Save
    output = f"{folder}/{tagger_label}_{variable}.png"
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Saved: {output}")

print("Plotting tagger score distributions")

bins = np.linspace(0, 1, 40) #check binning
data_hist, bins = np.histogram(data_score, bins=bins, density=True)
#mc_hist, _ = np.histogram(mc_score, bins=bins, density=True)
bin_centers = 0.5*(bins[1:]+bins[:-1])

fig, ax = plt.subplots(figsize=(8,6))
ax.step(bin_centers, data_hist, where="mid", label="Data", color="black", linewidth=1.6)
#ax.step(bin_centers, mc_hist, where="mid", label="MC", color="red", linestyle="--", linewidth=1.6)
ax.set_xlabel(f"{tagger_name} tagger score")
ax.set_ylabel("Normalized entries")
ax.legend()
ax.text(xpos, ypos, cmsLabel, transform=ax.transAxes, fontsize=14, fontweight="bold")
plt.tight_layout()
outname = f"{folder}/{tagger_name.lower()}_score.png"
plt.savefig(outname, dpi=150)
plt.close()
print(f"Saved: {outname}")
