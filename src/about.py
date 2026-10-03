import streamlit as st
import markdown
import os

def show():
    # st.title("ABOUT ME")
    
    # Main layout with two columns
    main_col1, main_col2 = st.columns([1, 2], gap="large")
    
    # Left column - Profile photo
    with main_col1:
        profile_photo = "assets/photos/profile_photo.jpg"
        if os.path.exists(profile_photo):
            st.image(profile_photo, use_container_width=True)
        else:
            st.info("Please add your profile photo to assets/photos/profile_photo.jpg")
    
    # Right column - About content and social links
    with main_col2:
        # About content
        with open('content/about.md', 'r', encoding='utf-8') as file:
            about_content = file.read()
            st.markdown(about_content)
        
        # Social links
        social_col1, social_col2, social_col3 = st.columns(3)
        with social_col1:
            st.link_button("LinkedIn", "https://www.linkedin.com/in/youssef-lafy-aa9808216")
        with social_col2:
            st.link_button("Kaggle", "https://www.kaggle.com/yousseflafy/code")
        # with social_col3:
        #     st.link_button("GitHub", "https://github.com/Muhammet-Abd-ElWahab?tab=repositories")
    
    # Skills section
    st.markdown("---")
    # col1, col2 = st.columns(2)
    # with col2:
    #     social_col1, social_col2, social_col3 = st.columns(3)
    #     with social_col1:
    #         st.link_button("LinkedIn", "https://www.linkedin.com/in/mohamed-gamal-abdelwahab/")
    #     with social_col2:
    #         st.link_button("Kaggle", "https://www.kaggle.com/muhammetgamal5/code")
    #     with social_col3:
    #         st.link_button("GitHub", "https://github.com/Muhammet-Abd-ElWahab?tab=repositories")
    st.header("Skills & Tools")
#    
    # Custom CSS for tags
    st.markdown("""
        <style>
        .skill-tag {
            display: inline-block;
            background-color: #f0f2f6;
            border-radius: 15px;
            padding: 5px 15px;
            margin: 4px;
            font-size: 14px;
            color: #0E1117;
            border: 1px solid #e0e0e0;
        }
        .skill-tag:hover {
            background-color: #e0e2e6;
        }
        .skills-container {
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Read skills content
    with open('content/skills.md', 'r', encoding='utf-8') as file:
        skills_content = file.read()
    
    # Create three columns for skills sections
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    current_col = 0
    
    # Process each skill section
    sections = skills_content.split('##')[1:]
    for section in sections:
        if not section.strip():
            continue
        
        # Split into title and skills
        parts = section.strip().split('\n', 1)
        if len(parts) != 2:
            continue
            
        title, content = parts
        
        # Use the next column
        with columns[current_col]:
            st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
            
            # Extract skills
            skills = [skill.strip('- \n') for skill in content.split('\n') if skill.strip().startswith('-')]
            
            # Create tags for skills
            tags_html = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
            st.markdown(f'<div class="skills-container">{tags_html}</div>', unsafe_allow_html=True)
        
        # Move to next column
        current_col = (current_col + 1) % 3
