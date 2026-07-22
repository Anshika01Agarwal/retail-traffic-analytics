import cv2
import time
from datetime import datetime
import pandas as pd
import psycopg2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Use a highly-optimized, fast YOLO model version built for continuous detection streams
print("🚀 Initializing computer vision networks...")
model = YOLO("yolo11n.pt") 
tracker = DeepSort(max_age=30, n_init=3)

# Dictionaries to capture entry times and temporary array buffers
customer_timers = {}
completed_sessions = []

def run_store_analytics(video_source=0):
    print("📹 Activating raw video stream target... Press 'q' to stop.")
    cap = cv2.VideoCapture(video_source)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Execute target class tracking inference via the active vision model 
        results = model(frame, verbose=False)
        detections = []
        
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            # Target human profiles (Class 0) with a confidence value barrier greater than 40%
            if cls == 0 and conf > 0.4:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))
                
        # Send raw vision metrics directly to deep sort tracking filters
        tracks = tracker.update_tracks(detections, frame=frame)
        current_epoch_time = time.time()
        active_ids = set()
        
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            active_ids.add(track_id)
            
            # Start timer calculation upon structural target entry detection
            if track_id not in customer_timers:
                customer_timers[track_id] = current_epoch_time
                
            # Render tracking bounding boxes and custom tags to verify visually
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Shopper ID: {track_id}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
            
        # Log absolute customer dwell metrics the moment a unique target leaves focus
        for departed_id in list(customer_timers.keys()):
            if departed_id not in active_ids:
                total_dwell_seconds = current_epoch_time - customer_timers[departed_id]
                completed_sessions.append({
                    "timestamp": datetime.now(),
                    "dwell_time": total_dwell_seconds
                })
                del customer_timers[departed_id]
                
        # Display the computational vision framework overlay output
        cv2.imshow("Active Retail Infrastructure Traffic Analytics Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    sync_live_telemetry_to_postgres()

def sync_live_telemetry_to_postgres():
    if not completed_sessions:
        print("⚠️ No unique user tracking sessions logged during this operational cycle.")
        return
        
    print("💾 Formatting tracking matrices for secure storage insertion...")
    df = pd.DataFrame(completed_sessions)
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.date
    
    # Calculate performance counts and summaries matching requirements
    summary = df.groupby(['date', 'hour']).agg(
        total_visitor_count=('dwell_time', 'count'),
        average_dwell_time_seconds=('dwell_time', 'mean')
    ).reset_index()
    
    try:
        connection = psycopg2.connect(
            host="localhost", database="retail_db", user="postgres", password="anshi@2004", port="5432"
        )
        cursor = connection.cursor()
        
        # Real-time UPSERT queries to block duplicates or key crashes
        upsert_query = """
            INSERT INTO hourly_analytics_summary (summary_date, hour_of_day, total_visitor_count, average_dwell_time_seconds)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (summary_date, hour_of_day) DO UPDATE SET
                total_visitor_count = hourly_analytics_summary.total_visitor_count + EXCLUDED.total_visitor_count,
                average_dwell_time_seconds = (hourly_analytics_summary.average_dwell_time_seconds + EXCLUDED.average_dwell_time_seconds) / 2;
        """
        
        for _, row in summary.iterrows():
            cursor.execute(upsert_query, (row['date'], row['hour'], int(row['total_visitor_count']), float(row['average_dwell_time_seconds'])))
            
        connection.commit()
        cursor.close()
        connection.close()
        print("📊 Telemetry updates saved to your PostgreSQL cluster successfully!")
    except Exception as db_sync_err:
        print(f"❌ Failed to stream active data metrics to database: {db_sync_err}")

if __name__ == "__main__":
    # Passing 0 opens your default laptop/PC webcam live feed space
    run_store_analytics(video_source=0)

