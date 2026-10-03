import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from abc import ABC, abstractmethod

class BaseVisualizer(ABC):
    def __init__(self, tab_id):
        self.tab_id = tab_id
        self.df = pd.DataFrame()
    
    def get_unique_key(self, base_key):
        """Generate a unique key for Streamlit elements"""
        return f"{base_key}_{self.tab_id}"
    
    def create_bar_chart(self, data, x, y, title, color=None, color_map=None, width=0.4, height=600, text=None):
        """Create a standardized bar chart"""
        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title,
            color=color,
            color_discrete_map=color_map,
            width=800
        )
        
        # Update traces with text and width settings
        fig.update_traces(
            width=width,
            textposition='outside'
        )
        
        # If text is provided, update the text values
        if text is not None:
            fig.update_traces(text=text)
        
        fig.update_layout(
            showlegend=bool(color),
            height=height,
            bargap=0.5
        )
        
        return fig
    
    def create_line_chart(self, data, x, y, title, mode='lines+markers', height=600):
        """Create a standardized line chart"""
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data[x],
                y=data[y],
                mode=mode,
                name=y
            )
        )
        
        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title=y,
            height=height
        )
        
        return fig
    
    def show_plotly_chart(self, fig, key_base):
        """Display a plotly chart with a unique key"""
        st.plotly_chart(fig, use_container_width=True, key=self.get_unique_key(key_base))
    
    def show_metrics(self, metrics):
        """Display metrics in columns"""
        cols = st.columns(len(metrics))
        for col, (label, value, delta) in zip(cols, metrics):
            with col:
                st.metric(label, value, delta)
    
    def show_dataframe(self, df, column_config, expanded=False):
        """Display a dataframe in an expander"""
        with st.expander("", expanded=expanded):
            st.dataframe(
                df,
                column_config=column_config,
                hide_index=True,
                use_container_width=True
            )
    
    @abstractmethod
    def get_data(self):
        """Fetch data for visualization"""
        pass
    
    @abstractmethod
    def show(self):
        """Display visualizations"""
        pass
