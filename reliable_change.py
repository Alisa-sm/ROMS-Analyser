import pandas as pd 
import numpy as np 

"""PART 1: DATA CLEANING"""

"""Ensure that excel files are in the same file directory"""
cwp = pd.read_excel('cwp_outcomes_cleaned.xlsx')
emhp = pd.read_excel('emhp_outcomes_cleaned.xlsx')

"""Exclude na values"""
cwp_rcads_t1_nonan = cwp['rcads_tscore_anx_dep_t1'].dropna()
cwp_rcads_t2_nonan = cwp['rcads_tscore_anx_dep_t2'].dropna()
cwp_sdq_t1_nonan = cwp['sdq_total_t1'].dropna()
cwp_sdq_t2_nonan = cwp['sdq_total_t2'].dropna()
cwp_gbo_t1_nonan = cwp['goals_g1score_t1'].dropna() + cwp['goals_g2score_t1'].dropna() + cwp['goals_g3score_t1'].dropna()
cwp_gbo_t2_nonan = cwp['goals_g1score_t2'].dropna() + cwp['goals_g2score_t2'].dropna() + cwp['goals_g3score_t2'].dropna()
emhp_rcads_t1_nonan = emhp['rcads_tscore_anx_dep_t1'].dropna()
emhp_rcads_t2_nonan = emhp['rcads_tscore_anx_dep_t2'].dropna()
emhp_sdq_t1_nonan = emhp['sdq_total_t1'].dropna()
emhp_sdq_t2_nonan = emhp['sdq_total_t2'].dropna()
emhp_gbo_t1_nonan = emhp['goals_g1score_t1'].dropna() + emhp['goals_g2score_t1'].dropna() + emhp['goals_g3score_t1'].dropna()
emhp_gbo_t2_nonan = emhp['goals_g1score_t2'].dropna() + emhp['goals_g2score_t2'].dropna() + emhp['goals_g3score_t2'].dropna()

"""PART 2: RELIABLE CHANGE CRITERIONS"""
def reliable_change_criterion(sd, r):
    se_diff = sd * np.sqrt(2) * np.sqrt(1 - r)
    return se_diff * 1.96

cwp_rcads_reliable_change_criterion = reliable_change_criterion(cwp_rcads_t1_nonan.std(), 0.85)
cwp_sdq_reliable_change_criterion = reliable_change_criterion(cwp_sdq_t1_nonan.std(), 0.75)
emhp_rcads_reliable_change_criterion = reliable_change_criterion(emhp_rcads_t1_nonan.std(), 0.85)
emhp_sdq_reliable_change_criterion = reliable_change_criterion(emhp_sdq_t1_nonan.std(), 0.85)

"""If you need to visualise the criterions as a table, you can turn the variables above into a df"""
reliable_change_criterions = pd.DataFrame({
    'cwp_rcads': [np.round(cwp_rcads_reliable_change_criterion, 2)],
    'cwp_sdq': [np.round(cwp_sdq_reliable_change_criterion, 2)],
    'cwp_gbo': [2.45],
    'emhp_rcads': [np.round(emhp_rcads_reliable_change_criterion, 2)],
    'emhp_sdq': [np.round(emhp_sdq_reliable_change_criterion, 2)],
    'emhp_gbo': [2.45]
})

"""run reliable_change_criterions.head() to show the cut off points as a table (optional)"""

"""PART 3: RELIABLE CHANGE"""
"""This is done with a O(N) time complexity. Feel free to implement your own function that can outperform this."""

"""cwp data"""
cwp_rcads_reliable_improvement = 0
cwp_rcads_no_change = 0
cwp_rcads_reliable_deterioration = 0
cwp_sdq_reliable_improvement = 0
cwp_sdq_no_change = 0
cwp_sdq_reliable_deterioration = 0
cwp_gbo_reliable_improvement = 0
cwp_gbo_no_change = 0
cwp_gbo_reliable_deterioration = 0

for index, row in cwp.iterrows():
    if row['rcads_tscore_anx_dep_t2'] >= 0:
        if row['rcads_tscore_anx_dep_t1'] - row['rcads_tscore_anx_dep_t2'] > reliable_change_criterions['cwp_rcads'].mean():
            cwp_rcads_reliable_improvement += 1
        elif (row['rcads_tscore_anx_dep_t1'] - row['rcads_tscore_anx_dep_t2']) < -(reliable_change_criterions['cwp_rcads'].mean()):
            cwp_rcads_reliable_deterioration += 1
        else:
            cwp_rcads_no_change += 1

for index, row in cwp.iterrows():
    if row['sdq_total_t2'] >= 0:
        if row['sdq_total_t1'] - row['sdq_total_t2'] > reliable_change_criterions['cwp_sdq'].mean():
            cwp_sdq_reliable_improvement += 1
        elif (row['sdq_total_t1'] - row['sdq_total_t2']) < -(reliable_change_criterions['cwp_sdq'].mean()):
            cwp_sdq_reliable_deterioration += 1
        else:
            cwp_sdq_no_change += 1

for index, row in cwp.iterrows():
    goal_average_change = ((row['goals_g1score_t2']+row['goals_g2score_t2']+row['goals_g3score_t2'])/3) - ((row['goals_g1score_t1']+row['goals_g2score_t1']+row['goals_g3score_t1'])/3)
    if row['goals_g1score_t2'] >= 0:
        if goal_average_change > 2.45:
            cwp_gbo_reliable_improvement +=1
        elif goal_average_change < -2.45:
            cwp_gbo_reliable_deterioration +=1
        else:
            cwp_gbo_no_change +=1

"""emhp data"""
emhp_rcads_reliable_improvement = 0
emhp_rcads_no_change = 0
emhp_rcads_reliable_deterioration = 0
emhp_sdq_reliable_improvement = 0
emhp_sdq_no_change = 0
emhp_sdq_reliable_deterioration = 0
emhp_gbo_reliable_improvement = 0
emhp_gbo_no_change = 0
emhp_gbo_reliable_deterioration = 0

for index, row in emhp.iterrows():
    if row['rcads_tscore_anx_dep_t2'] >= 0:
        if row['rcads_tscore_anx_dep_t1'] - row['rcads_tscore_anx_dep_t2'] > reliable_change_criterions['cwp_rcads'].mean():
            emhp_rcads_reliable_improvement += 1
        elif (row['rcads_tscore_anx_dep_t1'] - row['rcads_tscore_anx_dep_t2']) < -(reliable_change_criterions['cwp_rcads'].mean()):
            emhp_rcads_reliable_deterioration += 1
        else:
            emhp_rcads_no_change += 1

for index, row in emhp.iterrows():
    if row['sdq_total_t2'] >= 0:
        if row['sdq_total_t1'] - row['sdq_total_t2'] > reliable_change_criterions['cwp_sdq'].mean():
            emhp_sdq_reliable_improvement += 1
        elif (row['sdq_total_t1'] - row['sdq_total_t2']) < -(reliable_change_criterions['cwp_sdq'].mean()):
            emhp_sdq_reliable_deterioration += 1
        else:
            emhp_sdq_no_change += 1

for index, row in emhp.iterrows():
    goal_average_change = ((row['goals_g1score_t2']+row['goals_g2score_t2']+row['goals_g3score_t2'])/3) - ((row['goals_g1score_t1']+row['goals_g2score_t1']+row['goals_g3score_t1'])/3)
    if row['goals_g1score_t2'] >= 0:
        if goal_average_change > 2.45:
            emhp_gbo_reliable_improvement +=1
        elif goal_average_change < -2.45:
            emhp_gbo_reliable_deterioration +=1
        else:
            emhp_gbo_no_change +=1

