# 📊 PhonePe Transaction Insights Dashboard

An interactive dashboard and analytical study of digital payment trends across India, powered by PhonePe Pulse data.

---

## 1. 📌 Project Overview

This project analyzes PhonePe’s publicly available data to uncover insights into digital payment trends, user behavior, and geographic variations across India. Built using **Python**, **SQL**, and **Streamlit**, it transforms complex datasets into actionable business intelligence through interactive visualizations.

---

## 2. 💼 Domain

**Finance / Digital Payments**

---

## 3. 🧠 Key Technologies & Skills

- **Programming:** Python  
- **Database:** PostgreSQL, SQLAlchemy  
- **Visualization:** Plotly, Seaborn, Matplotlib  
- **Web App:** Streamlit  
- **Data Handling:** Pandas, JSON, CSV  

---

## 4. 🎯 Objectives

- Transform and analyze PhonePe data to extract key insights.
- Visualize trends across states, districts, and quarters.
- Build an interactive dashboard for dynamic user exploration.
- Provide strategic recommendations based on analysis.

---

## 5. 🗂️ Dataset Overview

**Source:** [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)

**Data Categories:**
- **Aggregated Data:** User metrics, transactions, insurance
- **Map Data:** Geospatial metrics by state/district
- **Top Data:** Rankings of top-performing regions

**Transformation:** Raw JSON ➝ Cleaned CSV using custom Python scripts.

---

## 6. 📁 Project Structure

```plaintext
PHONEPE_PLUSE_ANALYZER/
├── data/
│   └── Data_Extract/                  # CSV files derived from raw JSON
├── image/
│   ├── Image.jpg
│   └── PhonePe_Logo.png
├── db_load.py                         # Loads data to PostgreSQL
├── main.ipynb                         # Main analysis & EDA
├── phonepe.py                         # Streamlit app
├── Phonepe_Docs.docx                  # Detailed project documentation
├── README.md                          # This file
├── .gitignore
├── LICENSE
