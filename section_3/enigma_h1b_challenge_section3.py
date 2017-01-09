
# coding: utf-8

# ### Load in H1B visa application data
# #### Sources: https://app.enigma.io/search/source/us.gov.dol.oflc.h1b

# In[2]:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[3]:

df_2011 = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2011.csv")
df_2012 = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2012.csv")
df_2013 = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2013.csv")
df_2014 = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2014-data.csv")
df_2015 = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2015.csv")
df_2016 = pd.read_csv("enigma-us.gov.h1b.2016.csv")


# In[4]:

df_2011 = df_2011[df_2011['status'] == 'CERTIFIED']
df_2012 = df_2012[df_2012['status'] == 'CERTIFIED']
df_2013 = df_2013[df_2013['status'] == 'CERTIFIED']
df_2014 = df_2014[df_2014['status'] == 'CERTIFIED']
df_2015 = df_2015[df_2015['case_status'] == 'CERTIFIED']
df_2016 = df_2016[df_2016['case_status'] == 'CERTIFIED']


# In[5]:

df11 = df_2011[['lca_case_workloc1_state','total_workers','lca_case_submit', 'decision_date']]
df12 = df_2012[['lca_case_workloc1_state','total_workers','lca_case_submit', 'decision_date']]
df13 = df_2013[['lca_case_workloc1_state','total_workers','lca_case_submit', 'decision_date']]
df14 = df_2014[['lca_case_workloc1_state','total_workers','lca_case_submit', 'decision_date']]
df15 = df_2015[['worksite_state','total_workers','case_submitted', 'decision_date']]
df16 = df_2016[['worksite_state', 'total_workers','case_submitted', 'decision_date']]

cols = ['worksite_state', 'total_workers', 'case_submitted', 'decision_date']

df11.columns = cols
df12.columns = cols
df13.columns = cols
df14.columns = cols
df15.columns = cols
df16.columns = cols


# In[84]:

df = df11.append(df12).append(df13).append(df14).append(df15).append(df16)


# In[85]:

df['case_submitted'] = df['case_submitted'].astype('datetime64[ns]')
df['decision_date'] = df['decision_date'].astype('datetime64[ns]')
df['approval_time'] = df['decision_date'] - df['case_submitted']


# In[86]:

df['approval_time'] = (df['approval_time'] / np.timedelta64(1, 'D')).astype(int)


# In[87]:

df['worker_volume'] = pd.cut(df['total_workers'], bins=[-1, 1, 20, 40, 60, 80, 10000])
# labels = np.array('1 2-20 21-40 41-60 61-80 81+'.split())
# df['worker_volume'] = labels[df['worker_volume']]


# In[ ]:

df['approval_time'].hist(by=df['worker_volume'])


# In[42]:

plt.savefig('distribution.png')

