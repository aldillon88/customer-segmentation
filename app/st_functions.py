import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


@st.cache_data
def load_data(path):
	df = pd.read_csv(path)
	return df


def plot_sunburst(df, dim1, dim2):

	fig = px.sunburst(df, path = [dim1, dim2])

	fig.update_layout(
		title="Cluster and Income Level Sunburst",
		margin=dict(t=20, l=0, r=0, b=0)
	)

	return fig


def plot_bubble(df, dimension, metric):
	grouped = df.groupby(['cluster', dimension], observed=True)[[metric, 'id']].agg({metric: 'mean', 'id': 'count'}).round(0).reset_index()
	size = grouped['id'].tolist()
	
	fig = go.Figure(data=[go.Scatter(
		x=grouped[dimension].tolist(),
		y=grouped[metric].tolist(),
		mode='markers',
		marker=dict(
			size=size,
			sizemode='area',
			sizeref=2.*max(size)/(60.**2),
			sizemin=4,
			color=grouped['cluster']#.unique()
		)
	)])
	return fig

def test():
	size = [20, 40, 60, 80, 100, 80, 60, 40, 20, 40]
	fig = go.Figure(data=[go.Scatter(
		x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
		y=[11, 12, 10, 11, 12, 11, 12, 13, 12, 11],
		mode='markers',
		marker=dict(
			size=size,
			sizemode='area',
			sizeref=2.*max(size)/(40.**2),
			sizemin=4
		)
	)])

	return fig