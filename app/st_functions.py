import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


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


def plot_bar(df, dimension):

	dim_title = dimension.replace('_', ' ').title()

	data = df.groupby(['cluster', dimension]).size().reset_index(name='count')
	clusters = data['cluster'].unique()

	fig = make_subplots(
		rows=len(clusters),
		cols=1,
		shared_xaxes=True,
		vertical_spacing=0.1
	)

	fig.update_layout(
	title=dict(
		text=f"Count per {dim_title}",
		x=0,
		y=1,
		xanchor='left',
		yanchor='top'
	),
	showlegend=False,
	legend=dict(
		orientation='h',
		x=0,
		y=-.2
	),
	margin=dict(
		l=120,
		r=0,
		t=60,
		b=0
	)
)

	for i, cluster in enumerate(clusters):

		cat_df = data[data['cluster'] == cluster].sort_values(by='count')

		fig.add_trace(go.Bar(
			x=cat_df['count'],
			y=cat_df[dimension],
			orientation='h',
			name=f"Cluster {cluster}",
			text=cat_df['count'],
			textfont=dict(color='white')
		),
		row=i+1,
		col=1)
		
		fig.update_yaxes(
			showline=True,
			linecolor='lightgrey',
			linewidth=1,
			ticklabelposition='outside',
			ticklen=7,
			tickcolor='white',
			row=i+1,
			col=1
		)

		fig.add_annotation(
			xref='paper',
			yref='y' + str(i + 1),
			#xanchor='right',
			x=-0.50,
			y=cat_df[dimension].iloc[len(cat_df) // 2],
			text=f"S.{cluster}",
			showarrow=False,
			font=dict(size=20),
			align='left'
		)

	return fig


def test(df, dimension, metric):

	#dim_title = dimension.replace('_', ' ').title()
	met_title = metric.replace('_', ' ').title()

	data = df.groupby(['cluster', dimension], observed=True)[[metric, 'id']].agg({metric: 'mean', 'id': 'count'}).round(0).reset_index()
	clusters = data['cluster'].unique()
	size = data['id'].tolist()
	metric_mean = data[metric].mean()

	fig = make_subplots(
		rows=len(clusters),
		cols=1,
		shared_xaxes=True,
		vertical_spacing=0.1
	)

	fig.update_layout(
	title=dict(
		text=met_title,
		x=0,
		y=1,
		xanchor='left',
		yanchor='top'
	),
	showlegend=False,
	#legend=dict(
	#	orientation='h',
	#	x=0,
	#	y=-.2
	#),
	margin=dict(
		l=0,
		r=0,
		t=60,
		b=0
	)
)

	for i, cluster in enumerate(clusters):

		cat_df = data[data['cluster'] == cluster].sort_values(by=metric)

		fig.add_trace(go.Scatter(
			x=cat_df[metric].tolist(),
			y=cat_df[dimension].tolist(),
			mode='markers',
			#marker=dict(
				#size=size,
				#sizemode='area',
				#sizeref=2.*max(size)/(15.**2),
				#sizemin=50,
				#color=grouped[cluster]#.unique()
			#),
			name=f"Cluster {cluster}"
			),

			row=i+1,
			col=1)
		
		fig.update_yaxes(
			showline=True,
			linecolor='lightgrey',
			linewidth=1,
			ticklabelposition='outside',
			ticklen=7,
			tickcolor='white',
			row=i+1,
			col=1
		)

		fig.update_traces(marker_size=10)

	return fig