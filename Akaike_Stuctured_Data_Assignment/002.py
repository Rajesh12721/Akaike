# -*- coding: utf-8 -*-
"""002.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14sCMT0XPcItDyBbYLMLn_Y9SXD5XXQbq

# **Problem 2**
 Drugs are generally administered/prescribed by the physicians for a certain period of time or they are administered at regular intervals, but for various reasons patients might stop taking the treatment . Consider following example for better understanding Let’s say you get a throat infection, the physician prescribes you an antibiotic for 10 days, but you stop taking the treatment after 3 days because of some adverse events.
In the above example ideal treatment duration is 10 days but patients stopped taking treatment after 3 days due to adverse events. Patients stopping a treatment is called dropoff. We want to study dropoff for “Target Drug”, the aim is to generate insights on what events lead to patients stopping on “Target Drug”. Assume ideal treatment duration for “Target Drug” is 1 year, come up with analysis showing how drop-off rate is, dropoff rate is defined as number of patients dropping off each month.
Then come up with analysis to generate insights on what events are driving a patient to stop taking “Target Drug”.

import libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Reading train data"""

train_df=pd.read_parquet("/content/sample_data/train.parquet")

"""Taking users who are all taking target drug"""

target_data = train_df[train_df['Incident'] == 'TARGET DRUG']

"""Calculate dropoff rate by month"""

target_data['Date'] = pd.to_datetime(target_data['Date'])
target_data['Month'] = target_data['Date'].dt.month
dropoff_rates = target_data.groupby('Month')['Patient-Uid'].nunique().diff().fillna(0)

"""To visualize the drop off rate over time"""

plt.figure(figsize = (8, 4))
dropoff_rates.plot(kind='bar', color = "green")
plt.xlabel('Month')
plt.ylabel('Drop-off Count')
plt.title('Drop-off Rate of Target Drug')
plt.show()

"""To analyze events driving dropp-off"""

dropoff_reasons = train_df[train_df['Patient-Uid'].isin(target_data['Patient-Uid'])]
dropoff_reasons = dropoff_reasons[dropoff_reasons['Date'] < dropoff_reasons.groupby('Patient-Uid')['Date'].transform('max')]
dropoff_reasons = dropoff_reasons[dropoff_reasons['Incident'] != 'TARGET DRUG']

"""To calculate the frequency of each event leading to drop-off"""

event_freq = dropoff_reasons['Incident'].value_counts()

"""Plot the events leading to drop-off"""

plt.figure(figsize=(8, 4))
event_freq.plot(kind='bar', color="green")
plt.xlabel('Event')
plt.ylabel('Frequency')
plt.title('Events Leading to Drop-off of Target Drug')
plt.show()