"""
- RQ4
- This file retrains the models with individual discriminatory instances.
"""

import sys
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model

sys.path.append('..')
from utils import config


# we randomly sample 5% of individual discriminatory instances generated by FIDIG for retraining
def retraining(dataset_name, config, model, x_train, x_test, y_train, y_test, idi, model_name):
    classifier = joblib.load('../models/ensemble_models/' + dataset_name + '_ensemble.pkl')
    protected_features = config.protected_attrs

    re_num = int(len(idi) * 0.05)
    selected_indices = np.random.choice(idi.shape[0], size=re_num, replace=False)
    idi_selected = idi[selected_indices, :]

    vote_label = classifier.predict(np.delete(idi_selected, protected_features, axis=1))
    x_train = np.append(x_train, idi_selected, axis=0)
    y_train = np.append(y_train, vote_label, axis=0)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=821)
    model.fit(x_train, y_train, epochs=200, validation_data=(x_val, y_val),
              callbacks=[keras.callbacks.EarlyStopping(patience=10)])
    model.evaluate(x_test, y_test)
    model.save('../models/retrained_models/' + dataset_name + '_' + model_name + '_retrained_model.h5')


# load the dataset
credit_data_path = '../datasets/credit'
bank_data_path = '../datasets/bank'
census_data_path = '../datasets/census'

credit_data = pd.read_csv(credit_data_path).values
bank_data = pd.read_csv(bank_data_path).values
census_data = pd.read_csv(census_data_path).values

credit_x = credit_data[:, 1:]
credit_y = credit_data[:, 0]
bank_x = bank_data[:, :-1]
bank_y = bank_data[:, -1]
census_x = census_data[:, :-1]
census_y = census_data[:, -1]

# spilt the training set and test set
credit_x_train, credit_x_test, credit_y_train, credit_y_test = train_test_split(credit_x, credit_y, test_size=0.2,
                                                                                random_state=821)
bank_x_train, bank_x_test, bank_y_train, bank_y_test = train_test_split(bank_x, bank_y, test_size=0.2,
                                                                        random_state=821)
census_x_train, census_x_test, census_y_train, census_y_test = train_test_split(census_x, census_y, test_size=0.2,
                                                                                random_state=821)
# load models
credit_model_path = '../models/trained_models/credit_model.h5'
census_model_path = '../models/trained_models/census_model.h5'
bank_model_path = '../models/trained_models/bank_model.h5'

credit_model = load_model(credit_model_path)
census_model = load_model(census_model_path)
bank_model = load_model(bank_model_path)


# retrain begins
# credit
# credit_idi = np.load('./logfile/generated_instances/credit_discriminatory_instance.npy')
# retraining('credit', config.Credit, credit_model, credit_x_train, credit_x_test, credit_y_train, credit_y_test,
#            credit_idi, 'final')

# bank
# bank_idi = np.load('./logfile/generated_instances/bank_discriminatory_instance.npy')
# retraining('bank', config.Bank, bank_model, bank_x_train, bank_x_test, bank_y_train, bank_y_test, bank_idi, 'final')

# census
census_idi = np.load('./logfile/generated_instances/census_discriminatory_instance.npy')
retraining('census', config.Census, census_model, census_x_train, census_x_test, census_y_train, census_y_test,
           census_idi, '1')

# retrain ends
"""
- credit model:
    loss: 0.3612
    accuracy: 0.7800
- bank model:
    loss: 0.2866
    accuracy: 0.9003
- census model:
    loss:
    accuracy:
"""