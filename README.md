CORD-19 COVID-19 Research Data Analysis

📊 Project Overview

This project analyzes metadata from the CORD-19 dataset, which contains over 1.3 million COVID-19 research papers. The analysis focuses on understanding publication trends, key journals, authors, and research patterns during the pandemic years (2019-2023).

🎯 Key Objectives

Clean and preprocess large-scale research metadata

Analyze publication trends over time

Identify leading journals and authors in COVID-19 research

Extract key research topics from titles and abstracts

Create interactive visualizations and exportable reports

📁 Project Structure
text
cord19-analysis/
│
├── PythonWeek8.ipynb          # Data preprocessing and cleaning
├── PythonWeek8.html        # Statistical analysis and visualization  
├── cleaned_cord19_data.csv  # Excel report (generated)
├── app.py                       # Streamlit dashboard (conceptual)
└── README.md                    # This file
🔍 Key Findings
📈 Publication Trends
Explosive growth in COVID-19 publications starting in 2020

Sustained high volume of research through 2022-2023

Clear correlation with pandemic waves and response needs

🏥 Top Journals
Leading publishers of COVID-19 research include:

BMJ (British Medical Journal)

The Lancet

JAMA (Journal of the American Medical Association)

Nature and Science journals

Various public health and virology journals

🔬 Research Focus Areas
Most common topics in paper titles:

covid, pandemic, patients, health, clinical

virus, infection, vaccine, treatment, public

study, analysis, model, data, response

🛠️ Technical Implementation
Data Cleaning Steps
Handled missing data (>95% missing columns removed)

Standardized formats (date conversion, text cleaning)

Removed duplicates based on title and author combinations

Created derived features (word counts, publication years)

Filtered relevant time period (2019-2023)

Analysis Techniques
Time series analysis of publication patterns

Frequency analysis of journals and authors

Text mining of titles and abstracts

Statistical summaries of paper characteristics

Correlation analysis between features

📊 Outputs Generated
Excel Reports
Sample dataset (first 1000 papers)

Summary statistics (key metrics and counts)

Yearly publication trends

Top journals and authors rankings

Word frequency analysis

Source distribution analysis

Visualizations
Monthly publication trend charts

Journal ranking bar charts

Word clouds of research topics

Distribution plots of paper characteristics

Correlation heatmaps of numerical features

🚀 How to Use
Prerequisites
bash
pip install pandas matplotlib seaborn wordcloud openpyxl
Basic Analysis
Run data cleaning notebook to create df_clean

Execute analysis cells to generate insights

Check Desktop for Excel report files

Streamlit App (Conceptual)
bash
# If implemented:
pip install streamlit
streamlit run app.py
⚠️ Notes on Streamlit App
The Streamlit application component was designed but not fully implemented due to:

Large dataset size (~1.3GB) requiring optimized loading

Memory considerations for web deployment

Focus on core analysis and export capabilities

The app structure was designed to include:

Year range sliders for temporal filtering

Journal selection dropdowns

Interactive visualizations

Data export functionality

📈 Insights for Researchers
Rapid Response: Academic community quickly mobilized for COVID-19 research

Interdisciplinary: Research spanned medicine, public health, economics, and social sciences

Open Science: High proportion of preprints and open-access publications

Global Effort: International collaboration evident in author affiliations

🔮 Future Enhancements
Topic modeling using NLP techniques

Citation network analysis

Author collaboration networks

Integration with full-text analysis

Real-time dashboard with automatic updates

📋 Data Source
CORD-19 (COVID-19 Open Research Dataset)

Source: Semantic Scholar

Size: ~1.3 million papers

Time span: 2019-2023

Fields: Medicine, public health, biology, social sciences

👨‍💻 Author
Data analysis project exploring COVID-19 research trends and patterns using Python data science tools and techniques.

Note: This analysis focuses on metadata only. Full text analysis would provide deeper insights into research content and finding