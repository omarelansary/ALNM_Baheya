# import pickle
# # import pandas as pd

# # import numpy as np

# # import category_encoders as ce

# # from catboost import CatBoostClassifier

# # import matplotlib.pyplot as plt
# # import seaborn as sns

# import pandas as pd
# import statsmodels.api as sm
# import numpy as np
# from sklearn import preprocessing
# from sklearn.impute import KNNImputer
# #from impyute.imputation.cs import mice
# from sklearn.preprocessing import OrdinalEncoder
# import category_encoders as ce
# from sklearn.experimental import enable_iterative_imputer
# from sklearn.impute import IterativeImputer
# from impyute.imputation.cs import mice
# from sklearn.preprocessing import OrdinalEncoder
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import accuracy_score
# from sklearn.pipeline import Pipeline
# from sklearn.impute import KNNImputer, IterativeImputer
# from sklearn.preprocessing import StandardScaler
# from sklearn.compose import ColumnTransformer
# from imblearn.combine import SMOTEENN

# from sklearn.model_selection import KFold
# from sklearn.metrics import f1_score
# from imblearn.over_sampling import SMOTE
# from imblearn.combine import SMOTETomek
# from sklearn.metrics import matthews_corrcoef
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.ensemble import GradientBoostingClassifier
# from catboost import CatBoostClassifier
# from lightgbm import LGBMClassifier
# from sklearn.svm import SVC
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import KFold
# from category_encoders import CatBoostEncoder
# from category_encoders import HashingEncoder
# from category_encoders import BinaryEncoder
# from imblearn.ensemble import BalancedRandomForestClassifier
# from sklearn.preprocessing import OrdinalEncoder
# import category_encoders as ce
# from sklearn.experimental import enable_iterative_imputer
# from sklearn.impute import IterativeImputer
# from impyute.imputation.cs import mice
# from sklearn.preprocessing import OrdinalEncoder
# from sklearn.feature_selection import SequentialFeatureSelector
# from sklearn.metrics import accuracy_score
# from sklearn.feature_selection import SelectFromModel
# from sklearn.metrics import roc_auc_score
# import matplotlib.pyplot as plt
# import seaborn as sns

# def ALNM_Model(df):
#     # Load the pickled model
#     with open('C:\\Users\\omr\\Documents\\GitHub\\ALNM_Baheya\\Streamlit\\Components\\trained_model.pkl', 'rb') as file:
#         loaded_model = pickle.load(file)
#     y_pred = loaded_model.predict(df) 
#     return y_pred





import os
import pickle
import pandas as pd
from catboost import CatBoostClassifier

def ALNM_Model(df):
    # Define the model path
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'final_catboost_model.pkl')
    
    # Load the pickled model
    try:
        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

    y_pred = loaded_model.predict(df) 
    y_pred_proba = loaded_model.predict_proba(df)
    y_pred_percentage=y_pred_proba.max()
    return y_pred,y_pred_percentage
