from tkinter import Tk
from tkinter.filedialog import askopenfilename
import re
import sys

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

file_path = askopenfilename()
filename = re.search(r'\/([\w\-]+)(\.\w+)', file_path).group(1)

import numpy as np
from sklearn import preprocessing
from sklearn.metrics import roc_auc_score
from sklearn import metrics
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_predict
from scipy import interp
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
import csv
from sklearn import svm
from sklearn.model_selection import KFold

default_cols = 0
if len(sys.argv) > 1:
    default_cols = int(sys.argv[1])
    print(f"Столбец с аномалиями: {default_cols}")

print("Открываю файл")
with open(file_path, 'r', newline="") as file:
    file_name = csv.reader(file)
    file_list = list(file_name)

# Данные для обучения с обозначенными аномалиями
print("Загружаю данные для обучения")
Y = np.loadtxt("all_logs_eventid_anomalies.csv", dtype="int", delimiter=',', usecols=default_cols) #Выбираем столбец с аномалиями
X = np.loadtxt(file_path, dtype="double", delimiter=',') #закодированный файл

# #Данные для поиска аномалий
print("Загружаю данные для обнаружения")
new_x = np.loadtxt("data_eventid_coder_res.csv", dtype="double", delimiter=',') #Закодированный файл
new_y = np.loadtxt("data_eventid_anomalies.csv", dtype="int", delimiter=',', usecols=default_cols) #Столбец с аномалиями

print(f"Данные в X:\n {X}")
print(f"Данные в Y:\n {Y}")
print(len(X))
print(len(Y))

print("Запускаю классификатор")
cv = StratifiedKFold(n_splits=5)
# cv = KFold(n_splits = 5)

model_RF = RandomForestClassifier(n_estimators=10, max_depth=15)
model_NB = GaussianNB()
model_AB = AdaBoostClassifier(n_estimators=10, random_state=0)
model_LR = LogisticRegression()
model_ET = ExtraTreesClassifier()

# Обучаем все модели
model_RF.fit(X, Y)
model_NB.fit(X, Y)
model_AB.fit(X, Y)
model_LR.fit(X, Y)
model_ET.fit(X, Y)

models = {'model_RF': model_RF, 'model_NB': model_NB, 'model_AB': model_AB, 'model_LR': model_LR, 'model_ET': model_ET}

for key, model in models.items():
    print(f"Классификатор: {key}")

    print("Cross val score:")
    cross_score = cross_val_score(model, new_x, new_y, cv=5)
    print(cross_score)

    # pdediction
    expected = new_y
    predicted = cross_val_predict(model, new_x, new_y, cv=5)

    print("classification report:")
    report = metrics.classification_report(new_y, predicted)

    conf_matrix = metrics.confusion_matrix(new_y, predicted)
    print("confusion_matrix with cross_val_score:")
    print(conf_matrix)

    print("Accuracy score:")
    accuracy = accuracy_score(new_y, predicted)
    print(accuracy)

    result = open(f'Result_{key}.txt', 'w')
    result.write(
        f"Cross_val_score: {cross_score}\nConusion Matrix: {conf_matrix}\nClassification Report: \n{report}\nAccuracy score: {accuracy}\nAUC_score: {roc_auc_score(
            new_y, predicted)}")
    result.close()

    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    plt.figure(f"{key}")
    print("Отрисовка графика")
    i = 0
    for train, test in cv.split(new_x, new_y):
        # print(f'{train} / {test}')
        probas_ = model.fit(new_x[train], new_y[train]).predict_proba(new_x[test])
        # Compute ROC curve and area the curve
        fpr, tpr, thresholds = roc_curve(new_y[test], probas_[:, 1])
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

        i += 1
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Chance', alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr, mean_tpr, color='b',
             label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2, alpha=.8)

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                     label=r'$\pm$ 1 std. dev.')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    print("Новая итерация")
plt.show()
