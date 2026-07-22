import psycopg2
import random
from datetime import datetime, timedelta

def generate_historical_metrics():
    print("⏳ Connecting to 'retail_db' to feed 30 days of mock tracking analytics...")
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="retail_db",
            user="postgres",
            password="anshi@2004",
            port="5432"
        )
        cursor = connection.cursor()
        
        # Reset the table first to clear out any accidental duplicate testing rows
        cursor.execute("TRUNCATE TABLE hourly_analytics_summary;")
        
        start_date = datetime.now() - timedelta(days=30)
        
        # Loop through each day of the past month
        for day_offset in range(31):
            current_date = (start_date + timedelta(days=day_offset)).date()
            
            # Loop through realistic retail store business hours (8 AM to 10 PM)
            for hour in range(8, 23):
                # Build standard store traffic flow: simulate busy peaks around lunch and evening
                if 12 <= hour <= 14 or 18 <= hour <= 20:
                    visitor_count = random.randint(55, 95)
                    avg_dwell = random.uniform(700.0, 1400.0) # Shoppers stay longer (11-23 mins)
                else:
                    visitor_count = random.randint(12, 38)
                    avg_dwell = random.uniform(180.0, 550.0)  # Off-peak quick visits (3-9 mins)
                
                # Insert calculated matrix entry safely
                cursor.execute("""
                    INSERT INTO hourly_analytics_summary (summary_date, hour_of_day, total_visitor_count, average_dwell_time_seconds)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (summary_date, hour_of_day) DO NOTHING;
                """, (current_date, hour, visitor_count, round(avg_dwell, 2)))
                
        connection.commit()
        cursor.close()
        connection.close()
        print("📊 Success! Your PostgreSQL analytics table is populated with 30 days of data.")
        
    except Exception as error:
        print(f"❌ Data generation failed: {error}")

if __name__ == "__main__":
    generate_historical_metrics()
