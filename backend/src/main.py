from fastapi import FastAPI
from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd

app = FastAPI()

load_dotenv()

DB_URL = os.getenv("DB_URL") 

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/check-db")
def check_db_connection():
    try:
        conn = psycopg2.connect(DB_URL)
        query_sql = "SELECT VERSION()"
        cur = conn.cursor()
        cur.execute(query_sql)
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"message": "Database connection successful", "version": version}
    except Exception as e:
        return {"error": str(e)}

@app.post("/process")
def process_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
    file_path = os.path.join(base_dir, "data", "data.txt")  

    try:
        df = pd.read_csv(file_path, sep=";", dtype=str)

        print(df.head())

        df = df.fillna("")  

        return {"data": df.to_dict(orient="records")}

    except FileNotFoundError:
        return {"error": f"File not found at path: {file_path}"}
    except Exception as e:
        return {"error": str(e)}
