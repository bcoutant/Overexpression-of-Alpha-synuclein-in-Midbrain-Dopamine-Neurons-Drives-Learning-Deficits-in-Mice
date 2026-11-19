#%% Import packages and df

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")
df_cog3 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")
df_cog5 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase5-1and2_BC-XZ.xlsx")

#%% Analysis Phase 2

#palette={"CTL":"#B4CBF0", "asyn":"#CAA3EF"}# Light blue and purple
palette={"CTL":"#000000", "asyn":"#E42217"}# Red and black

####
#### 2months 
####

# Pepare data frame 


df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

s_cog2 = df_cog2[(df_cog2['Time']=='2months')]
s_cog2['Nb_side_omissions'] = s_cog2['L_Nb_omissions'] + s_cog2['R_Nb_omissions']
s_cog2['TOT_NP'] = s_cog2.fillna(0)['TOT_LNP'] + s_cog2.fillna(0)['TOT_CNP'] + s_cog2.fillna(0)['TOT_RNP']
s_cog2['Side_NP'] = s_cog2.fillna(0)['TOT_LNP'] + s_cog2.fillna(0)['TOT_RNP']
s_cog2['Avg_RT'] = s_cog2['Avg_RT']/1000 # in seconds
s_cog2['Pct_Side_Omissions'] = s_cog2['Pct_Side_Omissions']*100 # in %

s_cog2= s_cog2[["Mouse", "Condition", "Sexe", "Phase", "Time", "Day", "Housing", "Time_Light-to-LNP-ms", 
                 "Time_Light-to-RNP-ms","TOT_LNP", "TOT_CNP", 'TOT_RNP', "TOT_NP", "Avg_RT", "Avg_success_both_sides", 
                 "Nb_side_omissions", 'Side_NP', 'Pct_Side_Omissions']]


# Histology Exclusion FINAL 1/31

ss_cog2=s_cog2[(~s_cog2['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AY31']))]  #filter based on histo 01/16 -- red
ss_cog2=ss_cog2[(~ss_cog2['Mouse'].isin(['AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52']))] #filter dead mice


# Make Figures
#Average Success
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_success_both_sides", hue = "Condition", markers='o', scale=2., color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
#plt.xlim(xmin=0)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful Trials (%)", size = 25)
plt.title(label= 'Phase 2, 8 weeks', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_LearningCurve_12Days.tiff", dpi=500, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_LearningCurve_12Days.pdf", dpi=500, format="pdf")



ss_cog2 = ss_cog2[(ss_cog2['Day']<7)]
ss_cog2["Day"] = ss_cog2["Day"].astype(int)

#Average Success
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_success_both_sides", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
#ax.set_yticks([0, 25, 50, 75, 100])
#plt.xlim(xmin=-1)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful Trials (%)", size = 25)
plt.title(label= 'Phase 2, 8 weeks', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_LearningCurve.tiff", dpi=500, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_LearningCurve.pdf", dpi=500, format="pdf")

#Average RT
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_RT", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=12)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Reaction Time (s)", size = 25)
plt.title(label= 'Phase2, 8weeks - Reaction Time', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_ReactionTime.tiff", dpi=500, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_ReactionTime.pdf", dpi=500, format="pdf")


#Nb of side Omissions
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Nb_side_omissions", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=120)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Omissions", size = 25)
plt.title(label= 'Phase2, 8weeks - Total Omissions', fontsize=30)
# highest nb of omissions in asyn over time, decay slower -- no learning, no decay over time
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_Nb_side_omissions.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_Nb_side_omissions.pdf", dpi=300, format="pdf")

# Pct side Omissions
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Pct_Side_Omissions", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Omissions", size = 25)
plt.title(label= 'Phase2, 8weeks - Pct_Side_Omissions', fontsize=30)
# highest nb of omissions in asyn over time, decay slower -- no learning, no decay over time
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_Pct-Side-Omissions.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_Pct-Side-Omissions.pdf", dpi=300, format="pdf")


#Number of Nosepoke
#Central
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "TOT_CNP", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=1200)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Total Number of \n center nosepokes", size = 25)
plt.title(label= 'Phase2, 8weeks - Central NP', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_CentralNP.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_CentralNP.pdf", dpi=300, format="pdf")


#Side
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Side_NP", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=300)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Total Number of \n side nosepokes", size = 25)
plt.title(label= 'Phase2, 8weeks - Side NP', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_8weeks_SideNP.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_8weeks_SideNP.pdf", dpi=300, format="pdf")


#### 
#### 3 weeks
####


df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")
# Histology Exclusion for all mice
#s_cog2 = df_cog2[(~df_cog2['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ10', 'AQ6']))]

s_cog2 = df_cog2[(df_cog2['Time']=='3weeks')]

s_cog2['Nb_side_omissions'] = s_cog2['L_Nb_omissions'] + s_cog2['R_Nb_omissions']
s_cog2['TOT_NP'] = s_cog2.fillna(0)['TOT_LNP'] + s_cog2.fillna(0)['TOT_CNP'] + s_cog2.fillna(0)['TOT_RNP']
s_cog2['Side_NP'] = s_cog2.fillna(0)['TOT_LNP'] + s_cog2.fillna(0)['TOT_RNP']
s_cog2['Avg_RT'] = s_cog2['Avg_RT']/1000 # in seconds
s_cog2['Pct_Side_Omissions'] = s_cog2['Pct_Side_Omissions']*100 # in %


s_cog2= s_cog2[["Mouse", "Condition", "Sexe", "Phase", "Time", "Day", "Housing", "Time_Light-to-LNP-ms", 
                 "Time_Light-to-RNP-ms","TOT_LNP", "TOT_CNP", 'TOT_RNP', "TOT_NP", "Avg_RT", "Avg_success_both_sides", 
                 "Nb_side_omissions", 'Pct_Side_Omissions']]

# Histo exclusion final January 2025
ss_cog2=s_cog2[(~s_cog2['Mouse'].isin(['AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6']))] 
ss_cog2=ss_cog2[(~ss_cog2['Mouse'].isin(['AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52']))] #filter dead mice

#Learning Curve - 12days 

ss_cog2 = ss_cog2[(ss_cog2['Day']<13)]
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_success_both_sides", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful Trials (%)", size = 25)
plt.title(label= 'Phase 2, 3 weeks', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_RewardedTrials_12Days.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_RewardedTrials_12Days.pdf", dpi=300, format="pdf")


# Figures
#Learning Curve - 6days
ss_cog2 = ss_cog2[(ss_cog2['Day']<7)]
ss_cog2["Day"] = ss_cog2["Day"].astype(int)

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_success_both_sides", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
#ax.set_yticks([0, 25, 50, 75, 100])
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful Trials (%)", size = 25)
plt.title(label= 'Phase 2, 3 weeks', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_LearningCurve_6Days.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_LearningCurve_6Days.pdf", dpi=300, format="pdf")


# Reaction Time 
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Avg_RT", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=12)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Reaction Time (s)", size = 25)
plt.title(label= 'Phase 2, 3 weeks', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_ReactionTime.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_ReactionTime.pdf", dpi=300, format="pdf")


#Number of Nosepoke
#Central
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "TOT_CNP", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=1200)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Total Number of \n center nosepokes", size = 25)
plt.title(label= 'Phase2, 3weeks - Central NP', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_CentralNP.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_CentralNP.pdf", dpi=300, format="pdf")


#Side
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Side_NP", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=300)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Total Number of \n side nosepokes", size = 25)
plt.title(label= 'Phase2, 3weeks - Side NP', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_SideNP.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_SideNP.pdf", dpi=300, format="pdf")



#%% Extra data and figures 

# Pct side Omissions
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog2, x = "Day", y = "Pct_Side_Omissions", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Omissions", size = 25)
plt.title(label= 'Phase2, 3weeks - Omissions', fontsize=30)
# highest nb of omissions in asyn over time, decay slower -- no learning, no decay over time
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase2_3weeks_Pct-Side-Omissions.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase2_3weeks_Pct-Side-Omissions.pdf", dpi=300, format="pdf")


#Each Mouse - asyn
sns.pointplot(data = ss_cog2[(ss_cog2['Condition']=='asyn')], x = "Day", y = "Avg_success_both_sides", hue = "Mouse", errorbar = "se").set(title='Phase 2 _ 3weeks _ asyn')
#Each Mouse - CTL
sns.pointplot(data = ss_cog2[(ss_cog2['Condition']=='CTL')], x = "Day", y = "Avg_success_both_sides", hue = "Mouse", errorbar = "se").set(title='Phase 2 _ 3weeks _ CTL')
plt.show()
## No one diff between CTL and asyn - both condition have good and bad leaners. Actually CTL has more bas ones


####
#### Phase3 


df_cog3 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")
df_cog3test = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")

df_cog3["Day"] = pd.to_numeric(df_cog3["Day"])

s_cog3=df_cog3[(df_cog3['Time']=='3weeks')]
#s_cog3=df_cog3[(df_cog3['Experimenter']=='BC')]

#Figures 12 Days
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = s_cog3, x = "Day", y = "Successful_trials", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=120)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful_trials", size = 25)
plt.title(label= 'Phase3, 3weeks - Successful Trials', fontsize=30)

# Exclusion criteria

# =============================================================================
# subset = ss_cog2[
#     (ss_cog2["Day"] < 13) &  # Check if the day is within 12 days
#     (ss_cog2["Avg_success_both_sides"] >= 80)  # Check if success percentage is 80% or higher
# ]
# mice_reached_80 = subset["Mouse"].unique()
# 
# 
# ss_cog3=s_cog3[(s_cog3['Day']<7)]
# ss_cog3=s_cog3[s_cog3['Mouse'].isin(mice_reached_80)] 
# 
# =============================================================================

ss_cog3=s_cog3[(s_cog3['Day']<7)]

#Figures Successful trials

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "Successful_trials", hue = "Condition", markers='o', scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=100)
#plt.yticks(np.arange(0, 100, step=50))
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Successful_trials", size = 25)
plt.title(label= 'Phase3, 3weeks - Successful Trials', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_SuccessfulTrials_Max100.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_SuccessfulTrials_Max100.pdf", dpi=300, format="pdf")



#%% Other metrics Phase3
## RT to start trial

ss_cog3['RT_C_light_ON_npC'] = ss_cog3['RT_C_light_ON_npC']/1000 # in seconds

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "RT_C_light_ON_npC", hue = "Condition", markers='o', scale=2.5, errorbar = "se", palette=palette).set(title='Phase 3 _ 3weeks - RT to start trial - Exclusion only histo')
plt.ylim(ymin=0, ymax=4)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("RT_C_light_ON_npC", size = 25)
plt.title(label= 'Phase3, 3weeks - RT to start trial', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_RT-to-start-trial.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_RT-to-start-trial.pdf", dpi=300, format="pdf")


## Nb omissions and errors
ss_cog3['Incorrect'] = ss_cog3['L_assigned_but_R'] + ss_cog3['R_assigned_but_L']

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "Incorrect", hue = "Condition", markers='o', scale=2.5, errorbar = "se", palette=palette).set(title='Phase 3 _ 3weeks - Errors (L but R or R but L) - Exclusion only histo')
plt.ylim(ymin=0, ymax=20)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Incorrect", size = 25)
plt.title(label= 'Phase3, 3weeks - Errors (L but R or R but L)', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_MissassignedSideErrors.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_MissassignedSideErrors.pdf", dpi=300, format="pdf")


## Center omissions
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "C_omission", hue = "Condition", markers='o', scale=2.5, errorbar = "se", palette=palette).set(title='hase 3 _ 3weeks - Center omission')
plt.ylim(ymin=0, ymax=60)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Center omission", size = 25)
plt.title(label= 'Phase 3 _ 3weeks - Center omission', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_CenterOmission.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_CenterOmission.pdf", dpi=300, format="pdf")



## Side omissions
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "Side_omission", hue = "Condition", markers='o', scale=2.5, errorbar = "se", palette=palette).set(title='hase 3 _ 3weeks - Center omission')
plt.ylim(ymin=0, ymax=30)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Side omission", size = 25)
plt.title(label= 'Phase 3 _ 3weeks - Side omission', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_SideOmission.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_SideOmission.pdf", dpi=300, format="pdf")



## Total omissions
ss_cog3['TOT_omissions'] = ss_cog3['C_omission'] + ss_cog3['Side_omission']

plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = ss_cog3, x = "Day", y = "TOT_omissions", hue = "Condition", markers='o', scale=2.5, errorbar = "se", palette=palette).set(title='hase 3 _ 3weeks - Total omissions')
plt.ylim(ymin=0, ymax=60)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Total omissions", size = 25)
plt.title(label= 'Phase 3 _ 3weeks - Total omissions', fontsize=30)
plt.tight_layout()
# Save as TIFF
plt.savefig("Phase3_3weeks_TotalOmission.tiff", dpi=300, format="tiff")
# Save as PDF
plt.savefig("Phase3_3weeks_TotalOmission.pdf", dpi=300, format="pdf")




#%% Number of mouse excluded. Binned days
 
''' I will bin the days into categories and show boxplot representing the proportion of mice 
reaching criteria in each bin ''' 

def days_to_reach_criteria (group, treshold=80):
    firstday = group[group['Avg_success_both_sides']>80]['Day'].min()
    #firstday = group[group['Successful_trials']>80]['Day'].min()
    if np.isnan(firstday) or firstday > 12:
        firstday = 13
        note = 'Did not reach criteria in 12 days'
    else:
        note = 'reached criteria in 12 days'
    
    return pd.Series({'Days_to_criteria': firstday, 'Note': note})


# Pepare data frame 
df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")
s_cog2=df_cog2[(~df_cog2['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AY31', 'AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6']))]   
#filter based on histo 10/09 and 09/01 -- red
s_cog2=s_cog2[(~s_cog2['Mouse'].isin(['AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52']))] #filter dead mice
s_cog2=s_cog2[(s_cog2['Time']=='3weeks')]
s_cog2=s_cog2[(s_cog2['Time']=='2months')]

#s_cog2["Days_to_Criterion"] = s_cog2.groupby("Mouse").apply(days_to_reach_criteria).reset_index(level=0, drop=True)
        
res = s_cog2.groupby('Mouse').apply(days_to_reach_criteria)
#res = s_cog3.groupby('Mouse').apply(days_to_reach_criteria)
df_days_to_reach = pd.merge(res, df_cog2[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach = df_days_to_reach.drop_duplicates().reset_index(drop=True)

bins = [0, 6, 12, float('inf')]
labels = ["0-6 days", "7-12 days", ">12 days"]
df_days_to_reach["Day_Bins"] = pd.cut(df_days_to_reach["Days_to_criteria"], bins=bins, labels=labels, right=True)

bin_counts = df_days_to_reach.groupby(["Condition", "Day_Bins"]).size()

# Calculate the total counts per condition
total_counts_per_condition = bin_counts.groupby(level=0).sum()

# Calculate the proportion for each condition within each bin
proportion_df = (bin_counts / bin_counts.groupby(level=0).transform("sum")).reset_index(name="Proportion")

# Plotting the data
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=proportion_df, x="Day_Bins", y="Proportion", hue="Condition", palette={"CTL":"#000000", "asyn":"#E42217"})
plt.ylim(ymin=0, ymax=1)
plt.tick_params(axis='x', length=10, labelsize=30)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=30)  # Adjust y-axis label size
plt.xlabel("Days to reach criteria", size = 30)
plt.ylabel("Proportion of mice reaching \n 80% successfull trials", size = 30)
plt.title(label= 'Subtle Deficit in Instrumental Learning At 8 Weeks', fontsize=40)
plt.tight_layout()
# Save as PDF
plt.savefig("Prop-Mice-Reaching-Criteria_BinnedTime_8weeks.pdf", dpi=300, format="pdf", bbox_inches='tight')


#%% Number of mouse excluded. 8 weeks

# Pepare data frame 
df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")
s_cog2=df_cog2[(~df_cog2['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AY31', 'AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6']))]   
s_cog2=s_cog2[(~s_cog2['Mouse'].isin(['AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52']))] #filter dead mice
s_cog2=s_cog2[(s_cog2['Time']=='2months')]

#s_cog2["Days_to_Criterion"] = s_cog2.groupby("Mouse").apply(days_to_reach_criteria).reset_index(level=0, drop=True)
        
res = s_cog2.groupby('Mouse').apply(days_to_reach_criteria)
df_days_to_reach = pd.merge(res, df_cog2[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach = df_days_to_reach.drop_duplicates().reset_index(drop=True)

bins = [0, 6, 12, float('inf')]
labels = ["0-6 days", "7-12 days", ">12 days"]
df_days_to_reach["Day_Bins"] = pd.cut(df_days_to_reach["Days_to_criteria"], bins=bins, labels=labels, right=True)

bin_counts = df_days_to_reach.groupby(["Condition", "Day_Bins"]).size()

# Calculate the total counts per condition
total_counts_per_condition = bin_counts.groupby(level=0).sum()

# Calculate the proportion for each condition within each bin
proportion_df = (bin_counts / bin_counts.groupby(level=0).transform("sum")).reset_index(name="Proportion")

# Plotting the data
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=proportion_df, x="Day_Bins", y="Proportion", hue="Condition", palette={"CTL":"#000000", "asyn":"#E42217"})
plt.ylim(ymin=0, ymax=1)
plt.tick_params(axis='x', length=10, labelsize=30)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=30)  # Adjust y-axis label size
plt.xlabel("Days to reach criteria", size = 30)
plt.ylabel("Proportion of mice reaching \n 80% successfull trials", size = 30)
plt.title(label= 'Subtle Deficit in Instrumental Learning At 8 Weeks', fontsize=40)
plt.tight_layout()
# Save as PDF
plt.savefig("Prop-Mice-Reaching-Criteria_BinnedTime_8weeks.pdf", dpi=300, format="pdf", bbox_inches='tight')


#%%  Proportion to reach - Phase 3. Binned days. 3 weeks

def days_to_reach_criteria_phase3 (group, treshold=80):
    firstday = group[group['Successful_trials']>80]['Day'].min()
    #firstday = group[group['Successful_trials']>80]['Day'].min()
    if np.isnan(firstday) or firstday > 12:
        firstday = 13
        note = 'Did not reach criteria in 12 days'
    else:
        note = 'reached criteria in 12 days'
    
    return pd.Series({'Days_to_criteria': firstday, 'Note': note})



# Pepare data frame 
df_cog3 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")
df_cog3["Day"] = pd.to_numeric(df_cog3["Day"])
s_cog3=df_cog3[(df_cog3['Time']=='3weeks')]

#s_cog2["Days_to_Criterion"] = s_cog2.groupby("Mouse").apply(days_to_reach_criteria).reset_index(level=0, drop=True)
        
res = s_cog3.groupby('Mouse').apply(days_to_reach_criteria_phase3)
df_days_to_reach = pd.merge(res, df_cog3[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach = df_days_to_reach.drop_duplicates().reset_index(drop=True)

bins = [0, 6, 12, float('inf')]
labels = ["0-6 days", "7-12 days", ">12 days"]
df_days_to_reach["Day_Bins"] = pd.cut(df_days_to_reach["Days_to_criteria"], bins=bins, labels=labels, right=True)

bin_counts = df_days_to_reach.groupby(["Condition", "Day_Bins"]).size()

# Calculate the total counts per condition
total_counts_per_condition = bin_counts.groupby(level=0).sum()

# Calculate the proportion for each condition within each bin
proportion_df = (bin_counts / bin_counts.groupby(level=0).transform("sum")).reset_index(name="Proportion")

# Plotting the data
plt.figure(figsize=(12, 8))
ax = sns.barplot(data=proportion_df, x="Day_Bins", y="Proportion", hue="Condition", palette={"CTL":"#000000", "asyn":"#E42217"})
plt.ylim(ymin=0, ymax=1)
plt.tick_params(axis='x', length=10, labelsize=30)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=30)  # Adjust y-axis label size
plt.xlabel("Days to reach criteria", size = 30)
plt.ylabel("Proportion of mice reaching \n 80% successfull trials", size = 30)
plt.title(label= 'Subtle Deficit in Instrumental Learning At 3 Weeks _ Phase3', fontsize=40)
plt.tight_layout()
# Save as PDF
plt.savefig("Prop-Mice-Reaching-Criteria_BinnedTime_3weeks_Phase3.pdf", dpi=300, format="pdf", bbox_inches='tight')


#%% Proportion to reach - Phase3. 3 weeks. 

# Pepare data frame 
df_cog3 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")
df_cog3["Day"] = pd.to_numeric(df_cog3["Day"])
s_cog3=df_cog3[(df_cog3['Time']=='3weeks')]


res2 = s_cog3.groupby('Mouse').apply(days_to_reach_criteria_phase3)
df_days_to_reach2 = pd.merge(res2, df_cog3[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach2 = df_days_to_reach2.drop_duplicates().reset_index(drop=True)
df_days_to_reach2['Reached_Criteria'] = df_days_to_reach2['Days_to_criteria'] <= 12

total_mice_per_condition = df_days_to_reach2.groupby('Condition')['Mouse'].nunique()
mice_reaching_criteria = df_days_to_reach2[df_days_to_reach2['Reached_Criteria']].groupby('Condition')['Mouse'].nunique()
proportion_reaching_criteria = mice_reaching_criteria / total_mice_per_condition


df_proportions = pd.DataFrame({
    'Total_Mice': total_mice_per_condition,
    'Reached_Criteria': mice_reaching_criteria,
    'Proportion': proportion_reaching_criteria
}).reset_index()

df_proportions['Not_Reached_Criteria'] = df_proportions['Total_Mice'] - df_proportions['Reached_Criteria']

# Iterate over each condition
for _, row in df_proportions.iterrows():
    condition = row['Condition']
    sizes = [row['Reached_Criteria'], row['Not_Reached_Criteria']]
    labels = ['Reached Criteria', 'Did Not Reach Criteria']
    colors = ['#FEC98F', '#FDF1AD']  # Green for reached, red for not reached
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6))  # Use `fig, ax` to control figure
    
    # Create pie chart
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
    )
    ax.set_title(f'Proportion of Mice in Condition: {condition} at 3 Weeks')
    
    plt.tight_layout()
    
    # Define a unique filename per condition
    filename = f"Prop-Mice-Reaching-Criteria_{condition}_PieChart_3weeks_Phase3.pdf"
    
    # Save plot with unique name
    fig.savefig(filename, dpi=300, format="pdf", bbox_inches='tight')
    
    # Show plot (optional, can slow down script if many plots)
    plt.show()
    
    # Close figure to prevent memory issues
    plt.close(fig)

#%% Proportion to Reach. Pie Chart. Phase2. 3 or 8 weeks

def days_to_reach_criteria (group, treshold=80):
    firstday = group[group['Avg_success_both_sides']>80]['Day'].min()
    #firstday = group[group['Successful_trials']>80]['Day'].min()
    if np.isnan(firstday) or firstday > 12:
        firstday = 13
        note = 'Did not reach criteria in 12 days'
    else:
        note = 'reached criteria in 12 days'
    
    return pd.Series({'Days_to_criteria': firstday, 'Note': note})


# Pepare data frame 
df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")
s_cog2=df_cog2[(~df_cog2['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AY31', 'AB1', 'AD1', 'AE7', 'AG3', 'AH4', 'AI8', 'AK1', 'AK22', 'AK4', 'AM22', 'AO6', 'AP0', 'AP4', 'AQ6']))]   
#filter based on histo 10/09 and 09/01 -- red
s_cog2=s_cog2[(~s_cog2['Mouse'].isin(['AZ4', 'AZ6', 'AZ7', 'AX3', 'AQ52']))] #filter dead mice
#s_cog2=s_cog2[(s_cog2['Time']=='2months')]
s_cog2=s_cog2[(s_cog2['Time']=='3weeks')]

res2 = s_cog2.groupby('Mouse').apply(days_to_reach_criteria)
df_days_to_reach2 = pd.merge(res2, df_cog2[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach2 = df_days_to_reach2.drop_duplicates().reset_index(drop=True)
df_days_to_reach2['Reached_Criteria'] = df_days_to_reach2['Days_to_criteria'] <= 12

total_mice_per_condition = df_days_to_reach2.groupby('Condition')['Mouse'].nunique()
mice_reaching_criteria = df_days_to_reach2[df_days_to_reach2['Reached_Criteria']].groupby('Condition')['Mouse'].nunique()
proportion_reaching_criteria = mice_reaching_criteria / total_mice_per_condition


df_proportions = pd.DataFrame({
    'Total_Mice': total_mice_per_condition,
    'Reached_Criteria': mice_reaching_criteria,
    'Proportion': proportion_reaching_criteria
}).reset_index()

df_proportions['Not_Reached_Criteria'] = df_proportions['Total_Mice'] - df_proportions['Reached_Criteria']

# Iterate over each condition
for _, row in df_proportions.iterrows():
    condition = row['Condition']
    sizes = [row['Reached_Criteria'], row['Not_Reached_Criteria']]
    labels = ['Reached Criteria', 'Did Not Reach Criteria']
    colors = ['#FEC98F', '#FDF1AD']  # Green for reached, red for not reached
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6))  # Use `fig, ax` to control figure
    
    # Create pie chart
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
    )
    ax.set_title(f'Proportion of Mice in Condition: {condition} at 3 Weeks')
    
    plt.tight_layout()
    
    # Define a unique filename per condition
    filename = f"Prop-Mice-Reaching-Criteria_{condition}_PieChart_3weeks_Phase2.pdf"
    
    # Save plot with unique name
    fig.savefig(filename, dpi=300, format="pdf", bbox_inches='tight')
    
    # Show plot (optional, can slow down script if many plots)
    plt.show()
    
    # Close figure to prevent memory issues
    plt.close(fig)



#%% Phase 3. Pie Chart. Prop of excluded

def days_to_reach_criteria_phase3 (group, treshold=80):
    firstday = group[group['Successful_trials']>80]['Day'].min()
    #firstday = group[group['Successful_trials']>80]['Day'].min()
    if np.isnan(firstday) or firstday > 12:
        firstday = 13
        note = 'Did not reach criteria in 12 days'
    else:
        note = 'reached criteria in 12 days'
    
    return pd.Series({'Days_to_criteria': firstday, 'Note': note})


df_cog3 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase3_BC-XZ.xlsx")
df_cog3["Day"] = pd.to_numeric(df_cog3["Day"])
s_cog3=df_cog3[(df_cog3['Time']=='3weeks')]

res3 = s_cog3.groupby('Mouse').apply(days_to_reach_criteria_phase3)
df_days_to_reach3 = pd.merge(res3, df_cog3[['Mouse', 'Sexe', 'Condition', 'Time']], on = 'Mouse', how='left')
df_days_to_reach3 = df_days_to_reach3.drop_duplicates().reset_index(drop=True)
df_days_to_reach3['Reached_Criteria'] = df_days_to_reach3['Days_to_criteria'] <= 12

total_mice_per_condition = df_days_to_reach3.groupby('Condition')['Mouse'].nunique()
mice_reaching_criteria = df_days_to_reach3[df_days_to_reach3['Reached_Criteria']].groupby('Condition')['Mouse'].nunique()
proportion_reaching_criteria = mice_reaching_criteria / total_mice_per_condition


df_proportions = pd.DataFrame({
    'Total_Mice': total_mice_per_condition,
    'Reached_Criteria': mice_reaching_criteria,
    'Proportion': proportion_reaching_criteria
}).reset_index()

df_proportions['Not_Reached_Criteria'] = df_proportions['Total_Mice'] - df_proportions['Reached_Criteria']

# Iterate over each condition
for _, row in df_proportions.iterrows():
    condition = row['Condition']
    sizes = [row['Reached_Criteria'], row['Not_Reached_Criteria']]
    labels = ['Reached Criteria', 'Did Not Reach Criteria']
    colors = ['#FEC98F', '#FDF1AD']  # Green for reached, red for not reached
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6))  # Use `fig, ax` to control figure
    
    # Create pie chart
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
    )
    ax.set_title(f'Proportion of Mice in Condition: {condition} at 3 Weeks')
    plt.tight_layout()
    # Define a unique filename per condition
    filename = f"Prop-Mice-Reaching-Criteria_{condition}_PieChart_3weeks_Phase3.pdf"
    # Save plot with unique name
    fig.savefig(filename, dpi=300, format="pdf", bbox_inches='tight')
    # Show plot (optional, can slow down script if many plots)
    plt.show()
    # Close figure to prevent memory issues
    plt.close(fig)

#%% Test ad libitum sweets in homecage - 8 weeks only 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df_motiv = pd.read_excel(r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\MotivationTest_AdlibitumFood.xlsx')

df_motiv=df_motiv[(~df_motiv['Mouse'].isin(['Nb0', 'Nb1', 'Nb2', 'Nb3', 'AY31']))]   

sub = df_motiv[['Condition', 'Food_consumed_Hourly']].dropna()
sub = sub[sub['Condition'].isin(['CTL', 'asyn'])]


#palette={"CTL":"#B4CBF0", "asyn":"#CAA3EF"}# Light blue and purple
palette={"CTL":"#000000", "asyn":"#E42217"}# Red and black
order = ['CTL', 'asyn']

# fig = plt.figure(figsize =(10, 7))
 
# # Creating axes instance
# ax = fig.add_axes([0, 0, 1, 1])
 
# # Creating plot
fig, ax = plt.subplots(figsize=(4, 5))

sns.boxplot(data=sub, x="Condition", y="Food_consumed_Hourly", palette=palette, order=order, width=0.3).set(title='Ad Libitum Food Consumption')
sns.stripplot(x='Condition', y='Food_consumed_Hourly', order=order, color='black', size = 10, data=sub, jitter=0.1)

ax.set_title("Food consummed in homecage")
ax.set_ylim(0, 0.8)

plt.tight_layout()

# Show first, then save
plt.show()
fig.savefig("MotivationTest_AdLibitum_FoodConsummed_8weeks_AfterPhase2.pdf", dpi=300, format="pdf", bbox_inches='tight')



#%% Motivation - Phase 1: Latency to react 

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

os.chdir(r"C:\Users\beren\.spyder-py3\berenice")
path = r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Phase1_Files\Analysis_Files'


def calculate_average_latency(path):
    
    # Initialize an empty DataFrame to store the results
    results_df_phase1 = pd.DataFrame(columns=['Mouse', 'Date', 'AvgLatency', 'Phase'])
    results_list_phase1 = []
    
    for filename in os.listdir(path):
        # Take only file ending by .csv
        if filename.endswith(".csv"):
            
            # Construct the full file path -- need to read the file
            file_path = os.path.join(path, filename)
            
            #Extract element from filename and store them in variable called mouse, date, phase
            ele_filename = filename.split('_')
            mouse = ele_filename[0]
            date = ele_filename[1]
            phase = ele_filename[2]
            
            # Read the CSV file
            df = pd.read_csv(file_path, header=None, delimiter=',', keep_default_na=False, on_bad_lines='skip')
            # Ensure there are at least two columns
            if df.shape[1] < 2:
                print(f"File {filename} does not have at least two columns. Skipping.")
                continue
            
            df = pd.read_csv(file_path, header=None, delimiter=',', keep_default_na=False, on_bad_lines='skip')
            
            #Extract latencies by index (second column)
            latencies = df.iloc[:,1]
            latencies_sec = latencies/1000 # put in seconds
            
            # Calculate the average latency
            average_latency = latencies_sec.mean()
    
            # Create DataFrame with the results
            result_df = pd.DataFrame({'Mouse': [mouse], 'Date': [date], 'AvgLatency': [average_latency], 'Phase': [phase]})
            
            # Add the result DataFrame to the list
            results_list_phase1.append(result_df)
       
    # Combine all results into a single DataFrame
    results_df_phase1 = pd.concat(results_list_phase1, ignore_index=True)
    
    print(results_df_phase1)
    return(results_df_phase1)


# Crossing information from df_cog2 (Conditon and Sexe) for results_df_phase1
df_cog2 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase2_BC-WZ.xlsx")

path = r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Phase1_Files\Analysis_Files'
path_2months = r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Phase1_Files\Analysis_Files\2months\Berenice'
# Fonction calculating latencies 

results_df_phase1 = calculate_average_latency(path=path_2months)
results_df_phase1 = calculate_average_latency(path=path)

## Histo 30/01
results_df_phase1=results_df_phase1[(~results_df_phase1['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AB1', 'AE7', 'AH4', 'AI8', 'AK1', 'AK4', 'AM22', 'AP0', 'AQ6', 'AD1', 'AG3', 'AK22', 'AO6', 'AP4', 'AY31']))]
results_df_phase1=results_df_phase1.reset_index(drop=True)

#Combine info
columns_to_merge = ['Mouse', 'Condition', 'Sexe']
df_phase1 = pd.merge(results_df_phase1, df_cog2[columns_to_merge], on='Mouse', how='left')
df_phase1_unique = df_phase1.drop_duplicates().reset_index(drop=True)


####
#### Plot latencies of Phase 1 between control and asyn
####

#palette_point={"CTL":"#A7A7A7", "asyn":"#A7A7A7"}
#palette={"CTL":"#B4CBF0", "asyn":"#CAA3EF"}# Light blue and purple

palette={"CTL":"#000000", "asyn":"#E42217"}
order = ['CTL', 'asyn']

# Final Histo end of January
df_phase1_histo=df_phase1_unique[(~df_phase1_unique['Mouse'].isin(['J1', 'K1', 'V1', 'W2', 'X4', 'AB1', 'AE7', 'AH4', 'AI8', 'AK1', 'AK4', 'AM22', 'AP0', 'AQ6', 'AD1', 'AG3', 'AK22', 'AO6', 'AP4', 'AY31']))] #filter based on histo 10/09

fig, ax = plt.subplots(figsize=(4, 5))

sns.boxplot(data=df_phase1_histo, x="Condition", y="AvgLatency", order=order, width=0.3, palette=palette, ax=ax)
sns.stripplot(data=df_phase1_histo, x="Condition", y="AvgLatency", color='black', size=10, order=order, ax=ax)

ax.set_title("Average Latency to Retrieve Reward - 8 weeks")
ax.set_ylim(0, 60)

plt.tight_layout()

# Show first, then save
plt.show()
fig.savefig("MotivationTest_ReactionTime_Phase1_8weeks-sansAZ.pdf", dpi=300, format="pdf", bbox_inches='tight')


#%% Phase 5

os.chdir(r"C:\Users\beren\.spyder-py3\berenice")
#df_cog5 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\ASAP_Cog_behavior_Phase5-1and2_BC-XZ.xlsx")
df_cog5 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Sorted_ASAP_Cog_behavior_Phase5-1and2_BC-XZ.xlsx")
df_cog5 = pd.read_excel(r"C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Test_Sorted.xlsx")

s_cog51=df_cog5[(df_cog5['Phase']=='Phase5.1') & (df_cog5['Time']=='3weeks')]

s_cog51=s_cog51[(s_cog51['Day']<7)]

palette={"CTL":"#000000", "asyn":"#E42217"}# Red and black

# Nb of rewarded trials
# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
# Create point plot
sns.pointplot(
    data=s_cog51, 
    x="Day", 
    y="Rewarded_trials_Nb", 
    hue="Condition", 
    markers='o', 
    errorbar="se", 
    scale=2.5, 
    color='white', 
    palette=palette,
    ax=ax  # Use ax for explicit figure control
)
# Set axis limits and ticks
ax.set_ylim(0, 100)
ax.set_yticks([0, 25, 50, 75, 100])
# Adjust tick labels
ax.tick_params(axis='x', length=10, labelsize=25)
ax.tick_params(axis='y', length=10, labelsize=25)
# Set axis labels
ax.set_xlabel("Days", fontsize=25)
ax.set_ylabel("Rewarded Trial Number", fontsize=25)
# Set title
ax.set_title("Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch", fontsize=30)
# Optimize layout
plt.tight_layout()
# Save the figure in different formats
fig.savefig("Phase51_80-0_RewardedTrials.png", dpi=200, format="png", bbox_inches='tight')
fig.savefig("Phase51_80-0_RewardedTrials.pdf", dpi=200, format="pdf", bbox_inches='tight')
# Show the plot
plt.show()
# Close the figure to free memory
plt.close(fig)



## Nb of switch
# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
# Create point plot
sns.pointplot(data=s_cog51, x="Day", y="Nb_switch", hue="Condition", markers='o', errorbar="se", scale=2.5, color='white', palette=palette,ax=ax)  # Use ax for explicit figure control
# Set axis limits
ax.set_ylim(0, 5)
# Adjust tick labels
ax.tick_params(axis='x', length=10, labelsize=25)
ax.tick_params(axis='y', length=10, labelsize=25)
# Set axis labels
ax.set_xlabel("Days", fontsize=25)
ax.set_ylabel("Number of Switches", fontsize=25)
# Set title
ax.set_title("Phase 5.1 _ 80/0 - 80/0 Random 7-23 Nb Switch", fontsize=30)
# Optimize layout
plt.tight_layout()
# Save the figure as PDF
fig.savefig("Phase51_80-0_NbSwitch.png", dpi=200, format="png", bbox_inches='tight')
fig.savefig("Phase51_80-0_NbSwitch.pdf", dpi=200, format="pdf", bbox_inches='tight')
# Show the plot
plt.show()
# Close the figure to free memory
plt.close(fig)



## Side Omissions
fig, ax = plt.subplots(figsize=(8, 6))
# Create point plot
sns.pointplot(data=s_cog51, x="Day", y="Side_omission", hue="Condition", markers='o', errorbar="se", scale=2.5, color='white', palette=palette,ax=ax)  # Use ax for explicit figure control
# Set axis limits
ax.set_ylim(0, 40)
# Adjust tick labels
ax.tick_params(axis='x', length=10, labelsize=25)
ax.tick_params(axis='y', length=10, labelsize=25)
# Set axis labels
ax.set_xlabel("Days", fontsize=25)
ax.set_ylabel("Side omissions", fontsize=25)
# Set title
ax.set_title("Phase 5.1 _ 80/0 - 80/0 Random 7-23 Side omissions", fontsize=30)
# Optimize layout
plt.tight_layout()
# Save the figure as PDF
fig.savefig("Phase51_80-0_Side omissions.png", dpi=200, format="png", bbox_inches='tight')
fig.savefig("Phase51_80-0_Side omissions.pdf", dpi=200, format="pdf", bbox_inches='tight')
# Show the plot
plt.show()
# Close the figure to free memory
plt.close(fig)


## Center Omissions
fig, ax = plt.subplots(figsize=(8, 6))
# Create point plot
sns.pointplot(data=s_cog51, x="Day", y="C_omission", hue="Condition", markers='o', errorbar="se", scale=2.5, color='white', palette=palette,ax=ax)  # Use ax for explicit figure control
# Set axis limits
ax.set_ylim(0, 150)
# Adjust tick labels
ax.tick_params(axis='x', length=10, labelsize=25)
ax.tick_params(axis='y', length=10, labelsize=25)
# Set axis labels
ax.set_xlabel("Days", fontsize=25)
ax.set_ylabel("Center omissions", fontsize=25)
# Set title
ax.set_title("Phase 5.1 _ 80/0 - 80/0 Random 7-23 Center omissions", fontsize=30)
# Optimize layout
plt.tight_layout()
# Save the figure as PDF
fig.savefig("Phase51_80-0_ Center omissions.png", dpi=200, format="png", bbox_inches='tight')
fig.savefig("Phase51_80-0_ Center omissions.pdf", dpi=200, format="pdf", bbox_inches='tight')
# Show the plot
plt.show()
# Close the figure to free memory
plt.close(fig)


#### Individual Mouse - CTL 

sns.pointplot(data = s_cog51[(s_cog51['Condition']=='CTL')], x = "Day", y = "Rewarded_trials_Nb", hue = "Mouse", errorbar = "se").set(title='Phase 5.1 _ 3weeks _ CTL, individual mouse')
plt.show()

# Get unique mice in CTL condition
mouse_list = s_cog51[s_cog51['Condition'] == 'CTL']['Mouse'].unique()

for m in mouse_list:
    # Filter data for the individual mouse
    mouse_data = s_cog51[s_cog51['Mouse'] == m]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create point plot
    sns.pointplot(data=mouse_data, x="Day", y="Rewarded_trials_Nb", errorbar="se", ax=ax)

    # Set title with mouse ID
    ax.set_title(f'Phase 5.1 _ 3weeks _ CTL, Mouse {m}')

    # Show the plot (optional)
    plt.show()
    
    plt.tight_layout()
    
    # Save with unique filename
    filename = f"Phase5.1_3weeks_CTL_Mouse_{m}.pdf"
    fig.savefig(filename, dpi=300, format="pdf", bbox_inches='tight')



    # Close the figure to free memory
    #plt.close(fig)


#### Individual Mouse - asyn 

sns.pointplot(data = s_cog51[(s_cog51['Condition']=='asyn')], x = "Day", y = "Rewarded_trials_Nb", hue = "Mouse", errorbar = "se").set(title='Phase 5.1 _ 3weeks _ asyn, individual mouse')
plt.show()

# Get unique mice in asyn condition
mouse_list = s_cog51[s_cog51['Condition'] == 'asyn']['Mouse'].unique()

for m in mouse_list:
    # Filter data for the individual mouse
    mouse_data = s_cog51[s_cog51['Mouse'] == m]

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create point plot
    sns.pointplot(data=mouse_data, x="Day", y="Rewarded_trials_Nb", errorbar="se", ax=ax)

    # Set title with mouse ID
    ax.set_title(f'Phase 5.1 _ 3weeks _ asyn, Mouse {m}')

    plt.tight_layout()

    # Save with unique filename
    filename = f"Phase5.1_3weeks_asyn_Mouse_{m}.pdf"
    #fig.savefig(filename, dpi=300, format="pdf", bbox_inches='tight')
    fig.savefig(filename, dpi=300, format="png", bbox_inches='tight')

    # Show the plot (optional)
    plt.show()

    # Close the figure to free memory
    plt.close(fig)






# Number of trials before switch
df = pd.DataFrame()

def convert_to_list(value):
    if isinstance(value, int):  # If already an integer, wrap it in a list
        return [value]
    elif isinstance(value, str):  # If string, split and convert
        return [int(i) for i in value.split(',')]
    return []  # Handle unexpected cases

df= s_cog51[["Mouse", "Condition", "Sexe", "Phase", "Time", "Day", "Trial_nb_bf_switch"]]

df['Trial_nb_bf_switch'] = df['Trial_nb_bf_switch'].apply(convert_to_list)
# Compute row-wise mean
df['Mean_Trial_nb_bf_switch'] = df['Trial_nb_bf_switch'].apply(lambda x: sum(x) / len(x) if len(x) > 0 else None)

df=df[(df['Phase']=='Phase5.1') & (df_cog5['Time']=='3weeks')]

## Mean_Trial_nb_bf_switch
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = df, x = "Day", y = "Mean_Trial_nb_bf_switch", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=120)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Number of trials before switch", size = 25)
plt.title(label= 'Phase 5.1 _ 80/0 - Nb of trials before switch', fontsize=30)
plt.show()

#%% Phase 5.2 

s_cog52=df_cog5[(df_cog5['Phase']=='Phase5.2') & (df_cog5['Time']=='3weeks')]
s_cog52=s_cog52[(s_cog52['Day']<4)]

## Nb of switch
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = s_cog52, x = "Day", y = "Rewarded_trials_Nb", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=120)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Rewarded_trials_Nb", size = 25)
plt.title(label= 'Phase 5.1 _ 80/0 - Rewarded_trials_Nb', fontsize=30)
plt.show()

## Nb of switch
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = s_cog52, x = "Day", y = "Nb_switch", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=6)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Number of switches", size = 25)
plt.title(label= 'Phase 5.2 _ 80/20 - Number of switches', fontsize=30)
plt.show()




#%% Leaners vs Non leaners 

learner_cog52 = pd.read_excel(r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\LEARNERS_Sorted_ASAP_Cog_behavior_Phase5-1and2_BC-XZ.xlsx')

## Nb of rewarded trials
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = learner_cog52, x = "Day", y = "Rewarded_trials_Nb", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=75, ymax=150)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Nb of rewarded trials", size = 25)
plt.title(label= 'Phase 5.2 _ 80/20 - Number of rewarded trials - Learners', fontsize=30)
plt.show()


## Nb of switches
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = learner_cog52, x = "Day", y = "Nb_switch", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=6)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Number of switches", size = 25)
plt.title(label= 'Phase 5.2 _ 80/20 - Number of switches - Learners', fontsize=30)
plt.show()


nonlearner_cog52 = pd.read_excel(r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\NON-LEARNERS_Sorted_ASAP_Cog_behavior_Phase5-1and2_BC-XZ.xlsx')

## Nb of rewarded trials
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = nonlearner_cog52, x = "Day", y = "Rewarded_trials_Nb", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=150)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Nb of rewarded trials", size = 25)
plt.title(label= 'Phase 5.2 _ 80/20 - Number of rewarded trials - Non learners ', fontsize=30)
plt.show()


## Nb of switches
plt.figure(figsize=(8, 6))
ax = sns.pointplot(data = nonlearner_cog52, x = "Day", y = "Nb_switch", hue = "Condition", markers='o', errorbar = "se", scale=2.5, color='white', palette=palette)
plt.ylim(ymin=0, ymax=6)
plt.tick_params(axis='x', length=10, labelsize=25)  # Adjust x-axis label size
plt.tick_params(axis='y', length=10, labelsize=25)  # Adjust y-axis label size
plt.xlabel("Days", size = 25)
plt.ylabel("Number of switches", size = 25)
plt.title(label= 'Phase 5.2 _ 80/20 - Number of switches - Non learners ', fontsize=30)
plt.show()





#%% NO OFFICIAL CODE

LvsNL = pd.read_excel(r'C:\Users\beren\.spyder-py3\berenice\Data_Reversal_learning\Nb-Days_LearnerVSNon-learners.xlsx')
# Nb of days to learn
s_LvsNL=LvsNL[(~LvsNL['Mouse'].isin(['J1', 'K1', 'V1', 'X4', 'W2', 'AB1', 'AE7', 'AG3', 'AD1',  
                                        'AH4', 'AI8', 'I0', 'L4', 'I5', 'U3', 'Y0',
                                        'AE7', 'AF5', 'AK1', 'AK22', 'AN41', 'AO01', 'AO3', 'AQ12', 
                                        'AQ3', 'AQ10', 'AQ51', 'AR6', 'AA2', 'AN0', 'AN41', 'AB0', 'AB1', 
                                        'AC3', 'AD1', 'AE7', 'E5.2' ]))] 

plt.figure(figsize=(6, 6))
sns.boxplot(data=s_LvsNL, x = 'Condition', y = 'Nb_Day', width=0.3).set(title='Nb of days to reach Phase5.2')
sns.stripplot(data=s_LvsNL, x = 'Condition', y = 'Nb_Day', size= 10, color='grey')
plt.ylim(ymin=0)
plt.show()


## Nb of switch
#plt.figure(figsize=(6, 6))
sns.pointplot(data = s_LvsNL, x = "Day", y = "Nb_switch", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.2 _ 80/20 - 80% Rewarded trials in last 15 to switch')
plt.ylim(ymax=5)
plt.show()


## Rewarded Pct
sns.pointplot(data = s_cog51, x = "Day", y = "Rewarded_trials_Pct", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch- Rewarded_trials_Pct')
plt.show()

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='M')], x = "Day", y = "Rewarded_trials_Pct", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Rewarded_trials_Pct - Males')

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='F')], x = "Day", y = "Rewarded_trials_Pct", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Rewarded_trials_Pct - Females')

## Side Omissions
sns.pointplot(data = s_cog51, x = "Day", y = "Side_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch- Side_omission')
plt.show()

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='M')], x = "Day", y = "Side_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Side_omission - Males')

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='F')], x = "Day", y = "Side_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Side_omission - Females')

## Center omissions
sns.pointplot(data = s_cog51, x = "Day", y = "C_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch- Center_omission')
plt.show()

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='M')], x = "Day", y = "C_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - C_omission - Males')

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='F')], x = "Day", y = "C_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - C_omission - Females')



## Total omissions
s_cog51['TOT_omissions'] = s_cog51['C_omission'] + s_cog51['Side_omission']

sns.pointplot(data = s_cog51, x = "Day", y = "TOT_omissions", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch- TOT_omissions')
plt.show()

sns.pointplot(data = s_cog51, x = "Day", y = "C_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Center Omissions')
sns.pointplot(data = s_cog51, x = "Day", y = "Side_omission", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - Side Omissions')

sns.pointplot(data = s_cog51[(s_cog51['Sexe']=='F')], x = "Day", y = "TOT_omissions", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch - TOT_omissions - Females')


# Pointplot - Rewarded_trials_Pct
sns.pointplot(data = s_cog51, x = "Day", y = "Rewarded_trials_Nb", hue = "Condition", palette=palette, errorbar = "se").set(title='Phase 5.1 _ 80/0 - 80/0 Random 7-23 Rew trials to switch')
plt.show()


#Each Mouse - asyn
sns.pointplot(data = s_cog51[(s_cog51['Condition']=='asyn')], x = "Day", y = "Rewarded_trials_Nb", hue = "Mouse", errorbar = "se").set(title='Phase 5.1 80/0 _ 3weeks _ asyn')
plt.show()

#Each Mouse - CTL
sns.pointplot(data = s_cog51[(s_cog51['Condition']=='CTL')], x = "Day", y = "Rewarded_trials_Nb", hue = "Mouse", errorbar = "se").set(title='Phase 5.1 80/0 _ 3weeks _ CTL')
plt.show()


## Sexe 

#Intragroup
sns.pointplot(data = s_cog51[(s_cog51['Condition']=='asyn')], x = "Day", y = "Rewarded_trials_Nb", hue = "Sexe", errorbar = "se", palette=palette).set(title='Phase 5.1 80/0 _ 3weeks _ CTL')
plt.show()






