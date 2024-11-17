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