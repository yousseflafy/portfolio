import streamlit as st
import json
import os
from PIL import Image
import base64

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def show():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');
        
        .title-text {
            color: #008294;
            font-family: 'Roboto', sans-serif;
            font-size: 24px;
            font-weight: 500;
            margin-bottom: 40px;
        }
        
        .cert-title {
            color: #008294;
            font-family: 'Roboto', sans-serif;
            font-size: 20px;
            font-weight: 500;
            margin: 0 0 35px 0;
            text-align: center;
        }
        
        .cert-container {
            margin-bottom: 40px;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .cert-content {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
        
        .button-row {
            margin-top: auto;
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 20px 0;
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
    
    st.markdown('<h1 class="title-text">CERTIFICATES</h1>', unsafe_allow_html=True)
    
    try:
        with open('content/certificates.json', 'r', encoding='utf-8') as file:
            certificates = json.load(file).get('certificates', [])
        
        for i in range(0, len(certificates), 3):
            cols = st.columns(3)
            batch = certificates[i:i+3]
            
            for col, cert in zip(cols, batch):
                with col:
                    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
                    st.markdown('<div class="cert-content">', unsafe_allow_html=True)
                    
                    # Title
                    st.markdown(f'<div class="cert-title">{cert.get("title", "")}</div>', unsafe_allow_html=True)
                    
                    # Image
                    image_path = f"assets/photos/certificates/{cert.get('image', '')}"
                    if os.path.exists(image_path):
                        image = Image.open(image_path).convert('RGB')
                        st.image(image, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Button row
                    if cert.get('verify_link'):
                        st.markdown('<div class="button-row">', unsafe_allow_html=True)
                        st.link_button("Verify Certificate", cert['verify_link'], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Add space between rows
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
