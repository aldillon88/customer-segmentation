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

#with st.container():
st.header("Overview")
st.markdown("""
	This dashboard aims to present useful distinctions between various customer segments. The segmentation was achieved through the use of Machine learning (ML), 
	specifically a popular unsupervised learning  technique called ***K-Means Clustering***. The K-Means algorithm takes in a prepared dataset and assigns a label (cluster)
	from 0 to n-1 to each sample, where 'n' is the number of clusters defined by the analyst. Each cluster represents a distinct customer segment.
	""")

st.divider()
st.header("Data Dictionary")
st.markdown("""
	- **:blue[Age]**: Age of the customer.
	- **:blue[Gender]**: Gender of the customer (Male, Female, Other).
	- **:blue[Income]**: Annual income of the customer (in USD).
	- **:blue[Spending Score]**: Spending score (1-100), indicating the customer's spending behavior and loyalty.
	- **:blue[Membership Tenure]**: Number of years the customer has been a member.
	- **:blue[Purchase Frequency]**: Number of purchases made by the customer in the last year.
	- **:blue[Preferred Category]**: Preferred shopping category (Electronics, Clothing, Groceries, Home & Garden, Sports).
	- **:blue[Last Purchase Amount]**: Amount spent by the customer on their last purchase (in USD).
	""")