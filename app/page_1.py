import streamlit as st

import sys
import os

# Add the project root to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
	sys.path.append(project_root)

from st_functions import *

data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean', 'clustered.csv'))

#df = load_data("../data/clean/clustered.csv") # for local development
df = load_data(data_path) # In the Docker build this is /app/data/clean/clustered.csv

# Create population averages for comparison metrics.
pop_total = len(df)
pop_mean_age = df['age'].mean().astype('int')
pop_mean_income = df['income'].mean().astype('int')
pop_mean_spending_score = df['spending_score'].mean().astype('int')
pop_mean_purchase_freq = df['purchase_frequency'].mean().astype('int')
pop_mean_membership = df['membership_years'].mean().astype('int')

clusters = df['cluster'].sort_values().unique().tolist()
clusters.insert(0, 'All Segments')
cluster_colors = [None, '#83C9FF', '#2568C9', '#F9ABAB']
dimensions = df.select_dtypes('object').columns.sort_values().to_list()
dimensions.pop(dimensions.index('spending_score_category'))
dimensions.pop(dimensions.index('purchase_frequency_category'))
dimensions = [dim.replace('_', ' ').title() for dim in dimensions]

with st.sidebar:
	st.subheader('Filters', divider=True)
	cluster = st.selectbox('Customer Segment', clusters)
	dimension = st.selectbox('Dimension', dimensions).replace(' ', '_').lower()

if cluster != 'All Segments':
	df = df[df['cluster'] == cluster]
	col_index = clusters.index(cluster)
	color = [cluster_colors[col_index]]
else:
	color = cluster_colors[1:]

# Calculate metrics
total = len(df)
mean_age = df['age'].mean().astype('int')
mean_income = df['income'].mean().astype('int')
mean_spending_score = df['spending_score'].mean().astype('int')
mean_purchase_freq = df['purchase_frequency'].mean().astype('int')
mean_membership = df['membership_years'].mean().astype('int')

# Create a list of metrics (tuples)
metrics = [
	('Total Customers', total, pop_total),
	('Mean Age', mean_age, pop_mean_age),
	('Mean Income', mean_income, pop_mean_income),
	('Mean Spending Score', mean_spending_score, pop_mean_spending_score),
	('Mean Purchase Frequency', mean_purchase_freq, pop_mean_purchase_freq),
	('Mean Membership Tenure', mean_membership, pop_mean_membership)
]

r1_cols = st.columns(6)

for col, (metric, val, pop_val) in zip(r1_cols, metrics):
	if cluster != 'All Segments':
		with col:
			with st.container(border=True):
				if metric == 'Total Customers':
					diff = f"{int(val / pop_val * 100)}% of all customers"
					st.metric(metric, f"{val:,}", diff, delta_color='off')
				else:
					diff = f"{relative_percentage_difference(val, pop_val)}% vs. global mean"
					st.metric(metric, f"{val:,}", diff)
	else:
		with col:
			with st.container(border=True):
				st.metric(metric, f"{val:,}")


c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:
	with st.container(border=True):
		bar1 = plot_bar(df, dimension, color)
		st.plotly_chart(bar1)

with c2:
	with st.container(border=True):
		bubble1 = plot_bubble(df, dimension, 'spending_score', color)
		st.plotly_chart(bubble1)

with c3:
	with st.container(border=True):
		bubble2 = plot_bubble(df, dimension, 'purchase_frequency', color)
		st.plotly_chart(bubble2)

with c4:
	with st.container(border=True):
		bubble3 = plot_bubble(df, dimension, 'last_purchase_amount', color)
		st.plotly_chart(bubble3)