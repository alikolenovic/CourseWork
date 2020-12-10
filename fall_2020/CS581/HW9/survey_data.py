# Author:  Ali Kolenovic

#  survey_data.py runs an analysis of data on Pew_Survey.csv

# To run from terminal window:   survey_data.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('Pew_Survey.csv')
tot_participants = df.size
# Create a dataframe of people who use instagram
insta = df.loc[df['web1b'] == 1]
# Percentage of Instagram users on survey.
print("Percentage of Instagram Users: %.2f" % (insta.size / tot_participants))
print("Total Instagram Users: ", insta.size)

# How often Instagram users are on the app.
several = insta.loc[insta['sns2b'] == '1']
once_day = insta.loc[insta['sns2b'] == '2']
few_times = insta.loc[insta['sns2b'] == '3']
few_weeks = insta.loc[insta['sns2b'] == '4']
less_often = insta.loc[insta['sns2b'] == '5']

groups = ['Several times a day', 'Once a day', 'Few times a week', 'Every few weeks', 'Less Often']
freq = [several.size, once_day.size, few_times.size, few_weeks.size, less_often.size]
print('------ Frequency of Users ------')
print('Frequency                 Total                Percentage')
print('Several times a day:       %i                    %.2f' % (several.size, freq[0] / insta.size))
print('Once a day:                %i                    %.2f' % (once_day.size, freq[1] / insta.size))
print('Few times a week:          %i                    %.2f' % (few_times.size, freq[2] / insta.size))
print('Every few weeks:           %i                    %.2f' % (few_weeks.size, freq[3] / insta.size))
print('Less often:                %i                    %.2f' % (less_often.size, freq[4] / insta.size))
# --- Create a bar graph of the frequency ---
plt.bar(groups, freq)
plt.xlabel("Frequency")
plt.ylabel("Amount of Users")
plt.title("Frequency of Instagram Users")
plt.show()
plt.clf()
# -------------------------------------------


# Political party based on time spent on the app
several_dem = several.loc[several['party'] == 1]
several_rep = several.loc[several['party'] == 2]
once_day_dem = once_day.loc[once_day['party'] == 1]
once_day_rep = once_day.loc[once_day['party'] == 2]
few_times_dem = few_times.loc[few_times['party'] == 1]
few_times_rep = few_times.loc[few_times['party'] == 2]
few_weeks_dem = few_weeks.loc[few_weeks['party'] == 1]
few_weeks_rep = few_weeks.loc[few_weeks['party'] == 2]
less_often_dem = less_often.loc[less_often['party'] == 1]
less_often_rep = less_often.loc[less_often['party'] == 2]

dem_count = (several_dem.size, once_day_dem.size, few_times_dem.size, few_weeks_dem.size, less_often_dem.size)
rep_count = (several_rep.size, once_day_rep.size, few_times_rep.size, few_weeks_rep.size, less_often_rep.size)
print('------ Political Party of User Based on Frequency (Recorded) ------')
print('Frequency                                  Total Dems            Total Reps')
print('Affiliation based on Several times a day:      %i                  %i' % (dem_count[0], rep_count[0]))
print('Affiliation based on Once a day:               %i                   %i' % (dem_count[1], rep_count[1]))
print('Affiliation based on Few times a week:         %i                   %i' % (dem_count[2], rep_count[2]))
print('Affiliation based on Every few weeks:          %i                   %i' % (dem_count[3], rep_count[3]))
print('Affiliation based on Less often:               %i                   %i' % (dem_count[4], rep_count[4]))
ind = np.arange(5)
p1 = plt.bar(ind, dem_count)
p2 = plt.bar(ind, rep_count, bottom=dem_count)
plt.xlabel("Frequency")
plt.ylabel('Amount of Users')
plt.title('Political Party of Instagram Users per Frequency')
plt.xticks(ind, ('Several times a day', 'Once a day', 'Few times a week', 'Every few weeks', 'Less Often'))
plt.legend((p1[0], p2[0]), ('Democrat', 'Republican'))
plt.show()

# Which region are Instagram users residing in
northeast = insta.loc[insta['cregion'] == 1]
midwest = insta.loc[insta['cregion'] == 2]
south = insta.loc[insta['cregion'] == 3]
west = insta.loc[insta['cregion'] == 4]

groups = ['Northeast', 'Midwest', 'South', 'West']
freq = [northeast.size, midwest.size, south.size, west.size]
print('------ Frequency of Users ------')
print('Region         Total                Percentage')
print('Northeast:      %i                    %.2f' % (northeast.size, freq[0] / insta.size))
print('Midwest:        %i                    %.2f' % (midwest.size, freq[1] / insta.size))
print('South:          %i                    %.2f' % (south.size, freq[2] / insta.size))
print('West:           %i                    %.2f' % (west.size, freq[3] / insta.size))

plt.bar(groups, freq)
plt.xlabel("Region")
plt.ylabel("Amount of Users")
plt.title("Instagram Users per Region")
plt.show()
plt.clf()

# Political Party of Instagram Users per Region
northeast_dem = northeast.loc[northeast['party'] == 1]
northeast_rep = northeast.loc[northeast['party'] == 2]
midwest_dem = midwest.loc[midwest['party'] == 1]
midwest_rep = midwest.loc[midwest['party'] == 2]
south_dem = south.loc[south['party'] == 1]
south_rep = south.loc[south['party'] == 2]
west_dem = west.loc[west['party'] == 1]
west_rep = west.loc[west['party'] == 2]

dem_count = (northeast_dem.size, midwest_dem.size, south_dem.size, west_dem.size)
rep_count = (northeast_rep.size, midwest_rep.size, south_rep.size, west_rep.size)
print('------ Political Party of User Based on Region (Recorded) ------')
print('Frequency                           Total Dems            Total Reps')
print('Affiliation based on Northeast:         %i                  %i' % (dem_count[0], rep_count[0]))
print('Affiliation based on Midwest:           %i                  %i' % (dem_count[1], rep_count[1]))
print('Affiliation based on South:             %i                 %i' % (dem_count[2], rep_count[2]))
print('Affiliation based on West:              %i                  %i' % (dem_count[3], rep_count[3]))
ind = np.arange(4)
p1 = plt.bar(ind, dem_count)
p2 = plt.bar(ind, rep_count, bottom=dem_count)
plt.xlabel("Region")
plt.ylabel('Amount of Users')
plt.title('Political Party of Instagram Users per Region')
plt.xticks(ind, ('Northeast', 'Midwest', 'South', 'West'))
plt.legend((p1[0], p2[0]), ('Democrat', 'Republican'))
plt.show()
