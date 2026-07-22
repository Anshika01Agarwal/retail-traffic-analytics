import psycopg2
import sys

def create_retail_database_table():
    print("🔄 Attempting to connect to PostgreSQL server...")
    try:
        # Explicit configuration parameters to safely bypass string errors
        connection = psycopg2.connect(
            host="localhost",
            database="retail_db",
            user="postgres",
            password="anshi@2004",
            port="5432"
        )
        cursor = connection.cursor()
        
        # Build Table 2 SQL statement directly from your specifications
        table_creation_query = """
        CREATE TABLE IF NOT EXISTS hourly_analytics_summary (
            summary_date DATE NOT NULL,
            hour_of_day INT NOT NULL,
            total_visitor_count INT DEFAULT 0,
            average_dwell_time_seconds REAL DEFAULT 0.0,
            PRIMARY KEY (summary_date, hour_of_day)
        );
        """
        
        cursor.execute(table_creation_query)
        connection.commit()
        
        cursor.close()
        connection.close()
        print("✅ Success! PostgreSQL table 'hourly_analytics_summary' is fully built!")
        
    except psycopg2.OperationalError as db_err:
        print(f"❌ Connection Failed! Verify pgAdmin is running and 'retail_db' exists.")
        print(f"Details: {db_err}")
    except Exception as general_err:
        print(f"❌ Unexpected script error: {general_err}")

if __name__ == "__main__":
    create_retail_database_table()
