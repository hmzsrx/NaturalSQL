from langchain_core.tools import tool
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

from sqlalchemy import text
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))


@tool
def get_database_schema() -> str:
    """
    Database ka poora schema return karta hai — sab tables, unke columns,
    aur foreign key relationships. Kisi bhi SQL query banane se PEHLE
    ye tool zaroor call karo, taake sahi table/column names pata chalein.
    """
    inspector = inspect(engine)
    schema_text = ""

    for table_name in inspector.get_table_names():
        schema_text += f"Table: {table_name}\n"

        # Columns nikalna
        columns = inspector.get_columns(table_name)
        for col in columns:
            schema_text += f"  - {col['name']} ({col['type']})\n"

        # Foreign keys nikalna
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            local_col = fk['constrained_columns'][0]
            ref_table = fk['referred_table']
            ref_col = fk['referred_columns'][0]
            schema_text += f"  Foreign Key: {local_col} -> {ref_table}.{ref_col}\n"

        schema_text += "\n"

    return schema_text


# Test karne ke liye
if __name__ == "__main__":
    print(get_database_schema.invoke({}))



@tool
def run_sql_query(query: str) -> str:
    """
    Diye gaye SQL query ko database par chalata hai aur result return karta hai.
    SIRF SELECT queries allowed hain — koi INSERT, UPDATE, DELETE, DROP nahi chalega.
    Query chalane se pehle get_database_schema tool use kar ke sahi table/column
    names confirm kar lo.
    """
    cleaned_query = query.strip().lower()

    # --- Read-Only Guard ---
    if not cleaned_query.startswith("select"):
        return "Error: Sirf SELECT queries allowed hain. Ye query reject kar di gayi."

    dangerous_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    if any(keyword in cleaned_query for keyword in dangerous_keywords):
        return "Error: Ye query khatarnak keywords contain karti hai, isliye reject kar di gayi."

    # --- Query Execute karna ---
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()

            if not rows:
                return "Query chal gayi, lekin koi result nahi mila."

            # Result ko readable text mein format karna
            output = ", ".join(columns) + "\n"
            for row in rows:
                output += ", ".join(str(val) for val in row) + "\n"
            return output

    except Exception as e:
        return f"Error: Query chalate waqt masla aaya — {str(e)}"


# Test karne ke liye
if __name__ == "__main__":
    print(get_database_schema.invoke({}))
    print("\n--- Test Query ---\n")
    print(run_sql_query.invoke({"query": "SELECT * FROM students"}))
    print("\n--- Blocked Query Test ---\n")
    print(run_sql_query.invoke({"query": "DELETE FROM students"}))