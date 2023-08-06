import pandas as pd
import scCPEP.dataloading_utils as dataloading_utils
import scCPEP.method_utils as method_utils
import scCPEP.pareto_ensemble_pruning as pareto_ensemble_pruning
import numpy as np
import scipy
import gc
import os
import math
import rpy2.robjects as robjects
import time

from sklearn.preprocessing import OneHotEncoder
from pycaret.classification import *
# import pareto_ensemble_pruning

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

def mainFunc(args, OutputDir, TrainDataPath, TrainLabelsPath, TestDataPath, TestLabelsPath, result_dir):

    start = time.time()
    
    # prj_path = Path(__file__).parent.resolve()
    # prj_path = Path(__file__).parent.resolve().parent.resolve()
    # data_dir = prj_path / 'datas'
    # result_dir = prj_path / 'tmp'

    # OutputDir = data_dir / f'{args.dataset}' / 'result'       # Output directory defining the path of the exported file.
    # TrainDataPath = data_dir / f'{args.dataset}' / f'{args.train}_data.csv'
    # TrainLabelsPath = data_dir / f'{args.dataset}' / f'{args.train}_label.csv'
    # TestDataPath = data_dir / f'{args.dataset}' / f'{args.test}_data.csv'
    # TestLabelsPath = data_dir / f'{args.dataset}' / f'{args.test}_label.csv'
    # OutputDir = str(args.OutputDir)       # Output directory defining the path of the exported file.
    # TrainDataPath = str(args.TrainDataPath)
    # TrainLabelsPath = str(args.TrainLabelsPath)
    # TestDataPath = str(args.TestDataPath)
    # TestLabelsPath = str(args.TestLabelsPath)


    nfolds = 1
    traindata = pd.read_csv(TrainDataPath, index_col=0, sep=',')
    train_labels = pd.read_csv(TrainLabelsPath, header=0, index_col=None, sep=',')
    testdata = pd.read_csv(TestDataPath, index_col=0, sep=',')
    test_labels = pd.read_csv(TestLabelsPath, header=0, index_col=None, sep=',')
    
    for fold in range(np.squeeze(nfolds)):
        train_adata, test_adata = dataloading_utils.prepare_data(traindata, train_labels, testdata, test_labels, fold)
        train_adata, test_adata = dataloading_utils.preprocessing_data(train_adata, test_adata, lognorm=args.lognorm)
        tmp_df_path, cell_annots_path = method_utils.generate_tmp(train_adata, str(result_dir))
        
        celltype_cols = "cell.type"
        # OneHotEncoding the celltypes
        enc_train = OneHotEncoder(handle_unknown='ignore')
        y_train = enc_train.fit_transform(train_adata.obs[[celltype_cols]]).toarray()
        y_test = test_adata.obs[[celltype_cols]]
        
        trueClass = y_train.argmax(1)
        num_celltype = len(np.unique(y_train.argmax(1)))
        model_count = 0  # count the total number of ML models
        
        model_num = 6 # the number of models used

        fs_count = 0
        for fs in args.feature_selection:
            fs_count = fs_count + 1
            # each iter use one feature selection method
            train_sub, test_sub, features =method_utils.feature_selection(fs, train_adata, test_adata, str(result_dir), tmp_df_path, cell_annots_path)
            trainXY = train_sub.to_df()
            trainXY['cell.type'] = y_train.argmax(1)
            # testX = test_sub.to_df()
        
            # initialize setup
            model_setup = setup(data=trainXY, target='cell.type', preprocess = False, silent = True, session_id = args.random_seed)
            from sklearn.naive_bayes import MultinomialNB
            from sklearn.svm import LinearSVC
            from sklearn.calibration import CalibratedClassifierCV
        
            best_models = compare_models(n_select=model_num, include=[MultinomialNB(alpha=0.01),
                                                   CalibratedClassifierCV(LinearSVC()),
                                                   'mlp',
                                                   'knn', 
                                                   'rbfsvm',
                                                   'rf']) # the machine learning methods included can be changed
        
            for i in range(min(model_num, len(best_models))):
                
                model_count = model_count + 1

                if 1 == model_count:
                    test_feas = pd.DataFrame({str(model_count):features})
                else:
                    test_feas = pd.concat([test_feas, pd.DataFrame({str(model_count):features})], axis=1) # column

                model = best_models[i]
                pred = predict_model(model, data=trainXY)
                predClass = pred[['Label']]
                
                ## add 'unassigned' to predClass
                predScore = pred[['Score']].to_numpy()
                unknown_pred = np.where(predScore < args.rejection)
                predClass.iloc[unknown_pred[0].tolist()] = num_celltype
                
                if 0 == i and 1 == fs_count:
                    predictClass = predClass
                else:
                    predictClass = np.append(predictClass, predClass, axis=1)
                    
                    
                save_model(model, 'MLmodels/model_' + str(model_count))
            gc.collect()

        ensembleResults = pareto_ensemble_pruning.startTrain(predictClass, trueClass)

        ind = np.where(ensembleResults == 1)[0] # need to add 1(start from 0)
        for test in range(len(ind)):
            model_ind = ind[test] + 1 # selected models
            # load model
            model = load_model('MLmodels/model_' + str(model_ind))
            fea=test_feas.iloc[:,ind[test]].tolist()
            fea=[elem for elem in fea if elem == elem]
            testX = test_adata[:, fea].to_df()
            pred = predict_model(model, data=testX)
            predLabel = pred[['Label']]
            testScore = pred[['Score']].to_numpy()
            unknown = np.where(testScore < args.rejection)
            predLabel.iloc[unknown[0].tolist()] = num_celltype
            if 0 == test:
                testPred = predLabel
            else:
                testPred = np.append(testPred, predLabel, axis=1)
                
        # organize the result
        test_index = test_adata.obs_names
        testP = pd.DataFrame(testPred, index=test_index)
        predResult = pd.DataFrame.mode(testP, axis=1)[0].astype('int64')
        # generate the final predict result
        common_celltypes = set(train_adata.obs["cell.type"]).intersection(set(test_adata.obs["cell.type"]))
        cellTypes_train = enc_train.categories_[0]
        with_unknown = np.append(cellTypes_train, 'unknown')
        predResult_type = with_unknown[predResult.astype(np.int_)]
        end = time.time()

        trueLabs = pd.DataFrame(y_test.to_numpy())
        predLabs = pd.DataFrame(predResult_type)
        testingTime = str(end-start)
        testTimeFile = str(result_dir) + os.sep + " testTimeFile.txt"
        with open(testTimeFile, 'a') as f:
            f.write("%s\n" % testingTime)
            f.flush()
        f.close()
        
        # save the result
        trueLabs.to_csv(str(OutputDir) + os.sep + "trueLabels_" + args.train + "_" + args.test + "_" + str(args.rejection) + ".csv", index=False)
        predLabs.to_csv(str(OutputDir) + os.sep + "predLabels_"  + args.train + "_" + args.test + "_" + str(args.rejection) + ".csv", index=False)
        ensembleResults.to_csv(str(OutputDir) + os.sep + "ensembleResult_" + args.train + "_" + args.test + "_" + str(args.rejection) + ".csv", index=False)

        Acc = accuracy_score(y_true = trueLabs, y_pred = predLabs)
        weighted_F1 = f1_score(y_true = trueLabs, y_pred = predLabs,average = 'weighted')
        all_F1 = f1_score(y_true = trueLabs, y_pred = predLabs,average = None)
        median_F1 = np.median(all_F1)

        print('Acc= %.4f, meanF1= %.4f, MedF1= %.4f' % (Acc, weighted_F1, median_F1))