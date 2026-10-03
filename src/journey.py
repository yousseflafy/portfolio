import streamlit as st
import json
from streamlit_timeline import timeline

def show():
    # st.title("PROFESSIONAL JOURNEY")
    
    try:
        # Read and display timeline
        with st.spinner(text="Building timeline..."):
            with open('content/timeline.json', "r", encoding='utf-8') as f:
                data = f.read()
                timeline(data, height=600)
    
    except FileNotFoundError:
        st.error("Timeline data file not found. Please create content/timeline.json")
    except json.JSONDecodeError:
        st.error("Invalid JSON format in timeline.json")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
