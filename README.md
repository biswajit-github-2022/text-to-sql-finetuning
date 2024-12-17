# Project: T5 Model Fine-Tuning and Application

This project demonstrates the fine-tuning of the T5-small model from Hugging Face for text-to-text tasks, integration with MySQL, and schema generation. The repository is structured to include a Streamlit application, database testing, and fine-tuning notebooks.

---

## 📂 Directory Structure

- **`src/`**  
  - **`weights`**: Download from givem link below. 
  - **`app_version4.py`**: Contains the Streamlit application for user interaction.

- **`testing/`**  
  - **`connect.py`**: Tests the connection to the MySQL database.  
  - **`getschema.py`**: Generates the schema required to feed data into the fine-tuned model.  

- **`finetune.ipynb`**  
  Notebook for fine-tuning the T5-large model. The model has been trained for one epoch, achieving promising results.

---

## 📋 Requirements

To run this project, ensure you have the following dependencies installed:

```plaintext
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
```

---

## Note: 

We have used the weights we got by doing the finetuning in **`app_version4.py`**, and used pretrained model in **`app_version3.py`**
You also have to do the configeration for Mysql Data base for the streamlit app to work properly.
Keep the weights in a **`weights`** folder in the root folder of the project.
Download the weights from [https://drive.google.com/drive/folders/1kWGmSJI7Q2o4qnt2K85HHsuhJxF9Cjkh?usp=drive_link](https://drive.google.com/drive/folders/1kWGmSJI7Q2o4qnt2K85HHsuhJxF9Cjkh?usp=drive_link)