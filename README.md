# Data Science Portfolio

A modern, interactive portfolio website built with Streamlit showcasing your data science projects, professional journey, and achievements.

## Features

- About Me section with professional summary
- Interactive Professional Journey timeline
- Certificates showcase with verification links
- Projects portfolio with GitHub integration
- Analytics dashboard showing GitHub and Kaggle statistics

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create necessary directories:
```bash
mkdir -p assets/photos/companies assets/photos/certificates assets/photos/projects
```

3. Add your images:
- Profile photo in `assets/photos/profile_photo.jpg`
- Company logos in `assets/photos/companies/`
- Certificate images in `assets/photos/certificates/`
- Project images in `assets/photos/projects/`

4. Update content:
- Edit markdown files in `content/` directory
- Update JSON files with your information

5. Run the application:
```bash
streamlit run app.py
```

## Customization

- Edit `style.css` to customize the appearance
- Modify JSON files in `content/` to update your information
- Add new pages by creating new Python files in the `src/` directory

## Requirements

- Python 3.8+
- Streamlit
- Plotly
- Pandas
- Requests
- Markdown
