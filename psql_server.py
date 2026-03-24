# pg_server.py
from fastmcp import FastMCP
import psycopg2
import os

# Initialize FastMCP
mcp = FastMCP("PostgresServer")


# Database configuration (use environment variables for security)
DB_CONFIG = {
    "host": "<host_name>",
    "database": "<db_name>",
    "user": "<username>",
    "password": "<password>",
    "port": 5432
}

@mcp.tool()
def execute_pg_query(sql: str) -> str:
    """
    Executes a SQL query against the PostgreSQL database.
    Use this for data analysis, fetching user records, or checking system status.
    """
    try:
        # Use psycopg2 to connect and execute
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                # Fetch results if it's a SELECT query
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    results = cur.fetchall()
                    return str([dict(zip(columns, row)) for row in results])
                conn.commit()
                return "Command executed successfully."
    except Exception as e:
        return f"PostgreSQL Error: {str(e)}"

if __name__ == "__main__":
    # Run using stdio transport for local agent communication
    mcp.run()
