# import streamlit as st
# import json
# from typing import Dict, List
# from pathlib import Path

# class ProjectManager:
#     def __init__(self, json_path: str):
#         self.json_path = Path(json_path)
#         self.projects = self._load_projects()
        
#     def _load_projects(self) -> Dict:
#         """Load projects from JSON file."""
#         with open(self.json_path, 'r') as f:
#             return json.load(f)
            
#     def get_all_categories(self) -> List[str]:
#         """Get list of all categories in order."""
#         return list(self.projects['projects'].keys())

# def show():
#     # Custom CSS for styling
#     st.markdown("""
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
        
#         .category-title {
#             text-align: center;
#             font-size: 2.5em;
#             font-weight: bold;
#             margin: 1.5em 0;
#             color: #1f77b4;
#             padding: 20px;
#             border-bottom: 2px solid #1f77b4;
#         }
#         .project-box {
#             border: 1px solid #e1e1e1;
#             border-radius: 10px;
#             padding: 25px;
#             margin: 15px 0;
#             box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#             height: 100%;
#         }
#         .project-title {
#             text-align: left;
#             font-size: 1.5em;
#             font-weight: bold;
#             margin-bottom: 1em;
#             color: #008294;
#             border-bottom: 1px solid #eee;
#             padding-bottom: 10px;
#             font-family: 'Roboto', sans-serif;
#         }
#         .project-description {
#             font-size: 1.1em;
#             margin: 1em 0;
#             color: gray;
#             line-height: 1.6;
#         }
#         .tech-container {
#             display: flex;
#             align-items: center;
#             gap: 15px;
#             margin-top: 20px;
#         }
#         .tech-tags {
#             display: flex;
#             flex-wrap: wrap;
#             gap: 8px;
#             flex: 1;
#         }
#         .tech-tag {
#             display: inline-block;
#             background-color: #f0f2f6;
#             border-radius: 15px;
#             padding: 5px 15px;
#             margin: 2px;
#             font-size: 14px;
#             color: #0E1117;
#             border: 1px solid #e0e0e0;
#         }
#         .tech-tag:hover {
#             background-color: #e0e2e6;
#         }
#         .stButton button {
#             font-family: 'Roboto', sans-serif !important;
#             font-size: 16px !important;
#             color: #008294 !important;
#             border-color: #008294 !important;
#             height: 40px !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     try:
#         project_manager = ProjectManager('content/projects.json')
#         categories = project_manager.get_all_categories()
        
#         # Display projects by category
#         for category in categories:
#             st.markdown(f'<h1 class="category-title">{category}</h1>', unsafe_allow_html=True)
            
#             projects = project_manager.projects['projects'][category]
            
#             # Process projects in pairs
#             for i in range(0, len(projects), 2):
#                 left_col, mid_col, right_col = st.columns([2, 0.25, 2])
                
#                 # Left project
#                 with left_col:
#                     if i < len(projects):
#                         project = projects[i]
#                         st.markdown(f"""
#                             <div class="project-box">
#                                 <div class="project-title">{project["title"]}</div>
#                                 <div class="project-description">{project["description"]}</div>
#                                 <div class="tech-container">
#                                     <div class="tech-tags">
#                                         {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in project["technologies"][:])}
#                                     </div>
#                         """, unsafe_allow_html=True)
                        
#                         st.link_button("View Project", project["link"], use_container_width=False)
                        
#                         st.markdown("""
#                                 </div>
#                             </div>
#                         """, unsafe_allow_html=True)
                
#                 # Middle column stays empty
#                 with mid_col:
#                     st.empty()
                
#                 # Right project
#                 with right_col:
#                     if i + 1 < len(projects):
#                         project = projects[i + 1]
#                         st.markdown(f"""
#                             <div class="project-box">
#                                 <div class="project-title">{project["title"]}</div>
#                                 <div class="project-description">{project["description"]}</div>
#                                 <div class="tech-container">
#                                     <div class="tech-tags">
#                                         {' '.join(f'<span class="tech-tag">{tech}</span>' for tech in project["technologies"][:])}
#                                     </div>
#                         """, unsafe_allow_html=True)
                        
#                         st.link_button("View Project", project["link"], use_container_width=False)
                        
#                         st.markdown("""
#                                 </div>
#                             </div>
#                         """, unsafe_allow_html=True)
            
#     except FileNotFoundError:
#         st.error("projects.json file not found")
#     except json.JSONDecodeError:
#         st.error("Invalid JSON format in projects.json")
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     show()

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import streamlit as st
import streamlit.components.v1 as components

@st.cache_data
def load_projects_data(filepath: str = "content/projects.json") -> List[Dict[str, Any]]:
    path = Path(filepath)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "projects" in data:
            if isinstance(data["projects"], list):
                return data["projects"]
            flattened = []
            for category, items in data["projects"].items():
                for item in items:
                    item.setdefault("category", category)
                    flattened.append(item)
            return flattened
    return []

@st.dialog("Project Preview", width="large")
def render_html_modal(title: str, html_path: str):
    st.subheader(title)
    if not os.path.exists(html_path):
        st.error(f"File not found: `{html_path}`")
        return
    with open(html_path, "r", encoding="utf-8") as f:
        components.html(f.read(), height=720, scrolling=True)

def render_project_card(project: Dict[str, Any]):
    with st.container(border=True):
        category = project.get("category", "General")
        st.markdown(f'<span class="project-category-badge">{category}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="project-title">{project.get("title", "Untitled")}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="project-description">{project.get("description", "")}</p>', unsafe_allow_html=True)
        
        techs = project.get("technologies", [])
        if techs:
            tags_html = " ".join([f'<span class="skill-chip">{tech}</span>' for tech in techs])
            st.markdown(f'<div class="skill-pills-container" style="margin-bottom: 1rem;">{tags_html}</div>', unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns([1, 1], gap="small")
        html_file = project.get("html_file")
        external_url = project.get("url") or project.get("link")
        
        with btn_col1:
            if html_file:
                if st.button("Preview Report ↗", key=f"preview_{project.get('title')}", use_container_width=True):
                    render_html_modal(project.get("title", "Project View"), html_file)
            elif external_url:
                st.link_button("View Demo ↗", external_url, use_container_width=True)
            else:
                st.button("In Progress", disabled=True, key=f"none_{project.get('title')}", use_container_width=True)
                
        with btn_col2:
            github_url = project.get("github")
            if github_url:
                st.link_button("Source Code", github_url, use_container_width=True)

def show():
    st.markdown('<h1>Featured Projects</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--muted); margin-bottom: 1.5rem;">Interactive analytical reports, dashboards, and research tooling.</p>', unsafe_allow_html=True)
    
    projects = load_projects_data("content/projects.json")
    if not projects:
        st.warning("No projects found in `content/projects.json`.")
        return

    all_categories = ["All"] + sorted(list({p.get("category", "General") for p in projects}))
    
    # Perfect widget alignment: vertical_alignment="bottom" aligns search box with filter pills
    filter_col, search_col = st.columns([2.5, 1.5], gap="medium", vertical_alignment="bottom")
    
    with filter_col:
        selected_category = st.pills("Filter by domain:", all_categories, default="All", label_visibility="collapsed")
    with search_col:
        search_query = st.text_input("Search", placeholder="Search projects...", label_visibility="collapsed")

    filtered_projects = projects
    if selected_category and selected_category != "All":
        filtered_projects = [p for p in filtered_projects if p.get("category") == selected_category]
    
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_projects = [
            p for p in filtered_projects 
            if q in p.get("title", "").lower() 
            or q in p.get("description", "").lower()
            or any(q in t.lower() for t in p.get("technologies", []))
        ]

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if not filtered_projects:
        st.info("No projects match your criteria.")
        return

    for i in range(0, len(filtered_projects), 2):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            render_project_card(filtered_projects[i])
        with col2:
            if i + 1 < len(filtered_projects):
                render_project_card(filtered_projects[i + 1])
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     show()