#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns   
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("data/fertilizer_dataset.csv")
df


# In[ ]:


df.info()


# In[ ]:


df['Fertilizer Name'].value_counts()


# In[ ]:


df['Soil Type'].value_counts()


# In[ ]:


df['Crop Type'].value_counts()


# In[ ]:


y = df['Fertilizer Name'].copy()
X = df.drop(['Fertilizer Name'],axis=1).copy()


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,shuffle=True,random_state=1)


# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

nominal_transformer = Pipeline(steps=[
    ('onehot',OneHotEncoder(sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('nominal',nominal_transformer,['Soil Type','Crop Type'])
],remainder='passthrough')

model = Pipeline(steps=[
    ('preprocessor',preprocessor),
    ('scaler',StandardScaler()),
    ('classifier',RandomForestClassifier())
])


# In[ ]:


model.fit(X_train,y_train)


# In[ ]:


model.score(X_test,y_test)


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_test,model.predict(X_test)))

import joblib

joblib.dump(model, "models/fertilizer_model.pkl")
print("✅ Fertilizer model saved successfully!")