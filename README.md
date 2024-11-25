Project: T5 Model Fine-Tuning and Application
This project demonstrates the fine-tuning of the T5-large model from Hugging Face for text-to-text tasks, integration with MySQL, and schema generation. The repository is structured to include a Streamlit application, database testing, and fine-tuning notebooks.

Directory Structure
src/
Contains the Streamlit application for user interaction.

testing/

connect.py: Tests the connection to the MySQL database.
getschema.py: Generates the schema required to feed data into the fine-tuned model.
finetune.ipynb
Notebook for fine-tuning the T5-large model. The model has been trained for one epoch, achieving promising results.

Requirements
To run this project, ensure you have the following dependencies installed:

Copy code
streamlit
pandas
sqlalchemy
transformers
torch
evaluate
datasets
numpy
scikit-learn
pymysql
You can install them using:

bash
Copy code
pip install -r requirements.txt
Highlights
Fine-Tuning:
The finetune.ipynb file showcases the process of fine-tuning a T5-large model for one epoch on the desired dataset, producing accurate results.

Database Connection:
The connect.py script verifies MySQL database connectivity using PyMySQL.

Schema Generation:
The getschema.py script dynamically generates schemas tailored to the input structure for the fine-tuned model.

Streamlit Application:
A user-friendly interface provided through Streamlit for real-time interaction with the fine-tuned model.

How to Use
Install Dependencies
Run the following command to set up the required libraries:

bash
Copy code
pip install -r requirements.txt
Database Testing
Execute testing/connect.py to test the MySQL database connection.

Generate Schema
Run testing/getschema.py to generate the schema for feeding into the fine-tuned model.

Streamlit Application
Navigate to the src folder and launch the Streamlit app:

bash
Copy code
streamlit run app.py
Fine-Tuning
Open and run the finetune.ipynb notebook to observe or reproduce the fine-tuning process.

