
# coding: utf-8

# In[1]:

"""
Enigma Data Science Challenge

Junia Zhang | 01.08.2016

For this exercise, you will be working with the H1B visa application data, one of the most popular datasets in Enigma. 
All questions refer to the 2014 data. Please include your code along with your answers.
"""


# In[2]:

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns


# ### Load in 2014 H1B visa application data
# #### Source: https://app.enigma.io/table/us.gov.dol.oflc.h1b.2014

# In[3]:

df = pd.read_csv("enigma-us.gov.dol.oflc.h1b.2014-data.csv")


# ### Section 1: Warm Up (1/4)

# ### 1.1 - NYC H-1B visa applications by company
# * Compare Total Workers by Employer Name 
# * Filter based on whether Work City Location 1 OR Work City Location 2 contains 'New York' (+ variations)

# In[5]:

df.columns.values


# In[32]:

c = df[['lca_case_employer_name','lca_case_workloc1_city','lca_case_workloc2_city','total_workers']]


# In[50]:

nyc = c[c.lca_case_workloc1_city.str.contains("NEW YORK", na=False) | c.lca_case_workloc2_city.str.contains("NEW YORK", na=False) | c.lca_case_workloc1_city.str.contains("NYC", na=False) | c.lca_case_workloc2_city.str.contains("NYC", na=False)]


# In[51]:

nyc = nyc[['lca_case_employer_name','total_workers']]
nyc = nyc.groupby(['lca_case_employer_name']).sum().sort_values('total_workers',ascending = False)


# In[54]:

filename = "top_20_nyc_applicants.csv"
top_20 = nyc.head(20)
top_20.to_csv(filename)


# In[55]:

filename = "full_ranked_nyc_applicants.csv"
nyc.to_csv(filename)


# ### 1.2 - NYC and Mountain View Wages Comparison
# * For the purposes of this exercise, only looking at proposed wages set at 'Year' Wage Rate Unit

# In[4]:

w = df[['lca_case_employer_name',
       'lca_case_job_title',
       'lca_case_wage_rate_from', 
       'lca_case_wage_rate_unit', 
       'full_time_pos', 
       'total_workers',
       'lca_case_workloc1_city',
       'pw_1',
       'pw_unit_1', 
       'pw_source_1', 
       'other_wage_source_1',
       'yr_source_pub_1', 
       'lca_case_workloc2_city',
       'pw_2', 
       'pw_unit_2', 
       'pw_source_2',
       'other_wage_source_2']]


# In[64]:

ny = w[w.lca_case_workloc1_city.str.contains("NEW YORK", na=False) | w.lca_case_workloc2_city.str.contains("NEW YORK", na=False) | w.lca_case_workloc1_city.str.contains("NYC", na=False) | w.lca_case_workloc2_city.str.contains("NYC", na=False)]
mv = w[w.lca_case_workloc1_city.str.contains("MOUNTAIN VIEW", na=False) | w.lca_case_workloc2_city.str.contains("MOUNTAIN VIEW", na=False)]


# In[153]:

ny = ny[['lca_case_employer_name',
       'lca_case_job_title',
       'lca_case_wage_rate_from', 
       'lca_case_wage_rate_unit', 
       'full_time_pos', 
       'total_workers']]

mv = mv[['lca_case_employer_name',
       'lca_case_job_title',
       'lca_case_wage_rate_from', 
       'lca_case_wage_rate_unit', 
       'full_time_pos', 
       'total_workers']]


# In[71]:

nyy = ny[ny['lca_case_wage_rate_unit'] == 'Year']
mvy = mv[mv['lca_case_wage_rate_unit'] == 'Year']


# In[75]:

def total_wages(x):
    return x['lca_case_wage_rate_from'] * x['total_workers']


# In[76]:

nyy['total_wages'] = nyy.apply(total_wages, axis = 1)
mvy['total_wages'] = mvy.apply(total_wages, axis = 1)


# In[83]:

def wage_mean(y):
    return y.total_wages.sum()/y.total_workers.sum()


# In[92]:

mean_ny = wage_mean(nyy)
mean_mv = wage_mean(mvy)

print "The mean proposed annual wage rate in  New York is " + '$' + str(round(mean_ny,1))
print "The mean proposed annual wage rate in  Mountain View is " + '$' + str(round(mean_mv,1))


# In[105]:

nyy['varw'] = ((nyy['lca_case_wage_rate_from'] - mean_ny) ** 2) * nyy['total_workers']
mvy['varw'] = ((mvy['lca_case_wage_rate_from'] - mean_mv) ** 2) * mvy['total_workers']


# In[124]:

def wage_var(z):
    return z.varw.sum()/z.total_workers.sum()

def wage_sd(z):
    return math.sqrt(wage_var(z))


# In[125]:

variance_ny = wage_var(nyy)
variance_mv = wage_var(mvy)

stddev_ny = wage_sd(nyy)
stddev_mv = wage_sd(mvy)

print "The standard deviation of the proposed annual wage rates in  New York is " + '$' + str(round(stddev_ny,1))
print "The standard deviation of the proposed annual wage rates in  Mountain View is " + '$' + str(round(stddev_mv,1))


# ### Z-test to compare whether the two populations are statistically different
# #### Hypothesis: Wages proposed for Mountain View workers are significantly higher than wages proposed for New York workers

# In[139]:

z = (mean_mv - mean_ny)/math.sqrt(variance_mv/mvy.total_workers.sum() + variance_ny/nyy.total_workers.sum())
print "The z-statistic for the two populations means is " + str(round(z,2))


# In[140]:

def p_val(zs):
    from scipy.stats import norm
    return 2*(1 - norm.cdf(abs(z)))


# In[146]:

pv = p_val(z)
print "The p-value for the two populations means is " + str(round(pv,2))


# ### 1.3 - Relationship between H1B visas requested by an employer and the average wages proposed in NYC

# In[5]:

rny = w[w.lca_case_workloc1_city.str.contains("NEW YORK", na=False) | w.lca_case_workloc2_city.str.contains("NEW YORK", na=False) | w.lca_case_workloc1_city.str.contains("NYC", na=False) | w.lca_case_workloc2_city.str.contains("NYC", na=False)]


# In[6]:

rnyy = rny[rny['lca_case_wage_rate_unit'] == 'Year']

rnyy = rnyy[['lca_case_employer_name',
       'lca_case_wage_rate_from', 
       'total_workers']]


# In[7]:

rnyy['tot'] = rnyy['lca_case_wage_rate_from'] * rnyy['total_workers']


# In[8]:

r = rnyy.groupby('lca_case_employer_name').sum()
r['avg_wage'] = r['tot']/r['total_workers']


# In[9]:

r = r[['total_workers','avg_wage']]


# In[29]:

sns.set(style="ticks", context="talk")

g = sns.lmplot(x='total_workers', y='avg_wage', data=r, size=7)
g.set_axis_labels("Total Number of Workers Requested", "Employer's Average Proposed Wage Rate")

g.savefig('workers_vs_wage.png')


# #### Remove outliers

# In[45]:

rf = r[(r.avg_wage < 200000) & (r.total_workers < 10)]


# In[46]:

gf = sns.lmplot(x='total_workers', y='avg_wage', data=rf, size=7)
gf.set_axis_labels("Total Number of Workers Requested", "Employer's Average Proposed Wage Rate")

gf.savefig('workers_vs_wage_filtered.png')


# In[40]:

print r.corr(method='pearson')
print rf.corr(method='pearson')

