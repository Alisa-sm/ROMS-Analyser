import streamlit as st 
import pandas as pd
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt

#Title
st.title('Site Reports: ROMS Analyser')
st.write('Fill in the appropriate fields and upload the excel files. Once they have all been filled out, click run report')

#Input details
site_name = st.text_input('Site Name')
registered_user = st.text_input('Number of registered users on POD. Please enter a numeric value.')
period_1 = st.date_input('Time Period 1. Default will be todays date. Please make sure this is correct as the report will run regardless of what date you put.')
period_2 = st.date_input('Time Period 2. Default will be todays date. Please make sure this is correct as the report will run regardless of what date you put.')

#Upload files
st.write('Upload the files you get from the POD export. For RCADS, GBO and SDQ, only upload the patient completions (not parent/carer)')
rcads = st.file_uploader('Upload RCADS', type='csv')
sdq = st.file_uploader('Upload SDQ', type='csv')
gbo = st.file_uploader('Upload GBO', type='csv')
st.write('If you have esq data, upload them here. If you do not, you can just leave it out. Esq is only used to get some qualitative feedback.')
esq_self_9_11 = st.file_uploader('Upload ESQ Self 9-11', type='csv')
esq_self_12_18 = st.file_uploader('Upload ESQ Self 12-18', type='csv')
esq_parent_carer = st.file_uploader('Upload ESQ Parent/Carer', type='csv')

#Run report
st.write('Click run report to get a report. At the very minimum, complete all fields except for the optional ESQs.')

#Report
def site_report():
    st.title(site_name + ' Site Report')

    #Get the number of completed patients between time period
    completed_patients_id = []
    rcads_df = pd.read_csv(rcads)
    sdq_df = pd.read_csv(sdq)
    gbo_df = pd.read_csv(gbo)
    rcads_cleaned = [] #<-- cleaned rcads for analysis
    sdq_cleaned = [] #<-- cleanded sdq for analysis
    gbo_cleaned = [] #<-- cleaned gbo for analysis
    for index, row in rcads_df.iterrows():
        if row['patient_id'] not in completed_patients_id and row['completed_by'] == 'patient' and str(row['rcads_date_t1']) >= str(period_1) and str(row['rcads_date_t2']) <= str(period_2):
            completed_patients_id.append(row['patient_id'])
        if row['completed_by'] == 'patient' and str(row['rcads_date_t1']) >= str(period_1) and str(row['rcads_date_t2']) <= str(period_2):
            rcads_cleaned.append(row)
    for index, row in sdq_df.iterrows():
        if row['patient_id'] not in completed_patients_id and row['completed_by'] == 'patient' and str(row['sdq_date_t1']) >= str(period_1) and str(row['sdq_date_t2']) <= str(period_2):
            completed_patients_id.append(row['patient_id'])
        if row['completed_by'] == 'patient' and str(row['sdq_date_t1']) >= str(period_1) and str(row['sdq_date_t2']) <= str(period_2):
            sdq_cleaned.append(row)
    for index, row in gbo_df.iterrows():
        if row['patient_id'] not in completed_patients_id and row['completed_by'] == 'patient' and str(row['goals_date_t1']) >= str(period_1) and str(row['goals_date_t2']) <= str(period_2):
            completed_patients_id.append(row['patient_id'])
        if row['completed_by'] == 'patient' and str(row['goals_date_t1']) >= str(period_1) and str(row['goals_date_t2']) <= str(period_2):
            gbo_cleaned.append(row)
    
    #Summary
    st.subheader('Summary')
    st.write('Between the period of ' + str(period_1) + ' and ' + str(period_2) + ', ' + site_name + ' have ' + registered_user + 
    ' registered users on POD. This report summarises the outcome for ' + str(len(completed_patients_id)) + 
    ' cases who had outcome measures for both timepooint 1 and timepoint 2 completed between ' + str(period_1)
    + ' and ' + str(period_2) + '. It is important to note that out of these ' + str(len(completed_patients_id)) +
    ' cases, there are some cases in this report that may have both RCADS and SDQ outcomes. On average, children'
    ' and young people showed reduced anxiety, improved low mood and parents reported reduced behaviour problems.'
    ' Parents and young people also made progress towards their individual interventions goals. Satisfaction with'
    ' the service were high. This report shows that scores on satisfaction measures were consistent with the rest'
    ' of London and the South East. The impliaction of the results from the report are discussed in the conclusion.') 

    #Anxiety and Depression (RCADS)
    rcads_paired = len(rcads_cleaned)
    st.subheader('Anxiety and Depression (RCADS)')
    st.write('In total, ' + str(rcads_paired) + ' cases were identified with paired RCADS data. The data for these '
    'paired cases are analysed below. The paired data shown below is the first completion (time 1) and most recent'
    ' entry (time 2), not necessarily at discharge.')
    rcads_cleaned_df = pd.DataFrame(rcads_cleaned)
    #t1
    rcads_gad_t1 = np.round(rcads_cleaned_df['rcads_tscore_gad_t1'].mean(), 2)
    rcads_mdd_t1 = np.round(rcads_cleaned_df['rcads_tscore_mdd_t1'].mean(), 2)
    rcads_pd_t1 = np.round(rcads_cleaned_df['rcads_tscore_pd_t1'].mean(), 2)
    rcads_sp_t1 = np.round(rcads_cleaned_df['rcads_tscore_sp_t1'].mean(), 2)
    #t2
    rcads_gad_t2 = np.round(rcads_cleaned_df['rcads_tscore_gad_t2'].mean(), 2)
    rcads_mdd_t2 = np.round(rcads_cleaned_df['rcads_tscore_mdd_t2'].mean(), 2)
    rcads_pd_t2 = np.round(rcads_cleaned_df['rcads_tscore_pd_t2'].mean(), 2)
    rcads_sp_t2 = np.round(rcads_cleaned_df['rcads_tscore_sp_t2'].mean(), 2)
    #graph
    rcads_labels = ['GAD','MDD','PD','SP']
    rcads_t1_means = [rcads_gad_t1, rcads_mdd_t1, rcads_pd_t1, rcads_sp_t1]
    rcads_t2_means = [rcads_gad_t2, rcads_mdd_t2, rcads_pd_t2, rcads_sp_t2]
    x = np.arange(len(rcads_labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, rcads_t1_means, width, label='T1')
    rects2 = ax.bar(x + width/2, rcads_t2_means, width, label='T2')
    ax.set_ylabel('Average T-Score')
    ax.set_title('Average T-Score at T1 and T2')
    ax.set_xticks(x)
    ax.set_xticklabels(rcads_labels)
    ax.legend()
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    st.pyplot(fig)
    st.write('The total scores at time 1 were consistent with average scores for services across London and the'
    ' South East indicating a similar level of difficulty at the beginning of the intervention (Major depression'
    ' 70.8; GAD 60.2; Panic 68.3; Social Phobia 55.9).')
    st.write('All subscales showed reductions in average scores by the end of the intervention. The threshold for'
    ' indicating a mental health problem is 65 and above and all groups showed an average reduction away from'
    ' this threshold. This suggests that the service was successful in some areas in providing an early intervention'
    ' for young people at risk of developing a mental health problem.')
    st.write('Data shows an average reduction for anxiety and low mood problems of ' + str(np.round(sum(rcads_t1_means)/len(rcads_t1_means) - sum(rcads_t2_means)/len(rcads_t2_means),2))
    + ' points. This is higher than the average reduction for scores across services in London and the South East'
    ' of approximately 10 points.')
    rcads_gad_above_threshold_t1 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_gad_t1 > 64].shape[0]
    rcads_mdd_above_threshold_t1 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_mdd_t1 > 64].shape[0]
    rcads_pd_above_threshold_t1 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_pd_t1 > 64].shape[0]
    rcads_sp_above_threshold_t1 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_sp_t1 > 64].shape[0]
    rcads_gad_above_threshold_t2 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_gad_t2 > 64].shape[0]
    rcads_mdd_above_threshold_t2 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_mdd_t2 > 64].shape[0]
    rcads_pd_above_threshold_t2 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_pd_t2 > 64].shape[0]
    rcads_sp_above_threshold_t2 = rcads_cleaned_df[rcads_cleaned_df.rcads_tscore_sp_t2 > 64].shape[0]
    rcads_labels_1 = ['GAD','MDD','PD','SP']
    rcads_t1_threshold = [rcads_gad_above_threshold_t1, rcads_mdd_above_threshold_t1, rcads_pd_above_threshold_t1, rcads_sp_above_threshold_t1]
    rcads_t2_threshold = [rcads_gad_above_threshold_t2, rcads_mdd_above_threshold_t2, rcads_pd_above_threshold_t2, rcads_sp_above_threshold_t2]
    fig1, ax1 = plt.subplots()
    rectss1 = ax1.bar(x - width/2, rcads_t1_threshold, width, label='T1')
    rectss2 = ax1.bar(x + width/2, rcads_t2_threshold, width, label='T2')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Scores above threshold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(rcads_labels)
    ax1.legend()
    def autolabel1(rects):
        for rect in rects:
            height = rect.get_height()
            ax1.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')
    autolabel1(rectss1)
    autolabel1(rectss2)
    fig1.tight_layout()
    st.pyplot(fig1)
    st.write('The graph above shows the RCADS subscales. The data shows the number of scores reaching clinical'
    ' threshold for all subscales. This shows CYPs score across the subscales rather than on an individual subscale'
    '. For example, a CYP may score on more than one of the subscales above clinical threshold at timepoint 1.'
    ' Since there are ' + str(rcads_paired) + ' identified paired RCADS, all of the data is out of a possible '
    + str(rcads_paired) + '. Out of the ' + str(rcads_paired) + ' paired RCADS data, all subscales showed a '
    'reduction of scores reaching clinical threshold by the end of intervention.')

    #Behavioural Problems (SDQ)
    sdq_cleaned_df = pd.DataFrame(sdq_cleaned)
    sdq_paired = sdq_cleaned_df['sdq_date_t2'].count()
    sdq_total_t1_avg = np.round(sdq_cleaned_df['sdq_total_t1'].mean(), 2)
    sdq_total_t2_avg = np.round(sdq_cleaned_df['sdq_total_t2'].mean(), 2)
    sdq_total_avg_change = np.round(sdq_total_t1_avg - sdq_total_t2_avg)
    sdq_total_above_threshold_t1 = sdq_cleaned_df[sdq_cleaned_df.sdq_total_t1 > 17].shape[0]
    sdq_total_above_threshold_t2 = sdq_cleaned_df[sdq_cleaned_df.sdq_total_t2 > 17].shape[0]
    st.subheader('Behavioural Problems (SDQ)')
    st.write('The mean Total Difficulties score (' + str(sdq_paired) + ' cases with paired outcomes'
    ' at timepoint 1 was ' + str(sdq_total_t1_avg) + '. The mean Total Difficulties score at timepoint 2 was '
    + str(sdq_total_t2_avg) + '.')
    st.write('There was an average reduction for behaviour problems of ' + str(sdq_total_avg_change) + '.'
    ' This is roughly the same average reduction for such scores across services in London and the South East'
    ' of approximately 4 points.')
    st.write('The total number of cases reaching clinical threshold (as defined as having a Total Difficulties'
    ' score of 17 or more) was ' + str(sdq_total_above_threshold_t1) + ' at timepoint 1. The total number of '
    'cases reaching clinical threshold was ' + str(sdq_total_above_threshold_t2) + ' at timepoint 2.')
    st.write('The IMPACT supplement measures how much the difficulty is interfering with various areas of life '
    '(0 = not at all and 2 = a great deal).')
    #Graph
    sdq_distress_t1 = np.round(sdq_cleaned_df['sdq_impact_distress_t1'].mean(), 2)
    sdq_homelife_t1 = np.round(sdq_cleaned_df['sdq_impact_homelife_t1'].mean(), 2)
    sdq_friendship_t1 = np.round(sdq_cleaned_df['sdq_impact_friendship_t1'].mean(), 2)
    sdq_learning_t1 = np.round(sdq_cleaned_df['sdq_impact_learning_t1'].mean(), 2)
    sdq_leisure_t1 = np.round(sdq_cleaned_df['sdq_impact_leisure_t1'].mean(), 2)
    sdq_distress_t2 = np.round(sdq_cleaned_df['sdq_impact_distress_t2'].mean(), 2)
    sdq_homelife_t2 = np.round(sdq_cleaned_df['sdq_impact_homelife_t2'].mean(), 2)
    sdq_friendship_t2 = np.round(sdq_cleaned_df['sdq_impact_friendship_t2'].mean(), 2)
    sdq_learning_t2 = np.round(sdq_cleaned_df['sdq_impact_learning_t2'].mean(), 2)
    sdq_leisure_t2 = np.round(sdq_cleaned_df['sdq_impact_leisure_t2'].mean(), 2)
    sdq_labels = ['Distress','Homelife','Friendship','Learning','Leisure']
    sdq_t1_impacts = [sdq_distress_t1, sdq_homelife_t1, sdq_friendship_t1, sdq_learning_t1, sdq_leisure_t1]
    sdq_t2_impacts = [sdq_distress_t2, sdq_homelife_t2, sdq_friendship_t2, sdq_learning_t2, sdq_leisure_t2]
    x1 = np.arange(len(sdq_labels))
    fig2, ax2 = plt.subplots()
    rectsss1 = ax2.bar(x1 - width/2, sdq_t1_impacts, width, label='T1')
    rectsss2 = ax2.bar(x1 + width/2, sdq_t2_impacts, width, label='T2')
    ax2.set_ylabel('Impact Score')
    ax2.set_title('Average Impact Score')
    ax2.set_xticks(x1)
    ax2.set_xticklabels(sdq_labels)
    ax2.legend()
    def autolabel2(rects):
        for rect in rects:
            height = rect.get_height()
            ax2.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width()/2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')
    autolabel2(rectsss1)
    autolabel2(rectsss2)
    fig2.tight_layout()
    st.pyplot(fig2)
    st.write('There was an average reduction for impact scores across nearly all domains. Average reductions '
    'for such scores across services in London and the South East were consistent with those reported here.')

    #Goal based Outcomes
    gbo_cleaned_df = pd.DataFrame(gbo_cleaned)
    g1_avg_t1 = gbo_cleaned_df['goals_g1score_t1'].mean()
    g2_avg_t1 = gbo_cleaned_df['goals_g2score_t1'].mean()
    g3_avg_t1 = gbo_cleaned_df['goals_g3score_t1'].mean()
    g1_avg_t2 = gbo_cleaned_df['goals_g1score_t2'].mean()
    g2_avg_t2 = gbo_cleaned_df['goals_g2score_t2'].mean()
    g3_avg_t2 = gbo_cleaned_df['goals_g3score_t2'].mean()
    gbo_avg_t1 = np.round((g1_avg_t1 + g2_avg_t1 + g3_avg_t1)/3,2)
    gbo_avg_t2 = np.round((g1_avg_t2 + g2_avg_t2 + g3_avg_t2)/3,2)
    gbo_avg_diff = np.round(gbo_avg_t2 - gbo_avg_t1,2)
    gbo_table = pd.DataFrame({'T1': [gbo_avg_t1], 'T2': [gbo_avg_t2]})
    gbo_table.index = ['Average GBO Score']
    st.subheader('Goal Based Outcomes')
    st.write(str(site_name) + ' have ' + str(len(gbo_cleaned)) + ' cases with paired goal ratings. The table below'
    ' shows the mean score between timepoint 1 and 2.')
    #Table
    st.write(gbo_table)
    st.write('The data from ' + site_name + ' showed an average improvement in relation to goals of ' + str(gbo_avg_diff)
    + ' between Time 1 and Time 2. This is roughly the same as average improvements in goals across services in'
    + ' London and the South East of 4.4')

    #ESQ
    if esq_parent_carer or esq_self_12_18 or esq_self_9_11:
        esq_parent_carer_df = pd.DataFrame(esq_parent_carer)
        esq_self_12_18_df = pd.DataFrame(esq_self_12_18)
        esq_self_9_11_df = pd.DataFrame(esq_self_9_11)
        st.subheader('Experience of Service Questionnaire')
        st.write('The ESQs were given to clients at the end of intervention. In ' + site_name + ', the ESQ was '
        'completed by ' + str(esq_parent_carer_df.shape[0] + esq_self_12_18_df.shape[0] + esq_self_9_11_df.shape[0])
        + ' clients. The ESQ Parent was completed by ' + str(esq_parent_carer_df.shape[0]) + ' clients.'
        + ' The ESQ Self 12-18 was completed by ' + str(esq_self_12_18_df.shape[0]) + ' clients.'
        + ' The ESQ Self 9-11 was completed by ' + str(esq_self_9_11_df.shape[0]) + ' clients.')
    
    #Conclusion
    st.subheader('Conclusion')
    st.write('Overall ' + site_name + ' have showed positive positive outcomes. The data from the outcome measures'
    ' show that the CWPs have been overall successful in reducing anxiety, improving low mood and reducing behaviour'
    ' problems. This is shown by the following:')
    st.write('- Reduction of RCADS average score for a majority of the subscales over time.')
    st.write('- Reduction of cases in clinical threshold over time (Majority of RCADS subscales and SDQ).')
    st.write('- Reduction of IMPACT scores (SDQ) over time.')
    st.write('- Parents and young people feeling they have reached their goals.')
    st.write('This report demonstrates that the CWP programme is delivering an early help intervention for young'
    ' people before symptoms are exacerbated. Service user satisfaction with the interventions is reflected in'
    ' the ESQ.')

    #RCADS
    st.subheader('RCADS DataFrame - cleaned')
    st.dataframe(rcads_cleaned_df)
    #SDQ
    st.subheader('SDQ DataFrame - cleaned')
    st.dataframe(sdq_cleaned_df)
    #GBO
    st.subheader('GBO DataFrame - cleaned')
    st.dataframe(gbo_cleaned_df)

if st.button('Run report'):
    #Validation
    if site_name == '' or registered_user == '' or rcads == None or sdq == None or gbo == None:
        st.error('Please complete all required fields. You have missed an important field.')
    else:
        site_report()
