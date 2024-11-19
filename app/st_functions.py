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

	dim_title = dimension.replace('_', ' ').title()

	grouped = df.groupby(['cluster', dimension], observed=True)[[metric, 'id']].agg({metric: 'mean', 'id': 'count'}).round(0).reset_index()
	size = grouped['id'].tolist()

	metric_mean = grouped[metric].mean()

	fig = go.Figure(data=[go.Scatter()])

	for cluster, cluster_data in grouped.groupby('cluster'):
		fig.add_trace(go.Scatter(
			x=cluster_data[dimension].tolist(),
			y=cluster_data[metric].tolist(),
			mode='markers',
			marker=dict(
				size=size,
				sizemode='area',
				sizeref=2.*max(size)/(60.**2),
				sizemin=4,
				#color=grouped[cluster]#.unique()
			),
			name=f"Cluster {cluster}"
			)
		)

	fig.update_layout(
		title=dict(
			text=f"Spending Score and {dim_title}",
			x=0,
			y=1,
			xanchor='left',
			yanchor='top'
		),
		showlegend=True,
		legend=dict(
			orientation='h',
			x=0,
			y=-.2
		)
	)

	fig.add_annotation(
		xref='paper',
		yref='paper',
		xanchor='left',
		yanchor='top',
		x=-0.03,
		y=1.2,
		text="* The bubble size indicates the size of each group.",
		showarrow=False,
		align='left'
	)

	fig.update_yaxes(
		range=[30, 70]
	)

	fig.add_hline(
		y=metric_mean,
		line_dash='dot',
		line_color='white',
		label=dict(
			text='Mean',
			textposition='start',
			font=dict(
				color='white'
			)
		)
	)

	return fig


def relative_percentage_difference(a, b):
    """Calculate the percentage difference relative to the first value."""
    if a == 0:  # Avoid division by zero
        raise ValueError("The first value cannot be zero.")
    return int((a - b) / (a) * 100)