import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, Dropout, MaxPooling1D, BatchNormalization, AveragePooling1D
from tensorflow.keras.optimizers import Nadam, Adam
import pandas as pd
import matplotlib.pyplot as plt
import uproot

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle
from itertools import combinations
from sklearn.metrics import roc_curve, auc
import csv

import sys, os, argparse, time, errno
import os.path

testing_mode = False
debug_mode = True
inclusive_only = True

perJet = False
num_jets = 1 if perJet else 4 # in v3.13 only 4 jets are saved! In earlier versions, 6 jets are saved

CONSTANTS = pd.read_csv("norm_constants_v3.csv")

FEATURES = ['perJet_Eta', 'perJet_Mass', 
       'perJet_S_phiphi', 'perJet_S_etaeta', 'perJet_S_etaphi', 
       'perJet_Tracks_dR', 
       'perJet_Track0dR', 'perJet_Track0dEta', 'perJet_Track0dPhi', 
       'perJet_Track1dR', 'perJet_Track1dEta', 'perJet_Track1dPhi',
       'perJet_Track2dR', 'perJet_Track2dEta', 'perJet_Track2dPhi',
       'perJet_Frac_Track0Pt', 'perJet_Frac_Track1Pt', 'perJet_Frac_Track2Pt',
       'perJet_EnergyFrac_Depth1', 'perJet_EnergyFrac_Depth2', 'perJet_EnergyFrac_Depth3', 'perJet_EnergyFrac_Depth4', 
       'perJet_LeadingRechitD', 
       'perJet_Frac_LeadingRechitE', 'perJet_Frac_SubLeadingRechitE', 'perJet_Frac_SSubLeadingRechitE', 
       'perJet_AllRechitE', 
       'perJet_NeutralHadEFrac', 'perJet_ChargedHadEFrac', 'perJet_PhoEFrac', 'perJet_EleEFrac', 'perJet_MuonEFrac']


class DataProcessor:
    def __init__(self, num_classes=2, mode=None, sel=True, tree="NoSel"): #counting from 0 
        self.return_value_bkg = num_classes
        self.return_sig_value = num_classes - 1
        self.num_classes = num_classes
        self.mode = mode
        self.tree = tree
        self.sel = sel
    
    def load_data(self, input_files=None, filepath=None):
        
        # need a mode that doesn't pre-classify them but just loads the data and then you can get it to predict
        # and returns the dataframe unchanged so filenames are the same
        print("Loading Data...")
        
        filter_name = "*"

        fps = [filepath + input_files] if input_files is not None else []
        df = [] #pd.DataFrame()
        
        # aggregating all signal events
        for file in fps:
            sig = uproot.open(file)[self.tree]
            print(f"Opened {file}")
            print(f"Evaluating on tree: {self.tree}")
            sig = sig.arrays(filter_name=filter_name, library="pd") 
            df.append(sig)
        self.df = pd.concat(df) if df else pd.DataFrame()
        
        print("Loaded Data")
        
    def no_selections_concatenate(self):
        self.cumulative_df = self.df
        print("-------------------All Data // No Cuts applied---------")
        print(self.cumulative_df.describe())

    def process_data(self):
        
        print("Processing...")

        all_normed_data = []
        all_labels = []
        all_jet_pt = []

        for jet in range(num_jets): 
            if not perJet:
                new_features = [i.replace('perJet','jet'+str(jet)) for i in FEATURES] # list comprehension 
                feature_dictionary = dict(zip(new_features, FEATURES))
            else: new_features = FEATURES
        
            labels = None 
            if not self.mode and self.sel:
                self.cumulative_df = self.cumulative_df.sample(frac=1, random_state=42).reset_index(drop=True) # shuffling
                labels = self.cumulative_df["classID"].values
            
            data = self.cumulative_df[new_features]
            print(data.describe())
            jet_pt = self.cumulative_df["jet"+str(jet)+"_Pt"].values
            jet_trained_on = self.cumulative_df
            # in data, would like to rename jetX to perJet to work with the input files
            if not perJet: data = data.rename(columns=feature_dictionary)

            normed_data = pd.DataFrame()
            for feature in data.columns:
                # giving data a nominal 0 value if bad, but scores are -9999 if jet is not valid
                mask_condition = (data[feature] <= -900) | (data[feature] >= 900)
                data.loc[mask_condition, feature] = 0  # Default to 0 for matching entries
                normed_data[feature] = (data[feature] - CONSTANTS[feature][0])/ CONSTANTS[feature][1]

            print(normed_data.describe())
        
            print("Processing Complete")

            all_normed_data.append(normed_data)
            all_labels.append(labels)
            all_jet_pt.append(jet_pt)
        
        # return normed data, labels, and a list of rows are ok (energy is positive) and which are not (energy is -9999.9)
        return all_normed_data, all_labels, all_jet_pt
    
    def default_variables(self, jet_index = 0):
        # assumes that you have already loaded the files and applied safety selections
        # for manual input of other useful variables not included in safety selection:
        useful_variables = ['perJet_Track0dzToPV', 'perJet_Track0dzOverErr', 'perJet_Track0dxyToBS', 'perJet_Track0dxyOverErr',
                            'perJet_Track1dzToPV', 'perJet_Track1dzOverErr', 'perJet_Track1dxyToBS', 'perJet_Track1dxyOverErr', 
                            'perJet_Track2dzToPV', 'perJet_Track2dzOverErr', 'perJet_Track2dxyToBS', 'perJet_Track2dxyOverErr']
        # rename to jet i 
        useful_variables = [i.replace('perJet','jet'+str(jet_index)) for i in useful_variables] # list comprehension
        for useful_variable in useful_variables:
            data = self.cumulative_df[[useful_variable]].copy()
            mask_condition = (data[useful_variable] <= -900) | (data[useful_variable] >= 900)
            data.loc[mask_condition, useful_variable] = 0  # Default to 0 for matching entries
    
    def write_to_root(self, scores, scores_inc, filename, labels=None):
        filename = f"{filename[:-5]}_{self.tree}_scores.root" # remove .root from initial filename
        # TODO: know the first time you open this file, call recreate before even starting (when loop over filenames, before loop over tree names), and then here call update
        dataframe = self.cumulative_df
        if self.num_classes == 2:
            for i in range(num_jets):
                dataframe['jet'+str(i)+'_scores12'] = scores[i][:, 0]
                dataframe['jet'+str(i)+'_scores34'] = scores[i][:, 1]
                dataframe['jet'+str(i)+'_scoresbkg'] = scores[i][:, 2]
                dataframe['jet'+str(i)+'_scores12_inc'] = scores_inc[i][:, 0]
                dataframe['jet'+str(i)+'_scores34_inc'] = scores_inc[i][:, 1]
                dataframe['jet'+str(i)+'_scoresbkg_inc'] = scores_inc[i][:, 2]
        elif self.num_classes == 1:
            for i in range(num_jets):
                if not inclusive_only: dataframe['jet'+str(i)+'_scores'] = scores[i][:, 0] # 0 is the signal class # don't write depth scores when only evaluating inclusive DNN
                dataframe['jet'+str(i)+'_scores_inc'] = scores_inc[i][:, 0] # 0 is the signal class
        if labels is not None:
            dataframe['classID'] = labels
        if os.path.isfile(filename): 
            with uproot.update(filename) as f:
                # TODO: propagate correct treename through to this point
                f[self.tree] = {key: dataframe[key] for key in dataframe.columns}
        else:  
            with uproot.recreate(filename) as f:
                f[self.tree] = {key: dataframe[key] for key in dataframe.columns}
                
        print(f"Wrote to ROOT file: {filename}")
        f.close()            
        
class ModelHandler:
    def __init__(self, num_classes=3, num_layers=3, optimizer="adam", lr=0.00027848106048644665, model_name="dense_model_v4.keras"):
        
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.model_name = model_name
        self.colors = ['red', 'blue', 'green']
        
        self.names = ["HCAL12", "HCAL34", "bkg"] if num_classes == 3 else ["HCAL", "bkg"]
    
        if optimizer == "adam":
            self.optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
        elif optimizer == 'adamax':
            self.optimizer = tf.keras.optimizers.Adamax(learning_rate=lr)
        elif optimizer == 'nadam':
            self.optimizer = tf.keras.optimizers.Nadam(learning_rate=lr)
        else:
            self.optimizer= tf.keras.optimizers.SGD(learning_rate=lr)    
            
    def get_model(self):
        return self.model
        
    def load(self):
        self.model = tf.keras.models.load_model(self.model_name)
    
    def test(self, X_test, y_test):
        preds = self.model.predict(X_test)
        predictions = np.argmax(preds, axis=1)
        accuracy = np.sum(predictions == y_test) / len(y_test)
        print("Total Test Samples: ", len(y_test))
        print("Accuracy: ", accuracy)
        
        self.roc_data = (y_test, preds)
        return self.roc_data
    
    def predict(self, predicting_data, labels=None):
        preds = self.model.predict(predicting_data)
        if labels is not None:
            print("Accuracy: ", np.sum(np.argmax(preds, axis=1) == labels) / len(labels) )
        return preds
    
    def save_roc_data(self, fpr, tpr):
        roc_data = zip(fpr, tpr)
        with open("roc_binary_data.csv", "w", newline='') as f:
            writer = csv.writer(f)

            # Write the header
            writer.writerow(["FPR", "TPR"])

            # Write all rows at once
            writer.writerows(roc_data)
            print("wrote to file")  

class Runner:
    def __init__(self, input_files=None, filepath=None, mode="train", num_classes=3, inclusive=False, load=True, tree="NoSel"):
        self.mode = mode
        self.num_classes = num_classes
        self.inclusive = inclusive
        self.load = load
        self.sig = input_files
        self.path = filepath
        self.tree = tree
        self.model_name = "dense_model_v4.keras"
    
    def evaluate_scores(self): # this code used to be in run_file_evaluation -- still testing
        print("Determining Scores")
        predicting_data, labels, jet_pt = self.processor.process_data()
        # depth
        # handler = ModelHandler(num_classes=self.num_classes, model_name=self.model_name)
        handler = ModelHandler(num_classes=self.num_classes, model_name="depth_model_v4.keras")
        print("Loading the depth model")
        handler.load()
        preds = [ handler.predict(predicting_data[i], labels[i]) for i in range(num_jets) ]
        # inclusive
        handler_inc = ModelHandler(num_classes=self.num_classes, model_name="inclusive_model_v4.keras")
        print("Loading the inclusive model")
        handler_inc.load()
        preds_inc = [ handler_inc.predict(predicting_data[i], labels[i]) for i in range(num_jets) ]
        # data is predicting_data, jet pT is jet_pt, scores are preds, all indexed by jet (6 total)
        # to print whole data table, predicting_data[0], to print just values in a list, predicting_data[0].values

        # check if predicting_data[i] has a valid jet. If so, keep DNN score. If not, set score = -9999
        for i in range(num_jets): # evaluate for all 6 jets
            for jet in range(len(predicting_data[i])): # evaluate for every jet, if valid
                if (jet_pt[i][jet] < -9000): # if jet pT is -9999.9, replace score with -9999.9
                    preds[i][jet] = [-9999.9, -9999.9]
                    preds_inc[i][jet] = [-9999.9, -9999.9]
                # do not score jets that were used in the training, based on split with jet_Pt
                # if ((jet_pt[i][jet] * 1000).astype(int) % 10 < 4): # extract 1000th place. Trained on "train_mask = randFloat_values < 4"
                #     # preds[i][jet] = [-9999.9, -9999.9] # depth scores are ok, because they rely on CR
                #     preds_inc[i][jet] = [-9999.9, -9999.9]
                if debug_mode:
                    print("jet pT = ")
                    print(jet_pt[i][jet])
                    print("inclusive scores = ")
                    print(preds_inc[i][jet])
                    print("depth scores = ")
                    print(preds[i][jet])

        self.processor.write_to_root(preds, preds_inc, self.fname, labels=None)

    def run_file_evaluation(self):
        print("Evaluating Single File")
        # processes one file per run for now
        print("Loaded files")
        if self.load:
            self.processor = DataProcessor(num_classes=self.num_classes - 1, mode="filewrite", sel=False, tree=self.tree)
            self.processor.load_data(input_files=self.sig, filepath=self.path)
        self.processor.no_selections_concatenate() # automatically inclusive
        self.fname = self.sig
        self.evaluate_scores()
        
    def run(self):
        if self.mode == "train":
            self.run_training()
        elif self.mode == "eval":
            self.run_evaluation()
        elif self.mode == "filewrite":
            self.run_file_evaluation()
        else:
            print("No Valid Mode Entered")
            
    def set_inclusive(self, inclusive=False):
        self.inclusive = inclusive
        return
    
    def set_load(self,load=True):
        self.load = load
    
    def set_model_name(self, model_name="dense_model_v4.keras"):
        self.model_name = model_name
        
        
def main():
    input_files = "test.root"
    filepath = "./"
    if testing_mode: filepath = "/eos/cms/store/group/phys_exotica/HCAL_LLP/MiniTuples/v3.13/" # TODO REMOVE THIS FOR RUNNING
    if len(sys.argv) > 1:
        input_files  = sys.argv[1]
    if len(sys.argv) > 2:
        filepath    = sys.argv[2]

    mode = "filewrite" # "eval", "filewrite"

    trees_to_iterate = ["NoSel"]
    
    print("Running Depth and Inclusive Tagger over each file")
    print("Infile = " + input_files)
    for tree_selected in trees_to_iterate:

        with uproot.open(filepath + input_files) as file:
            # Access the tree
            tree = file[tree_selected]
            # Get the number of entries
            num_entries = tree.num_entries
            print(tree_selected)
            print(num_entries)
            if (num_entries > 0):
                runner = Runner(input_files=input_files, filepath=filepath, mode=mode, num_classes=2, inclusive=False, tree=tree_selected)
                runner.run()
    
if __name__ == "__main__":
    main()