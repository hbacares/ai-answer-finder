import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
conn.autocommit = True

def get_best_answer(query_embedding, threshold=1.85):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT question, answer, 1 - (embedding <#> %s::vector) AS score
            FROM faqs
            ORDER BY embedding <#> %s::vector
            LIMIT 1;
        """, (query_embedding, query_embedding))
        row = cur.fetchone()

        if row and row[2] >= threshold:
            return {
                "question": row[0],
                "answer": row[1],
                "score": round(row[2], 3)
            }
        else:
            return {
                "question": None,
                "answer": None,
                "score": round(row[2], 3) if row else None
            }
        return None