import numpy as np
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score, precision_recall_curve, auc
import statsmodels.discrete.discrete_model as sm
from typing import Union

# helper functions for DRFSC
def create_balanced_distributions(labels: np.ndarray, n_feats: int, n_vbins: int, n_hbins: int):
    """
    Combines outputs from feature_distribution and balanced_sample_partition to create class-balanced feature and sample partitions for the dataset.
    """ 
    return feature_distribution(n_feats=n_feats,n_vbins=n_vbins
            ), \
        balanced_sample_partition(labels=labels, n_hbins=n_hbins
            )

def balanced_sample_partition(labels: np.ndarray, n_hbins: int) -> np.ndarray:
    """
    Creates class-balanced sample partitions for the dataset.
    
    Parameters
    ----------
    labels : np.ndarray 
        data labels.
    n_hbins : int
        number of sample partiions of the data.
    
    Returns
    -------
    sample_partitions : np.ndarray
        Class balanced version of sample_distribution.
    """
    index_by_label = {
        l: np.where(labels == l)[0] for l in np.unique(labels)
    }

    index_by_label_split = {
        key: sample_distribution(n_samples=None, n_hbins=n_hbins, sample=value) for key, value in index_by_label.items()
    }

    _partitions = []
    for i in range(n_hbins):
        combined_sample = np.concatenate(([index_by_label_split[key][:, i] for key in index_by_label_split.keys()]), axis=0)
        _partitions.append(random.sample(list(combined_sample), len(combined_sample)))

    return np.transpose(np.array(_partitions))

def sample_distribution(n_samples: int, n_hbins: int, sample: np.ndarray=None) -> np.ndarray:
    """
    Creates sample bins for the dataset.
    
    Parameters
    ----------
    n_samples : int
        number of samples in the data.
    n_hbins : int
        number of sample partiions of the data.
    sample : np.ndarray, optional
        if sample is not None, then the sample indexes are taken from sample, otherwise they are generated from np.arange(n_samples). sample argument required for creating balanced sample partitions.
    
    Returns
    -------
    sample_partitions : np.ndarray 
        Contains in each column the sample indexes of the samples that belong to that sample bin.
    """
    if sample is None:
        sample_index = np.arange(n_samples).tolist()# list of sample ids
    else:
        sample_index = sample.tolist()
        n_samples = len(sample_index)
    rnd_list = random.sample(sample_index, len(sample_index)) # random shuffle of feature ids
    
    _dups = (n_hbins - (len(rnd_list) % n_hbins)) if (n_samples % n_hbins != 0) else 0 # number of duplicates to add

    _comb = rnd_list + random.sample(sample_index, _dups)
    sample_partitions = np.reshape(_comb, (int(len(_comb) / n_hbins), n_hbins)) # convert reshuffled features into matrix of dim [int(len(_comb) / n_hbins)x n_bins]
    return sample_partitions

def feature_distribution(n_feats: int, n_vbins: int) -> np.ndarray:
    """
    Function that creates feature bins for the features in the dataset for use by DRFSC.
    
    Parameters
    ----------
    n_feats : int 
        number of features in the data
    n_vbins : int
        number of feature partitions of the data.
    
    Returns
    -------
    feature_partitions : np.ndarray 
        Contains in each column the features that belong to that feature bin
    """

    feature_index = np.arange(1, n_feats).tolist() # list of feature ids
    rnd_list = random.sample(feature_index, len(feature_index)) # random shuffle of feature ids
    
    _dups = (n_vbins - (len(rnd_list) % n_vbins)) if ((n_feats - 1) % n_vbins != 0) else 0 # number of duplicates to add
    
    _comb = rnd_list + random.sample(feature_index, _dups)
    rnd_mat = np.reshape(_comb, (int(len(_comb) / n_vbins), n_vbins)) # convert reshuffled features into matrix of dim [(int(len(_comb) / n_vbins) x n_vbins]
    feature_partitions = np.vstack((np.zeros((n_vbins,)), rnd_mat))
    return feature_partitions


def scale_data(data: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
    """ 
    Uses sklearn.preprocessing to rescale feature values to [0,1].
    
    Parameters
    ----------
    data : np.ndarray or pd.DataFrame
        data to be transformed
    
    Returns
    -------
    data_out : np.ndarray or pd.DataFrame
        [0,1] transform of data   
    """
    minmax = MinMaxScaler(feature_range=(0,1))
    if isinstance(data, pd.DataFrame):
        column_names = minmax.fit(data).get_feature_names_out()
        data_out = pd.DataFrame(minmax.fit_transform(np.asarray(data)), columns=column_names)
    
    else:
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data must be np.ndarray or pd.DataFrame. Type = {type(data)}")
        data_out = minmax.fit_transform(data)

    return data_out

def extend_features(data: Union[np.ndarray, pd.DataFrame], degree: int=1) -> Union[np.ndarray, pd.DataFrame]:
    """ 
    Uses sklearn.preprocessing to create polynomial features of data and add bias term.
    
    Parameters
    ----------
    data : np.ndarray or pd.DataFrame
        data to be transformed
    degree : int, optional
        Degree of non-linearity to generate. Defaults to 1. By default just adds a bias term.
    
    Returns
    -------
    data_out : np.ndarray or pd.DataFrame
        Polynomial transformed data   
    """

    if not isinstance(degree, int):
        raise TypeError("degree parameter must be an integer")
    
    poly = PolynomialFeatures(degree=degree, interaction_only=False, 
                            include_bias=True, order="C")
    
    if isinstance(data, pd.DataFrame):
        column_names = poly.fit(data).get_feature_names_out()
        data_out = pd.DataFrame(poly.fit_transform(np.asarray(data)), columns=column_names)
    
    else:
        if not isinstance(data, np.ndarray):
            raise TypeError(f"data must be np.ndarray or pd.DataFrame. Type = {type(data)}")
        data_out = poly.fit_transform(data)
        
    return data_out


def evaluate_model(
        model_features: list, 
        X_train: np.ndarray, 
        X_val: np.ndarray, 
        X_test: np.ndarray, 
        Y_train: np.ndarray, 
        Y_val: np.ndarray, 
        Y_test: np.ndarray, 
        metric: str
    ):
    """
    Evaluates the performance of a model on the test set.

    Parameters
    ----------
    model_features : list
        Subset of features to be included in the model
    X_train : np.ndarray
        Training data
    X_val : np.ndarray
        Validation data
    Y_train : np.ndarray
        Training labels
    Y_val : np.ndarray
        Validation labels
    metric : str {'acc', 'roc_auc', 'avg_prec','f1', 'auprc'}
        metric used to evaluate model performance

    Returns
    -------
    model_final : object
        Fitted logistic regression model. See statsmodels.Logit
    model_performance : float
        Performance of the model on the validation set
    """
    
    model_final = sm.Logit(
                        np.concatenate((Y_train, Y_val), axis=0), 
                        np.concatenate((X_train, X_val), axis=0)[:, model_features]
                    ).fit(disp=False, method='lbfgs')
    
    label_prediction = model_final.predict(X_test[:, model_features]) # predict probabilities
    
    return model_final, model_score(
                            method=metric, 
                            y_true=Y_test, 
                            y_pred_label=label_prediction.round(), 
                            y_pred_prob=label_prediction
                        )

def evaluate_interim_model(
        model_features: list, 
        X_train: np.ndarray, 
        X_val: np.ndarray, 
        Y_train: np.ndarray, 
        Y_val: np.ndarray, 
        metric: str
    ):
    """
    Evaluates the performance of a model on the validation set.

    Parameters
    ----------
    model_features : list
        Subset of features to be included in the model
    X_train : np.ndarray
        Training data
    X_val : np.ndarray
        Validation data
    Y_train : np.ndarray
        Training labels
    Y_val : np.ndarray
        Validation labels
    metric : str {'acc', 'roc_auc', 'avg_prec','f1', 'auprc'}
        metric used to evaluate model performance

    Returns
    -------
    model_final : object
        Fitted logistic regression model. See statsmodels.Logit
    model_performance : float
        Performance of the model on the validation set
    """
    model_final = sm.Logit(
                    Y_train, 
                    X_train[:, model_features]
                ).fit(disp=False, method='lbfgs')

    label_prediction = model_final.predict(X_val[:, model_features]) 
    
    return model_final, model_score(
                            method=metric, 
                            y_true=Y_val, 
                            y_pred_label=label_prediction.round(), 
                            y_pred_prob=label_prediction
                        )



def evaluate_interim_models(result_list, X_train, X_val, Y_train, Y_val, metric):
    for result in result_list:
        result.model, result.evaluation = evaluate_interim_model(
                                                    model_features=result.features_, 
                                                    X_train=X_train, 
                                                    X_val=X_val,
                                                    Y_train=Y_train, 
                                                    Y_val=Y_val,
                                                    metric=metric
                                                )
    return 

def model_score(
        method: str, 
        y_true: np.ndarray,
        y_pred_label: np.ndarray, 
        y_pred_prob: np.ndarray
    ) -> float:
    
    """
    Evalutates model performance based on specified metric using sklearn.metrics.
    
    Parameters
    ----------
    method : str {'acc', 'roc_auc', 'avg_prec','f1', 'auprc'}
        metric used to evaluate model performance
    y_true : np.ndarray
        {0,1} ground truth labels
    y_pred_label : np.ndarray
        {0,1} predicted labels
    y_pred_prob : np.ndarray
        [0,1] predicted probabilities
    
    Returns
    -------
    out : float
        output based on metric
    """
    methods = {
        'acc' : accuracy_score(
                    y_true=y_true, 
                    y_pred=y_pred_label
                ), \
        'roc_auc' : roc_auc_score(
                    y_true=y_true, 
                    y_score=y_pred_prob, 
                    average='weighted'
                ), \
        'avg_prec' : average_precision_score(
                    y_true=y_true, 
                    y_score=y_pred_prob, 
                    average='weighted'
                ), \
        'f1' : f1_score(
                    y_true=y_true, 
                    y_pred=y_pred_label, 
                    average='binary'
                ), \
        'auprc' : au_prc(
                    y_true=y_true, 
                    y_pred_prob=y_pred_prob
                )}
    out = methods.get(method, 'Invalid method')
    return out
        
def au_prc(y_true: np.ndarray, y_pred_prob: np.ndarray) -> float:
    """
    Computes the area under the precision-recall curve

    Parameters
    ----------
    y_true : np.ndarray
        array of {0,1} ground truth labels
    y_pred_prob : np.ndarray 
        array of [0,1] predicted probabilities

    Returns
    -------
    _auc : float
        area under the precision-recall curve
    """
    precision, recall, _ = precision_recall_curve(y_true=y_true, probas_pred=y_pred_prob)
    _auc = auc(x=recall, y=precision)
    return _auc
        
def remove_feature_duplication(list_of_arrays: list) -> set:
    return set(np.concatenate(list_of_arrays)) if list_of_arrays else set(list_of_arrays)


def data_info(X_train=None, X_val=None, X_test=None, Y_train=None, Y_val=None, Y_test=None):
    """
    Prints some information about the loaded data.
    """
    print("Information for Loaded Data: \n -------------")
    print(f"'X_train' SHAPE: {X_train.shape}, TYPE: {type(X_train).__name__}") if X_train is not None else None
    print(f"'X_val'   SHAPE: {X_val.shape}, TYPE: {type(X_val).__name__}") if X_val is not None else None
    print(f"'X_test'  SHAPE: {X_test.shape}, TYPE: {type(X_test).__name__}") if X_test is not None else None
    
    print(f"'Y_train' SHAPE: {Y_train.shape}, TYPE: {type(Y_train).__name__}") if Y_train is not None else None
    print(f"'Y_val'   SHAPE: {Y_val.shape}, TYPE: {type(Y_val).__name__}") if Y_val is not None else None
    print(f"'Y_test'  SHAPE: {Y_test.shape}, TYPE: {type(Y_test).__name__}") if Y_test is not None else None
    print("-------------")

def get_corr_df(X, level=0.8):
    '''

    Calculation how many times a feature was an in high correlation.

    Count = 1 denotes only autocorrelation.

    '''
    corr = X.corr()

    #display(corr.style.background_gradient(cmap='coolwarm'))
    counts = []
    for cnt in np.arange(0,X.shape[1]):
        highCorr_idx= np.where(corr>level)
        counts.append((len(np.where(highCorr_idx[0]==cnt)[0])+len(np.where(highCorr_idx[1]==cnt)[0]))/2)

    return pd.DataFrame(counts,X.columns,columns=['Count'])

def load_wdbc(path):
    '''
    Takes given WDBC file and returns the data in a numpy array
    '''
    with open(path, "rb") as fo:
        data = np.loadtxt(
            fo, 
            delimiter = ",", 
            skiprows = 0, 
            converters = {1: lambda x: 1 if x.decode("utf-8") == "M" else 0}
        )
    return data