from fastapi import FastAPI, HTTPException
from fastapi import FastAPI
from database import get_connection
from pydantic import BaseModel
from psycopg2 import errors
from fastapi.staticfiles import StaticFiles



class SubscribeRequest(BaseModel):
    name: str=None
    email: str

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/companies")
def get_companies(category: str = None):
    conn = get_connection()
    cur = conn.cursor()
    
    if category:
        cur.execute("""
            SELECT s.id, s.name, s.category, s.description, s.website, s.founded_year
            FROM startups s
            WHERE s.category = %s
        """, (category,))
    else:
        cur.execute("""
            SELECT s.id, s.name, s.category, s.description, s.website, s.founded_year
        FROM startups s
    """)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    companies = []
    for row in rows:
        companies.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "website": row[4],
            "founded_year": row[5]
        })
    
    return companies



   

@app.get("/companies/{company_id}")
def get_company(company_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, name, category, description, website, founded_year
        FROM startups
        WHERE id = %s
    """, (company_id,))
    
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
     raise HTTPException(status_code=404, detail="Startup bulunamadı")
    
    return {
        "id": row[0],
        "name": row[1],
        "category": row[2],
        "description": row[3],
        "website": row[4],
        "founded_year": row[5]
    }
    
@app.post("/subscribe")
def subscribe(request: SubscribeRequest):
    conn = get_connection()
    cur = conn.cursor()

     
    try:
        cur.execute("""
            INSERT INTO subscribers (name, email)
            VALUES (%s, %s)
            RETURNING id
        """, (request.name, request.email))
        new_id = cur.fetchone()[0]
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    finally:
        cur.close()
        conn.close()
    
    
    return {
        "id": new_id,
        "name": request.name,
        "email": request.email
    }
    
    