#Python Script for Biblical Baby Names Project
#Danielle Hill
#danie11e.com
#2015

#Import pandas and numpy and os
import pandas as pd
import numpy as np
import os


#1. Create a list of state abbreviations using file names
files = os.listdir('data/state_names/.')
states = []

for file in files:
	#grap first two letters and append to states array
	states.append(file[:2])


#2. Create DataFrame by concatenating individual state files
pieces = []
columns = ['state', 'gender', 'year', 'name', 'births']

for state in states:
	path = 'data/state_names/%s.txt' % state
	frame = pd.read_csv(path, names=columns) 

	pieces.append(frame)

df = pd.concat(pieces, ignore_index=True)

#3. Add T|F indicator to biblical list
biblical = pd.read_excel('data/biblicalnames.xlsx', 'biblicalnames', index_col=None, na_values=['NA'])
biblical['biblical'] = 'true'


#4. Merge biblical name list to names to show T|F for all names using left join
names = pd.merge(df, biblical, how='left')
#fill in na with false
names['biblical'].fillna('false', inplace=True)


#5. Create a pivot tables, rename columns, add column for % and calculate %

######  Define functions  #####

#Function to rename columns
def rename_columns(table):
	table.columns = ['false', 'true', 'total']

#Function to add column and calculate %
def add_percent(table):
	table['%'] = (table['true'] / (table['true']+table['false'])) * 100

######  End define functions  #####

#5A Pivot table summarizing the names by year and state
year_gender_summary = pd.pivot_table(names, values='births', index=['year', 'state', 'gender'],columns=['biblical'], aggfunc=np.sum, margins=True)
rename_columns(year_gender_summary)
add_percent(year_gender_summary)

#5B Pivot table calculating % biblical names by state for all years
state_summary = pd.pivot_table(names, values='births', index='state', columns=['biblical'], aggfunc=np.sum, margins=True)
rename_columns(state_summary)
add_percent(state_summary)

#6. Store table and names as csv	for visualization with d3.js and/or Tableau
#year_gender_summary.to_csv('bbnames_summary.csv')
#state_summary.to_csv('state_summary.csv')
#names.to_csv('bbnames_raw.csv')

#Plan for pivot for gender summary:
#table = pd.pivot_table(names, values='births', index=['state', 'gender'], columns='biblical', aggfunc=np.sum)
#add_percent(table)
#table2 = table.drop(['false', 'true'], 1)