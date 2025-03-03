# %% [markdown]
# This is an example of a jupyter notebook, running using the `pixi` environment we created to manage our dependencies. Note that you may need to change your python interpreter (top right corner) to:
# `.pixi/envs/default/bin/python`

# %%
import os
import glob
import re
import pandas as pd
import numpy as np
import random
import torch
import sklearn
import argparse

# change source to force cache invalidation in docker GA...

#set up plotting
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize']=[15,5] #for large visuals
%config InlineBackend.figure_format = 'retina'

from sklearn.metrics import roc_auc_score
from opensoundscape.ml import bioacoustics_model_zoo as bmz
from opensoundscape.ml.shallow_classifier import quick_fit 

DATA_SUBFOLDER_NAME = "data"
DATA_PATH = "/workspaces/non-avian-ml-toy/data/audio"


# %%
def fit_model(species, model_type, batch_size):

    files = glob.glob(os.path.join(DATA_PATH, species, DATA_SUBFOLDER_NAME, "**/*.wav"), recursive=True)
    labels = pd.DataFrame({"file": files, "present": ["pos" in f.lower() for f in files]})

    labels['file'] = labels['file'].astype(str)
    labels.set_index("file", inplace=True)

    labels_train, labels_val = sklearn.model_selection.train_test_split(labels[['present']])

    # Run Models

    torch.manual_seed(0)
    random.seed(0)
    np.random.seed(0)

    if args.model_type == "perch":

        # Do this step ONLY to convert to 5 second dataset to run perch!!!!
        labels['file'] = labels['file'].apply(lambda x: re.sub(r'data', 'data_5s', x, count=2).replace('data_5s', 'data', 1)) 
        model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', "Perch", trust_repo=True)

    elif args.model_type == "birdnet":

        model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', "BirdNET", trust_repo=True)

    else:

        raise ValueError("Invalid model type. Choose 'perch' or 'birdnet'.")

    emb_train = model.embed(labels_train, return_dfs=False, batch_size=args.batch_size, num_workers=0)
    emb_val = model.embed(labels_val, return_dfs=False, batch_size=args.batch_size, num_workers=0)

    model.change_classes(['present'])

    quick_fit(model.network, emb_train, labels_train.values, emb_val, labels_val.values, steps=1000)

    predictions = model.network(torch.tensor(emb_val).float()).detach().numpy()
    score = roc_auc_score(labels_val.values, predictions, average=None)

    print("Finished training with AUC: ", score)

    # plt.hist(predictions[labels_val==True],bins=20,alpha=0.5,label='positives')
    # plt.hist(predictions[labels_val==False],bins=20,alpha=0.5,label='negatives')
    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run bioacoustics model")
    parser.add_argument("--batch_size", type=int, default=128, help="Batch size for embedding")
    parser.add_argument("--model_type", type=str, choices=["perch", "birdnet"], default="perch", help="Model type to use")
    parser.add_argument("--species", type=str, default="bullfrog", help="Species to run model on")

    args = parser.parse_args()

    species = args.species
    model_type = args.model_type
    batch_size = args.batch_size

    fit_model(species = species, model_type = model_type, batch_size = batch_size)