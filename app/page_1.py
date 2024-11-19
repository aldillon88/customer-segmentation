import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import sys
import os

# Add the project root to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
	sys.path.append(project_root)

from st_functions import *

df = load_data("../data/clean/clustered.csv") # for local development
#df = load_data("/data/clean/clustered.csv")

# Create population averages for comparison metrics.
pop_total = len(df)
pop_mean_age = df['age'].mean().astype('int')
pop_mean_income = df['income'].mean().astype('int')
pop_mean_spending_score = df['spending_score'].mean().astype('int')
pop_mean_purchase_freq = df['purchase_frequency'].mean().astype('int')
pop_mean_membership = df['membership_years'].mean().astype('int')

clusters = df['cluster'].unique().tolist()
clusters.insert(0, 'All clusters')
dimensions = df.select_dtypes('object').columns.to_list()
dimensions.pop(dimensions.index('spending_score_category'))
dimensions = [dim.replace('_', ' ').title() for dim in dimensions]

with st.sidebar:
	st.subheader('Filters', divider=True)
	cluster = st.selectbox('Cluster', clusters)
	dimension = st.selectbox('Dimension', dimensions).replace(' ', '_').lower()

if cluster != 'All clusters':
	df = df[df['cluster'] == cluster]

# Calculate metrics
total = len(df)
mean_age = df['age'].mean().astype('int')
mean_income = df['income'].mean().astype('int')
mean_spending_score = df['spending_score'].mean().astype('int')
mean_purchase_freq = df['purchase_frequency'].mean().astype('int')
mean_membership = df['membership_years'].mean().astype('int')

# Create a list of metrics
metrics = [
	('Total Customers', total, pop_total),
	('Mean Age', mean_age, pop_mean_age),
	('Mean Income', mean_income, pop_mean_income),
	('Mean Spending Score', mean_spending_score, pop_mean_spending_score),
	('Mean Purchase Frequency', mean_purchase_freq, pop_mean_purchase_freq),
	('Mean Membership Tenure', mean_membership, pop_mean_membership)
]

# Calculate difference from population

r1_cols = st.columns(6)

for col, (metric, val, pop_val) in zip(r1_cols, metrics):
	if cluster != 'All clusters':
		with col:
			with st.container(border=True):
				if metric == 'Total Customers':
					diff = f"{int(val / pop_val * 100)}% of all customers"
					st.metric(metric, val, diff, delta_color='off')
				else:
					diff = f"{relative_percentage_difference(val, pop_val)}% vs. global mean"
					st.metric(metric, val, diff)
	else:
		with col:
			with st.container(border=True):
				st.metric(metric, val)


row1col1, row1col2 = st.columns(2)

with row1col1:
	with st.container(border=True):
		bubble = plot_bubble(df, dimension, 'spending_score')
		st.plotly_chart(bubble)

with row1col2:
	with st.container(border=True):
		sunburst = plot_sunburst(df, 'cluster', dimension)
		st.plotly_chart(sunburst)

dims = [dim.replace('_', ' ').title() for dim in dimensions]
st.text(dims)
dims_lower = [dim.replace(' ', '_').lower() for dim in dims]
st.text(dims_lower)