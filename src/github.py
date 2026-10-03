import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from github import Github
from datetime import datetime
from .base_visualizer import BaseVisualizer

class GitHubVisualizer(BaseVisualizer):
    def __init__(self, tab_id):
        super().__init__(tab_id)
        try:
            self.token = st.secrets["TOKEN"]
            self.language_colors = {
                'Jupyter Notebook': '#008294',     # teal
                'JavaScript': '#4F4F4F', # dark gray
                'HTML': '#4F4F4F',       # light gray
                'CSS': '#E0E0E0',        # light gray
                'Not specified': '#E0E0E0'  # light gray
            }
        except Exception as e:
            st.error("GitHub token not found in Streamlit secrets. Please add it in the Streamlit Cloud settings.")
            self.token = None
    
    def get_data(self):
        try:
            # Initialize GitHub API with token
            g = Github(self.token)
            
            # Get user
            user = g.get_user()
            # user = "Muhammet-Abd-ElWahab"
            
            # Get repositories data
            repos_data = []
            for repo in user.get_repos():
                repos_data.append({
                    'Name': repo.name,
                    'Language': repo.language or 'Not specified',
                    'Stars': repo.stargazers_count,
                    'Forks': repo.forks_count,
                    'Created': repo.created_at,
                    'Last Updated': repo.updated_at,
                    'Description': repo.description or '',
                    'URL': repo.html_url,
                    'Is Fork': repo.fork
                })
            
            # Convert to DataFrame
            self.df = pd.DataFrame(repos_data)
            return self.df
        
        except Exception as e:
            st.error(f"Error accessing GitHub API: {str(e)}")
            return pd.DataFrame()
    
    def show_language_distribution(self):
        lang_counts = self.df['Language'].value_counts().reset_index()
        lang_counts.columns = ['Language', 'Count']
        
        fig = self.create_bar_chart(
            data=lang_counts,
            x='Language',
            y='Count',
            title='Repositories by Language',
            text=lang_counts['Count'].astype(str) + ' repos',
        )
        fig.update_traces(width=0.5)  # Make bars thinner
        fig.update_layout(
            title={
                'text': 'Repositories by Language',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#008294'}
            },
            xaxis_title='Programming Language',
            yaxis_title='Number of Repositories',
            xaxis_title_font={'color': '#008294', 'size': 16},
            yaxis_title_font={'color': '#008294', 'size': 16},
            showlegend=True,
            legend=dict(
                title="Languages",
                orientation="v",  # Vertical legend
                yanchor="top",  # Align to the top
                y=1,  # Keep it at the top
                xanchor="left",  # Align to the right
                x=1.02  # Slightly outside the plot to the right
            ),
            bargap=0.4  # Add more gap between bars
        )
        self.show_plotly_chart(fig, 'language_distribution')
    
    def show_top_repos(self):
        top_repos = self.df.nlargest(7, 'Stars').copy()
        
        # Create custom bar chart for better control
        fig = go.Figure()
        
        # Add bars with names for legend
        for lang in top_repos['Language'].unique():
            mask = top_repos['Language'] == lang
            fig.add_trace(go.Bar(
                x=top_repos[mask]['Name'],
                y=top_repos[mask]['Stars'],
                name=lang,
                marker_color=self.language_colors.get(lang, '#E0E0E0'),
                text=top_repos[mask]['Stars'].apply(lambda x: f'⭐ {int(x)}'),
                textposition='outside',
                textfont=dict(size=14, color='#4F4F4F'),
                hovertemplate='Stars: %{y}<br>Repository: %{x}<extra></extra>',
                width=0.5  # Make bars thinner
            ))
        
        # Update layout with more space and better visibility
        fig.update_layout(
            xaxis_tickangle=45,
            height=700,
            title={
                'text': 'Top 10 Repositories by Stars',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#008294'}
            },
            xaxis_title='Repository Name',
            yaxis_title='Number of Stars',
            xaxis_title_font={'color': '#008294', 'size': 16},
            yaxis_title_font={'color': '#008294', 'size': 16},
            yaxis=dict(
                rangemode='nonnegative',
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(211, 211, 211, 0.2)',
                range=[0, max(top_repos['Stars']) * 1.2]
            ),
            margin=dict(t=100, b=100, l=50, r=50),
            showlegend=True,
            legend=dict(
                title="Languages",
                orientation="v",  # Vertical legend
                yanchor="top",  # Align to the top
                y=1,  # Keep it at the top
                xanchor="left",  # Align to the right
                x=1.02  # Slightly outside the plot to the right
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            bargap=0.4  # Add more gap between bars
        )
        
        # Ensure text is visible for small values
        fig.update_traces(
            textangle=0,
            cliponaxis=False,
            textfont_color='#008294'
        )
        
        self.show_plotly_chart(fig, 'top_repos')
    
    def show_activity_timeline(self):
        self.df['Created'] = pd.to_datetime(self.df['Created'])

        monthly_activity = self.df.resample('M', on='Created').size().reset_index()
        monthly_activity.columns = ['Date', 'New Repos']
        
        # Create custom line chart
        fig = go.Figure()
        
        # Add line trace
        fig.add_trace(go.Scatter(
            x=monthly_activity['Date'],
            y=monthly_activity['New Repos'],
            mode='lines+markers+text',
            line=dict(color='#008294', width=2),
            text=monthly_activity['New Repos'].apply(lambda x: f'{int(x)}'),
            textposition='top center',
            textfont=dict(color='#008294', size=14),
            marker=dict(color='#008294', size=8)
        ))
        
        fig.update_layout(
            title={
                'text': 'Repository Creation Timeline',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#008294'}
            },
            xaxis_title='Date',
            yaxis_title='Repositories Count',
            xaxis_title_font={'color': '#008294', 'size': 16},
            yaxis_title_font={'color': '#008294', 'size': 16},
            yaxis=dict(
                rangemode='nonnegative',
                showgrid=True,
                gridcolor='rgba(211, 211, 211, 0.2)',
                zeroline=True,
                zerolinecolor='rgba(211, 211, 211, 0.2)'
            ),
            margin=dict(t=100, b=50)
        )
        self.show_plotly_chart(fig, 'activity_timeline')
    
    def show_popularity_scatter(self):
        fig = px.scatter(
            self.df,
            x='Stars',
            y='Forks',
            title='Repository Popularity',
            text='Name',
            width=800,
            height=600
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            showlegend=False,
            title={
                'text': 'Repository Popularity',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#008294'}
            },
            xaxis_title='Number of Stars',
            yaxis_title='Number of Forks',
            xaxis_title_font={'color': '#008294', 'size': 16},
            yaxis_title_font={'color': '#008294', 'size': 16}
        )
        self.show_plotly_chart(fig, 'popularity_scatter')
    
    def show(self):
        # st.title("Performance Metrics")
        st.markdown("<h1 style='text-align: center;'>Metrics</h1>", unsafe_allow_html=True)

        
        with st.spinner("Loading GitHub data..."):
            df = self.get_data()
        
        if not df.empty:
            # Summary metrics
            total_repos = len(df)
            original_repos = len(df[~df['Is Fork']])
            total_stars = df['Stars'].sum()
            total_forks = df['Forks'].sum()
            languages = df['Language'].nunique()
            
            metrics = [
                ("Total Repositories", str(total_repos), f"{original_repos} Original"),
                ("Total Stars ⭐", str(total_stars) , f"{total_stars - 4 }"),
                ("Total Forks 🔄", str(total_forks) , f"{total_forks - 5}"),
                ("Languages Used", str(languages), "")
            ]
            self.show_metrics(metrics)
            
            # Repositories Overview
            display_df = df.drop(['URL', 'Is Fork'], axis=1).copy()
            display_df['Created'] = pd.to_datetime(display_df['Created']).dt.date
            display_df['Last Updated'] = pd.to_datetime(display_df['Last Updated']).dt.date
            
            column_config = {
                'Name': st.column_config.TextColumn('Repository', width='large'),
                'Language': st.column_config.TextColumn('Language', width='medium'),
                'Stars': st.column_config.NumberColumn('⭐', format="%d"),
                'Forks': st.column_config.NumberColumn('🔄', format="%d"),
                'Created': st.column_config.DateColumn('Created'),
                'Last Updated': st.column_config.DateColumn('Updated'),
                'Description': st.column_config.TextColumn('Description', width='large'),
            }
            # self.show_dataframe(display_df, column_config)
            
            # Create tabs for visualizations
            viz_tabs = st.tabs(["Distribution", "Performance"])
            
            with viz_tabs[0]:
                self.show_language_distribution()
                st.markdown("<br>", unsafe_allow_html=True)
                self.show_top_repos()
            
            with viz_tabs[1]:
                self.show_activity_timeline()
            
            # with viz_tabs[2]:
            #     self.show_popularity_scatter()
        
        else:
            st.warning("Unable to load GitHub data. Please check your credentials.")

def main():
    visualizer = GitHubVisualizer(0)
    visualizer.show()

if __name__ == "__main__":
    main()
