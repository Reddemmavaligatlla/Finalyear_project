# Personalized Recommendation System for E-Commerce Platform

## 📌 Project Overview
This project is a **Personalized Recommendation System** designed for an e-commerce platform.  
It recommends products to users based on their preferences, past interactions, and similarity with other users.

The project uses a cleaned e-commerce dataset containing product details and user interaction data.

The system combines:
- Content-based recommendations
- Collaborative filtering
- User interaction analysis (likes)

The application is built using **Python and Flask** with a simple web interface.

---

## 🎯 Project Objective
The main objective of this project is to improve user experience in e-commerce platforms by:
- Understanding user interests
- Suggesting relevant products
- Providing personalized recommendations instead of generic product lists

---

## 🧠 How the System Works (High Level)
1. User interacts with products on the website  
2. Product features and user behavior are analyzed  
3. Similar users and similar products are identified  
4. Personalized recommendations are generated and displayed  

---

## 🚀 Key Features
- Personalized product recommendations  
- User-based similarity analysis  
- Product similarity matching  
- Like-based preference learning  
- Web-based interface using Flask  
- Dynamic recommendation results  

---

## 🗂 Project Structure# 🛠 Technologies Used
```text
college_project/
├── app.py                     # Main Flask application
├── models/
│   ├── content_based.py       # Content-based recommendation logic
│   ├── collaborative.py      # Collaborative filtering logic
│   ├── regression_model.py   # Like prediction model
├── data/
│   ├── users.json             # User interaction data
│   ├── ecommerce_dataset_cleaned.csv
├── templates/
│   ├── index.html             # Home page
│   ├── products.html          # Product listing page
│   ├── recommend.html         # Recommendation results page
├── static/
│   └── css/                   # Styling files
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation



🛠 Technologies Used
- `Python`
- `Flask`
- `Pandas`
- `NumPy`
- `Scikit-learn`
- `HTML & CSS`
- `Git & GitHub`

▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/Reddemmavaligatlla/college_project.git
cd college_project

2️⃣ Install Required Dependencies
pip install -r requirements.txt

3️⃣ Run the Application
python app.py

4️⃣ Open in Browser
http://127.0.0.1:5000/

📈 Output
The system displays personalized product recommendations based on user preferences, product similarity, and interaction behavior.