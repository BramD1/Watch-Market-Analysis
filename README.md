# 📊 Project Title: Watch Market Data Analysis
## 📝 Overview
In this project, I will act as a Data Analyst from Rolex and I will provide insight regarding how the company compares to its competitor
along with the customer insight that will prove useful for the company. The insight will then be used to give advice to the Product
Managers and Supply Chain Managers regarding the watch production and business strategy.

## Presentation Link (Canva):
https://www.canva.com/design/DAGcDm0jW_Q/V_o2muLGX_7hDjirGc6EVg/edit?utm_content=DAGcDm0jW_Q&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton 

## 📂 Dataset
Source: https://www.kaggle.com/datasets/beridzeg45/watch-prices-dataset/data 

Size: 45025 rows × 23 columns

Description: This is watch market dataset that I gathered from Kaggle

## 🔧 Technologies Used
Programming Language: Python

Libraries: Pandas, Seaborn, Matplotlib, NumPy, Airflow, PythonGX, elasticsearch, Scipy, ScikitLearn

Tools: Jupyter Notebook, SQL, Docker, ElasticNet, Kibana, Airflow

## 🚀 Workflow
### 1️ Data Collecting
This is the part where I download the data from Kaggle and move it to my SQL Database
### 2 Data Extraction, Transformation, and Load inside the DAG file
This DAG file is responsible to create an ETL process of the data, which are:
1. Extraction
- This is where the raw data is extracted from my SQL database using query
2. Transformation
- This is the part where I clean the data by dropping unecessary column, handling missing values, and dropping duplicates
- The columns dropped are: 'Availability', 'Shape', 'Gender', 'Active listing of the seller', 'Dial', 'Bracelet color', 'Face Area', 'Bracelet material', 'Clasp'
- Missing values inside 'Price' and 'Movement' columns are removed, while others are filled with values.
- Dropping duplicates.
- Changing column names from using uppercase to lowercase for all columns.
- This cleaning process leaves me with 38805 rows to work with which is significant differences compared to the raw data. 
3. Loading
- After I get the cleaned version of the data, I load the data into ElasticNet to be further used in Kibana for visualization
### 3 Create Schedule Interval
The scheduling for the ETL is set to be done every Saturday for 10 minutes between 09:10 - 09:30
### 4 Great Expectation
To ensure my data is proper to use, I use great expectation which consists of:
1. No null values
2. Unique values for column `id`
3. Expect value to be between 0 and 6 million for column `price`
4. Expect only value of 0 or 1 for the column `trusted_seller`
5. Expect column `sold` to be a type of integer or float
6. Expect column `year_produced` to be higher than `punctual`
7. Expect `Automatic` to be the most common value for the `movement` column
8. Expect the median value of the `review` column to be between 0 and 300
### 5 Regression Analysis
I did a bit of regression for the sole purpose of finding which columns have the most correlation with `price`, our variable of interest, specifically for the Rolex brand. For more detail, you can check the Canva link above.
### 6 Kibana Analysis
This is the part where I create visualization using Kibana, which I find to be easier to do compared to Tableau (personally). I find interesting insights during this part regarding the value of vintage watches. The full analysis is located in the Canva file I put above.
### 7 Conclusion
This entire project purpose is to mainly highlight my skill in Data Engineering line of work. Hence, the conclusion here will mostly be about DE parts (DA part and insight can be seen in the Canva link). I have successfully done the ETL process of the airflow and create a schedule interval in case of changes in the database. The Python GX might needs some work since I only did the ones I personally felt necessary for this database. A more standardized and strict corporate great expectation for the clean data might be needed in this case.

## Thank You For Visiting!!

📬 Connect with me and give me feedback

💼 Linkedin: https://www.linkedin.com/in/bramantyo-anandaru-suyadi-0b9729208/ 