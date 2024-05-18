import streamlit as st
import sys
from Networking.Networking import Networking
import pandas as pd
from ourData.cache import LocalCache
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

def app():
    st.title('ALL Patients')
    
    # Instantiate networking and cache objects
    Network = Networking()
    cacheInMemory = LocalCache()
    
    # Retrieve the dataframe
    df = cacheInMemory.get_assessment_byDocId_version2()
    
    # Display the dataframe in a read-only format
    st.write("Dataframe (read-only):")
    st.dataframe(df)  # or st.table(df) for a more static table

