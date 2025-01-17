# Workflow of FEDIG Project
Welcome to this project, to follow or reproduce this work, please follow this ``workflow.md`` file.  
First, you need to prepare the environment: ``Python3.9.18 + Tensorflow2.10.0``.  
Second, you need to prepare following packages: ``numpy,pandas,jobliob,scikit-learn, tqdm, opencv-python``.

**Notice:**

**1. All commands written in this document are on the Windows 11 OS. Commands may vary for different OS.
Please verify and make appropriate modifications accordingly.**

**2. The part related to images (datasets, trained models, experimental models, etc.) cannot be uploaded to GitHub due to its large size. Please follow the instructions to add the dataset or train the neural network accordingly.**

## 1. Preprocess Dataset
```
In this part, we need to prepare and preprocess the dataset 
so that we can train the neural network model.
```

- First, we need to download the dataset from the internet. You can get the URL of datasets from the comments in the files in the folder ``/preprocessing``.
- Second, we need to save the datasets into the folder ``/datasets/raw/``, ``/datasets/celebA/``, ``/datasets/FairFace/``.
- Third, we need to run the following **python command** to preprocess the data and save them in folder ``/datasets``.

```shell
# Please make sure you are at path: /preprocessing 
# Then run the follow command:

python ./pre_bank.py
python ./pre_census.py
python ./pre_credit.py
```

## 2. Model training
```
In this part, we need to spilt data into training dataset and test dataset.
Then we use the dataset to train three DNN models.
```
- First, we need to split the data we preprocessed into training dataset and test dataset.
- Second, we need to set the corresponding hyperparameters and train the neural network.
- Third, we need to save the models after training. Also, we need to evaluate the model.

```shell
# Please make sure you are at path: /training
# Then run the follow command:

python ./train_bank.py
python ./train_census.py
python ./train_credit.py
python ./train_celebA.py
python ./train_FairFace.py
```

## 3. Cluster
```
Before generation, we need to do some preparatory work.
```
- In this part, we use K-Means algorithm to divide the dataset into clusters.

```shell
# Please make sure you are at path: /clusters
# The run the follow command:

python ./cluster.py
```

## 4. Comparison experiments with baseline
```
Some experiments of our algorithm and baselines.
```
In this part, we do some experiments of our algorithm FEDIG and baselines, 
which can prove that our algorithm is actually better than them.

**Notice:**  
1. **All the results of experiments are stored in folder */experiments/logfile*, so please clear all the *.csv* files before running the experiments.**
2. **Each experiment just run one time, in the paper we actually run five times and calculate the average result of them. So if you want to get an accurate result, please run five times (or more) per experiment.**

-  First, we need to conduct some experiments to determine the parameters of our algorithm.
```shell
# Please make sure that you are at path : /experiments
# 1.1 eta (η) of FEDIG
python .\parameter\eta.py

# 1.2 min_len of FEDIG
python .\parameter\min_len.py


#  If you want to check the results of these two experiments, 
#  please switch to the '/evaluation' folder and execute the following commands 

# evaluate eta (η) of FEDIG
python .\parameter\eta.py

# evaluate min_len of FEDIG
python .\parameter\min_len.py

```
-  Second, we compare our algorithm FEDIG with baselines in four aspects.  
We use five RQs to evaluate our algorithm, every RQ has some related experiments.
    - RQ1: How effective is FEDIG in generating IDIs? 
    - RQ2: How efficient is FEDIG in generating IDIs?
    - RQ3: How useful are the biased and irrelevant features for explaining the discriminatory decisions?
    - RQ4: How does FEDIG perform on unstructured data?
    - RQ5: How useful are the generated IDIs for improving the fairness of the DNN model?


(1). RQ1: How effective is FEDIG in generating IDIs?  
```shell
# We calculate GSR, time cost of four baselines and FEDIG on three datasets.
# Please make sure that you are at path : /experiments

# Run the RQ1 command:
python .\RQs\RQ1\RQ1_Effectiveness.py
```

(2). RQ2: How efficient is FEDIG in generating IDIs?
```shell
# We calculate the number of generated individual discriminatory instances per 1000 seconds.
# Please make sure that you are at path : /experiments

# Run the RQ2 command:
python .\RQs\RQ2\RQ2_Efficiency.py
```

(3). RQ3: How useful are the biased and irrelevant features for explaining the discriminatory decisions?
```shell
# We use FEDIG to identify biased features to explain the discrimination of DNN models.
# We also compare the result of FEDIG with NeuronFair.
# Please make sure that you are at path : /experiments

# Run tje RQ3 command:
python .\RQs\RQ3\RQ3_Explanation.py
python .\RQs\RQ3\RQ3_Explanation_img.py
python .\RQs\RQ3\RQ3_idi_retrain\bank_idi_retrain.py
python .\RQs\RQ3\RQ3_idi_retrain\census_idi_retrain.py
python .\RQs\RQ3\RQ3_idi_retrain\credit_idi_retrain.py
```

(4). RQ4: How does FEDIG perform on unstructured data?
```shell
# We calculate the performance of unstructured data on quality and quantity.
# a. Quality
python .\RQs\RQ4\RQ4_Quality.py
# b. Quantity
python .\RQs\RQ4\RQ4_Quantity.py
```

(5). RQ5: How useful are the generated IDIs for improving the fairness of the DNN model?
```shell
# Before retraining, we need to generate IDIs
# generate IDIs
python .\RQs\RQ5\FEDIG.py
python .\RQs\RQ5\FEDIG_img.py
 
# We first use majority voting to relabel the individual discriminatory instances after generating by FEDIG.
# Then we retrain the DNN models with some individual discriminatory instances.
# Please make sure that you are at path : /experiments

# a. majority voting
python .\RQs\RQ5\RQ5_majority_voting.py
python .\RQs\RQ5\RQ5_majority_voting_img.py
# b. retrain
python .\RQs\RQ4\RQ5_retraining.py
python .\RQs\RQ4\RQ5_retraining_img.py
```


## 5. Algorithm/Model Evaluation
```
Two evaluations of the retrained models.
```
- After the experiments in **Part 4**, we have proved that our algorithm FEDIG is better than the baseline.  
- Meanwhile, we retrained some DNN models with different percentage of individual discriminatory instances in
RQ4.
- We evaluate the models we retrained in this part.

```shell
# Two evaluations on retrained models.
# Please make sure that you are at path: /evaluation

# 1. Retrain evaluation
# Calculate the precision rate, recall rate and F1 score.
 python .\retrained_models\retrain_evaluation.py
 python .\retrained_models\retrain_evaluation_img.py

# 2. Fairness evaluation
# Calculate the percentage of individual discriminatory instances with .95 confidence
 python .\retrained_models\fairness_evaluation.py
 python .\retrained_models\fairness_evaluation_img.py
  
# 3. IDI evaluation
# Calculate the performance on similar datasets.
 python .\retrained_models\fairness_idi_evaluation.py
```


**Here are all the instructions. I hope they can be helpful to you.   
If you have any questions, please feel free to contact me.**

