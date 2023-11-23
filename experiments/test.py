import sys
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model

sys.path.append('..')
from FEDIG import FEDIG
from baseline import ADF, DICE, NeuronFair
from utils import config
from utils import FEDIG_utils
from utils import utils

# credit
path = '../models/trained_models/credit_model.h5'
data_path = '../datasets/credit'

df = pd.read_csv(data_path)
data = df.values[:, 1:]

# bank
# path = '../models/trained_models/bank_model.h5'
# data_path = '../datasets/bank'
#
# df = pd.read_csv(data_path)
# data = df.values[:, :-1]

# census
# path = '../models/trained_models/census_model.h5'
# data_path = '../datasets/census'
#
# df = pd.read_csv(data_path)
# data = df.values[:, :-1]

x = data
model = load_model(path)


# test for NeuronFair
# all_id = NeuronFair.individual_discrimination_generation('credit', config.Credit, model)
# print(len(all_id))
# print(all_id)


# test for EIDIG
# all_id = EIDIG.individual_discrimination_generation('credit', config.Credit, model)


# easy test for FEDIG
# all_id = FEDIG.individual_discrimination_generation('credit', config.Credit, model)
# print("==================len(all_id)=======================")
# print(len(all_id))


start_time = time.time()
all_id = DICE.individual_discrimination_generation('credit', config.Credit, model, c_num=4, timeout=300)
end_time = time.time()
execution_time = end_time - start_time
print("==================len(all_id)=======================")
print(len(all_id))
print('Algorithm Total time:', execution_time)
