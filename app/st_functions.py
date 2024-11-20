import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


@st.cache_data
def load_data(path):
	df = pd.read_csv(path)
	return df


def relative_percentage_difference(a, b):
    """Calculate the percentage difference relative to the first value."""
    if a == 0:  # Avoid division by zero
        raise ValueError("The first value cannot be zero.")
    return int((a - b) / (a) * 100)

@st.cache_data
def plot_bar(df, dimension, colors):

	dim_title = dimension.replace('_', ' ').title()

	data = df.groupby(['cluster', dimension]).size().reset_index(name='count')
	clusters = data['cluster'].unique().tolist()

	fig = make_subplots(
		rows=len(clusters),
		cols=1,
		shared_xaxes=True,
		vertical_spacing=0.03
	)

	fig.update_layout(
		title=dict(
			text=f"Count per {dim_title}",
			x=0,
			y=1,
			xanchor='left',
			yanchor='top'
		),
		showlegend=True,
		legend=dict(
			x=1,
			y=1
		),
		margin=dict(
			l=0,
			r=0,
			t=50,
			b=0
		)
)

	for i, (cluster, color) in enumerate(zip(clusters, colors)):

		cat_df = data[data['cluster'] == cluster].sort_values(by='count')

		fig.add_trace(go.Bar(
			x=cat_df['count'],
			y=cat_df[dimension],
			orientation='h',
			name=f"Segment {cluster}",
			text=cat_df['count'],
			textfont=dict(color='white'),
			textposition='outside',
			marker=dict(color=f"{color}")
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

		fig.update_xaxes(
			showticklabels=False
		)

	return fig

@st.cache_data
def plot_bubble(df, dimension, metric, colors):

	met_title = metric.replace('_', ' ').title()

	data = df.groupby(['cluster', dimension], observed=True)[[metric, 'id']].agg({metric: 'mean', 'id': 'count'}).round(0).reset_index()
	clusters = data['cluster'].unique()

	fig = make_subplots(
		rows=len(clusters),
		cols=1,
		shared_xaxes=True,
		vertical_spacing=0.03
	)

	fig.update_layout(
		title=dict(
			text=met_title,
			x=0,
			y=1,
			xanchor='left',
			yanchor='top'
		),
		showlegend=True,
		legend=dict(
			#orientation='h',
			x=1,
			y=1
		),
		margin=dict(
			l=0,
			r=0,
			t=50,
			b=0
		)
)

	for i, (cluster, color) in enumerate(zip(clusters, colors)):

		cat_df = data[data['cluster'] == cluster].sort_values(by=metric)

		fig.add_trace(go.Scatter(
			x=cat_df[metric].tolist(),
			y=cat_df[dimension].tolist(),
			mode='markers+text',
			marker=dict(color=color),
			text=cat_df[metric], ######
			textfont=dict(color='white'),
			textposition='middle right',
			name=f"Segment {cluster}"
			),
			row=i+1,
			col=1)

		# Add line traces for each point
		for j in range(len(cat_df)):
			fig.add_trace(go.Scatter(
				x=[0, cat_df[metric].iloc[j]],  # Line from 0 to the x value
				y=[cat_df[dimension].iloc[j], cat_df[dimension].iloc[j]],  # Same y-value
				mode='lines',
				line=dict(color=color, width=2),  # Adjust line properties
				showlegend=False  # Avoid duplicate legend entries
			),
				row=i+1,
				col=1
			)		
		
		fig.update_yaxes(
			showline=True,
			linecolor='lightgrey',
			linewidth=1,
			ticklabelposition='outside',
			ticklen=7,
			tickcolor='white',
			row=i+1,
			col=1,
			showgrid=False
		)

		fig.update_xaxes(
			showticklabels=False
		)

		fig.update_traces(marker_size=15)

	return fig

