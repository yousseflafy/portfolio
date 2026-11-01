import streamlit as st
from src import about, journey, certificates, projects
import os

st.set_page_config(
    page_title="Portfolio & Research Work",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Load external CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the external CSS file
css_path = os.path.join(os.path.dirname(__file__), 'style.css')
load_css(css_path)

# Rounded Hero Header Component
header_html = """
<div class="app-header-card">
    <div class="header-badge-row">
        <span class="header-status-badge">
            <span class="header-status-dot"></span>
            Available for Research & Collaborations
        </span>
    </div>
    <div class="header-title">Data Science & Biostatistical Portfolio</div>
    <p class="header-subtitle">
        Bridging statistical methodology, clinical observational data validation, 
        and interactive data systems to generate reproducible real-world evidence.
    </p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
# Create tabs
tabs = ["About Me", "Professional Journey", "Projects", "Certificates"]
current_tab = st.tabs(tabs)

# Initialize tab_id in session state if not present
if 'tab_id' not in st.session_state:
    st.session_state.tab_id = 0

# Render content based on selected tab
with current_tab[0]:
    about.show()
with current_tab[1]:
    journey.show()
with current_tab[2]:
    projects.show()
with current_tab[3]:
    certificates.show()
# with current_tab[4]:
#     dashboard.show()
