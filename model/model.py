import pandas as pd
import category_encoders
from category_encoders import TargetEncoder
import random
import warnings
import sys

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

#decision tree                                                                                                                                                                   
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#random forest                                                                                                                                                                   
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

#bagging
from numpy import mean
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import BaggingClassifier

'''                                                                                                                                                                              
Below are the constants to modify before running the model!                                                                                                                      
'''
MODELS=['rf', 'dt', 'bagging'] #expects a list, rf - Random Forest,  dt - Decision Tree, bagging - Bagging                                                                                                    
DEPTH = 5 #depth for Decision Tree Classifier                                                                                                                                    
CUTOFF = 12 #high/low cutoff                                                                                                                                                     
SAMPLE_SIZE = 50000
NUM_HIGH = 2550
NUM_LOW = 1250
BALANCED = False #boolean, whether we want to balance the distribution of high/low classes

#The below are the ways to handle the categorical features - they should be mutually exclusive                                                                                   
USE_ONE_HOT_ENCODING = False
USE_TARGET_ENCODING = False

OUTPUT_FILE = "./unbalanced_50000"                                        
METADATA = './all_data_final_all_features.csv'

'''                                                                                                                                                                              
Important Note: When editing the feature variables below, if you add features to the ALL_FEATURES list, add the feature to the NONBOOL_COLS l                                    
ist if it is categorical and the BOOL_COLS if it is boolean. These lists are used for one-hot encoding and translating True/False to 0/1 values for our model. There's no need t\
o remove items from NONBOOL_COLS or BOOL_COLS -- we'll only check for items that are specified as features in the model.                                                         
'''
NONBOOL_COLS = [] #'platform'                                                                         
BOOL_COLS = ["summer_fire_season", 'santa_ana_fire_season']

COLUMNS = ['fire_occurrence','acres_burned','avg_dp_temp','avg_rel_hum','avg_wb_temp','avg_wind_speed','precip','pop_density','latitude','longitude', "summer_fire_season", 'santa_ana_fire_season']
ALL_FEATURES = ['avg_dp_temp','avg_rel_hum','avg_wb_temp','avg_wind_speed','precip','pop_density','latitude','longitude', "summer_fire_season", 'santa_ana_fire_season']
#constants for model                                                                                                                                                             
LABEL_COL_NAME = 'fire_occurrence'
NUM_ESTIMATORS = 20
RANDOM_SEED = 21

def get_nonbool(subset):
    res = []
    for feature in subset:
        if feature in NONBOOL_COLS:
            res.append(feature)
    return res

def get_bool(subset):
    res = []
    for feature in subset:
        if feature in BOOL_COLS:
            res.append(feature)
    return res


def generate_model (models, depth, cutoff_val, features, sample_size, balanced, output_file):
    orig_stdout = sys.stdout
    f = open(output_file, "w")
    sys.stdout = f

    data = pd.read_csv(METADATA, sep=',', dtype={'county':str,'fire_occurrence':int, 'acres_burned': int, 'avg_dp_temp': float, 'avg_rel_hum': float, 'avg_wb_temp': float, 'avg_wind_speed': float, 'precip': float, 'pop_density': float, 'latitude':float, 'longitude':float, "summer_fire_season": int, 'santa_ana_fire_season': int}, header=0)
    
    #IF BALANCED, balance high and low classes so that each are 1/2 the number of samples indicated; otherwise just sample the number indicated                               
    if balanced:
        low = data[data['fire_occurrence'] == 0]
        low = low[['key']]
        high = data[data['fire_occurrence'] == 1]
        high = high[['key']]
        
        dates_high = list(set(high['key']))
        dates_low = list(set(low['key']))
        random.seed(RANDOM_SEED)
        try:
            random_high = random.sample(dates_high, NUM_HIGH)
            print("num_high", len(random_high))
            random_low = random.sample(dates_low,  NUM_LOW)
            print("num_low", len(random_low))

            data_high = data[data['key'].isin(random_high)]
            data_low = data[data['key'].isin(random_low)]
            frames = [data_high, data_low]
            final_df = pd.concat(frames)
        except:
            print("Data not large enough to fit desired sample size. Using full dataset instead...")
            final_df = data
    else:
        try:
            print("total", SAMPLE_SIZE)
            keys = list(set(data['key']))
            random.seed(RANDOM_SEED)
            random_dates= random.sample(keys, sample_size)
            final_df = data[data['key'].isin(random_dates)]
        except:
            print("Data not large enough to fit desired sample size. Using full dataset instead...")
            final_df = data
    category_labels = final_df[LABEL_COL_NAME]
    category_binary = [1 if i == 1 else 0 for i in category_labels]
    final_df[LABEL_COL_NAME] = category_binary

    final_df.index = final_df['key']
    final_df = final_df[ALL_FEATURES]

    final_df = final_df.fillna(0)
    X_train, X_test, y_train, y_test = train_test_split(final_df, category_binary, test_size=0.3, stratify=category_binary)

    #Run Decision Tree Classifier with user-provided Depth                                                                                                                       
    if "dt" in models:
        dtc = DecisionTreeClassifier(random_state=RANDOM_SEED, max_depth=depth)
        dtc.fit(X_train, y_train)

        # store predicted values and calculate accuracy                                                                                                                          
        y_pred = dtc.predict(X_test)
        print('Classification score with a depth of ' + str(depth) + ' is ' + str(dtc.score(X=X_test, y=y_test)))

        #decision tree eval metrics                                                                                                                                              
        print('Accuracy and performance of Decision Tree Classifier with ' + str(depth) + ' layers:')
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        print(accuracy_score(y_test, y_pred))

    #Run Random Forest Models                                                                                                                                                    
    if "rf" in models:
        rfc = RandomForestClassifier(n_estimators=NUM_ESTIMATORS, random_state=RANDOM_SEED)
        rfc.fit(X_train, y_train)
        y_pred = rfc.predict(X_test)

        scaler = StandardScaler()
        X_train_sc = scaler.fit_transform(X_train)
        X_test_sc = scaler.transform(X_test)

        rfc = RandomForestClassifier(n_estimators=NUM_ESTIMATORS, random_state=RANDOM_SEED, class_weight="balanced")
        rfc.fit(X_train_sc, y_train)
        y_pred_sc = rfc.predict(X_test_sc)
        rfc.score(X_test_sc, y_test)

        # again we leverage the metrics from sci-kit learn                                                                                                                       
        print('Accuracy and performance of Random Forests on non-normalized data with 20 estimators:')
        print(confusion_matrix(y_test,y_pred))
        print(classification_report(y_test,y_pred))
        print(accuracy_score(y_test, y_pred))
    
    if "bagging" in models:
        print("bagging")
        model = BaggingClassifier()
        # define evaluation procedure
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        # evaluate model
        scores = cross_val_score(model, final_df, category_binary, scoring='roc_auc', cv=cv, n_jobs=-1)
        # summarize performance
        print('Mean ROC AUC: %.3f' % mean(scores))
    sys.stdout = orig_stdout
    f.close()

def main():
    generate_model(MODELS, DEPTH, CUTOFF, ALL_FEATURES, SAMPLE_SIZE, BALANCED, OUTPUT_FILE)

if __name__ == "__main__":
    main()






