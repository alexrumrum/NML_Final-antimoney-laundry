#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
features = pd.read_csv('../../elliptic_bitcoin_dataset/full_data.csv',header=None)
classes = pd.read_csv('../../elliptic_bitcoin_dataset/elliptic_txs_classes.csv')
feature = [str(i) for i in range(171)]
features.columns = ["txId","time_step"] + feature
features = pd.merge(features,classes,left_on="txId",right_on="txId",how='left')

features['class'] = features['class'].apply(lambda x: '0' if x == "unknown" else x)
features.dropna(subset=['165'], inplace=True)
features.dropna(subset=['166'], inplace=True)
features.dropna(subset=['167'], inplace=True)
features.dropna(subset=['168'], inplace=True)
features.dropna(subset=['169'], inplace=True)
features.dropna(subset=['170'], inplace=True)

data = features[(features['class']=='1') | (features['class']=='2')]
X = data[feature]
Y = data['class']
Y = Y.apply(lambda x: 0 if x == '2' else 1)
std = StandardScaler()
X = std.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3,random_state=0,shuffle=False)
pca = PCA(n_components = X.shape[1] - 1)
pca.fit(X_train)
X_train = pca.transform(X_train)
X = pca.transform(X)
X2 = sm.add_constant(X_train)
est = sm.OLS(Y_train, X2)
est2 = est.fit()
print("Linear regression")
print(est2.summary())
fi = open('./linear_pca.txt', 'w')
fi.write(f"{est2.summary()}")
fi.close()

log_reg = sm.Logit(Y_train, X2).fit(method='bfgs')
print("logistic regression")
print(log_reg.summary())
fi = open('./logistic_pca.txt', 'w')
fi.write(f"{log_reg.summary()}")
fi.close()

fi = open('./corr_pca.txt', 'w')
fi.write(f"{pd.DataFrame(X).corr().to_string()}")
fi.close()
cmap = sns.diverging_palette(0, 230, 90, 60, as_cmap=True)
sns.heatmap(pd.DataFrame(X).corr(), cmap=cmap, cbar={'shrink':0.4, 'ticks':[-1, -0.5, 0, 0.5, 1]})
plt.savefig('../image/corr_pca.png')
plt.close()

cor = []
X = pd.DataFrame(X)
feature = [str(i) for i in range(170)]
X.columns = feature
for i in range(170):
    x = X[f'{i}'].corr(Y)
    cor.append(x)
plt.plot(cor)
plt.savefig("../image/corr_y_pca.png")