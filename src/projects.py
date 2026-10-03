import streamlit as st
import json
from typing import Dict, List
from pathlib import Path

class ProjectManager:
    def __init__(self, json_path: str):
        self.json_path = Path(json_path)
        self.projects = self._load_projects()
        
    def _load_projects(self) -> Dict:
        """Load projects from JSON file."""
        with open(self.json_path, 'r') as f:
            return json.load(f)
            
    def get_all_categories(self) -> List[str]:
        """Get list of all categories in order."""
        return list(self.projects['projects'].keys())

def show():
    # Custom CSS for styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
        
        .category-title {
            text-align: center;
            font-size: 2.5em;
            font-weight: bold;
            margin: 1.5em 0;
            color: #1f77b4;
            padding: 20px;
            border-bottom: 2px solid #1f77b4;
        }
        .project-box {
            border: 1px solid #e1e1e1;
            border-radius: 10px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            height: 100%;
        }
        .project-title {
            text-align: left;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 1em;
            color: #008294;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
            font-family: 'Roboto', sans-serif;
        }
        .project-description {
            font-size: 1.1em;
            margin: 1em 0;
            color: gray;
            line-height: 1.6;
        }
        .tech-container {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 20px;
        }
        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            flex: 1;
        }
        .tech-tag {
            display: inline-block;
            background-color: #f0f2f6;
            border-radius: 15px;
            padding: 5px 15px;
            margin: 2px;
            font-size: 14px;
            color: #0E1117;
            border: 1px solid #e0e0e0;
        }
        .tech-tag:hover {
            background-color: #e0e2e6;
        }
        .stButton button {
            font-family: 'Roboto', sans-serif !important;
            font-size: 16px !important;
            color: #008294 !important;
            border-color: #008294 !important;
            height: 40px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        project_manager = ProjectManager('content/projects.json')
        categories = project_manager.get_all_categories()
        
        # Display projects by category
        for category in categories:
            st.markdown(f'<h1 class="category-title">{category}</h1>', unsafe_allow_html=True)
            
            projects = project_manager.projects['projects'][category]
            
            # Process projects in pairs
            for i in range(0, len(projects), 2):
                left_col, mid_col, right_col = st.columns([2, 0.25, 2])
                
                # Left project
                with left_col:
                    if i < len(projects):
                        project = projects[i]
                        st.markdown(f"""
                            <div class="project-box">
                                <div class="project-title">{project["title"]}</div>
                                <div class="project-description">{project["description"]}</div>
                                <div class="tech-container">
                                    <div class="tech-tags">
                                        {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in project["technologies"][:])}
                                    </div>
                        """, unsafe_allow_html=True)
                        
                        st.link_button("View Project", project["link"], use_container_width=False)
                        
                        st.markdown("""
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                
                # Middle column stays empty
                with mid_col:
                    st.empty()
                
                # Right project
                with right_col:
                    if i + 1 < len(projects):
                        project = projects[i + 1]
                        st.markdown(f"""
                            <div class="project-box">
                                <div class="project-title">{project["title"]}</div>
                                <div class="project-description">{project["description"]}</div>
                                <div class="tech-container">
                                    <div class="tech-tags">
                                        {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in project["technologies"][:])}
                                    </div>
                        """, unsafe_allow_html=True)
                        
                        st.link_button("View Project", project["link"], use_container_width=False)
                        
                        st.markdown("""
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error("projects.json file not found")
    except json.JSONDecodeError:
        st.error("Invalid JSON format in projects.json")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    show()
