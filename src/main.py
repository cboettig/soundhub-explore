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

#set up plotting
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize']=[15,5] #for large visuals
%config InlineBackend.figure_format = 'retina'

from sklearn.metrics import roc_auc_score
from opensoundscape.ml import bioacoustics_model_zoo as bmz
from opensoundscape.ml.shallow_classifier import quick_fit 

# %% [markdown]
# Pre-processing

# %%
datapath = "/workspaces/non-avian-ml-toy/data/audio"
species = "bullfrog"
datatype = "data"

files = glob.glob(os.path.join(datapath, species, datatype, "**/*.wav"), recursive=True)
labels = pd.DataFrame({"file": files, "present": ["pos" in f.lower() for f in files]})

# Do this step ONLY to convert to 5 second dataset to run perch!!!!
labels['file'] = labels['file'].apply(lambda x: re.sub(r'data', 'data_5s', x, count=2).replace('data_5s', 'data', 1)) 

labels['file'] = labels['file'].astype(str)
labels.set_index("file", inplace=True)

pd.set_option('display.max_colwidth', 100)
print(labels.head())

# %%
labels_train, labels_val = sklearn.model_selection.train_test_split(labels[['present']])

# %% [markdown]
# Run Models

# %%
torch.manual_seed(0)
random.seed(0)
np.random.seed(0)

# %%
model = torch.hub.load('kitzeslab/bioacoustics-model-zoo', "Perch", trust_repo=True)

# %%
emb_train = model.embed(labels_train, return_dfs=False, batch_size=128, num_workers=0)
emb_val = model.embed(labels_val, return_dfs=False, batch_size=128, num_workers=0)

model.change_classes(['present'])

# %% [markdown]
# In the prior step is where the kernel crashes while embedding, apparently could be caused by a package installation issue with tensorflow or numpy (https://github.com/microsoft/vscode-jupyter/wiki/Kernel-crashes) 
# 
# Error: "The Kernel crashed while executing code in the current cell or a previous cell. Please review the code in the cell(s) to identify a possible cause of the failure."

# %%
quick_fit(model.network, emb_train, labels_train.values, emb_val, labels_val.values, steps=1000)

# %%
predictions = model.network(torch.tensor(emb_val).float()).detach().numpy()
score = roc_auc_score(labels_val.values, predictions, average=None)

print("Finished training with AUC: ", score)

# %%
plt.hist(predictions[labels_val==True],bins=20,alpha=0.5,label='positives')
plt.hist(predictions[labels_val==False],bins=20,alpha=0.5,label='negatives')
plt.legend()


