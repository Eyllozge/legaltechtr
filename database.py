import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS startups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            website VARCHAR(200),
            founded_year INT
            
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS founders (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            title VARCHAR(100),
            linkedin VARCHAR(200),
            startup_id INT NOT NULL REFERENCES startups(id)
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS experts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            area VARCHAR(100),
            linkedin VARCHAR(200),
            startup_id INT REFERENCES startups(id)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tablolar oluşturuldu.")