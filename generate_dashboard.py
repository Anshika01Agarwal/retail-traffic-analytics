import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress the pandas UserWarning about SQLAlchemy to keep your console completely clean
warnings.filterwarnings("ignore", category=UserWarning)

def generate_premium_retail_cockpit():
    print("🔄 Connecting to PostgreSQL cluster to build production-grade UI cockpit...")
    try:
        connection = psycopg2.connect(
            host="localhost", database="retail_db", user="postgres", password="anshi@2004", port="5432"
        )
        query = "SELECT * FROM hourly_analytics_summary ORDER BY summary_date, hour_of_day;"
        df = pd.read_sql_query(query, connection)
        connection.close()
        
        if df.empty:
            print("⚠️ Relational metrics are missing. Seed records before running visual builds.")
            return

        print("🎨 Formatting premium dark-mode interface skin layouts...")
        
        # Calculate key high-level operational summary statistics for top KPI blocks
        total_tracked_footfall = int(df['total_visitor_count'].sum())
        peak_hour_row = df.loc[df['total_visitor_count'].idxmax()]
        peak_hour_stamp = f"{int(peak_hour_row['hour_of_day'])}:00"
        overall_avg_dwell_mins = float((df['average_dwell_time_seconds'].mean()) / 60.0)

        # Apply an elegant cyber-dark aesthetic foundation template context
        plt.style.use('dark_background')
        sns.set_theme(style="dark", palette="pastel")
        
        # Build an asymmetric 3-axis canvas layout matrix window container
        fig = plt.figure(figsize=(20, 10), facecolor='#0d1117')
        gs = fig.add_gridspec(2, 2, height_ratios=[0.25, 1], hspace=0.35, wspace=0.25)
        
        # Adjust parent spacing margins perfectly to prevent text truncation bugs
        plt.subplots_adjust(left=0.06, right=0.94, top=0.88, bottom=0.10)
        
        fig.suptitle("RETAIL MANAGEMENT TRAFFIC INTERACTIVE COCKPIT", 
                     fontsize=20, fontweight="bold", color="#ffffff", y=0.96)

        # -----------------------------------------------------------------
        # TOP CONTAINER GRID: EXECUTIVE BANNER CARD KPI METRICS 
        # -----------------------------------------------------------------
        ax_kpi = fig.add_subplot(gs[0, :])
        ax_kpi.axis('off')  # Strip out typical graph box borders to treat as a text tile banner
        ax_kpi.set_facecolor('#161b22')
        
        # Draw clean background rectangular dashboard boxes for our stats cards using safe parameters
        for x_coord in [0.02, 0.36, 0.70]:
            rect = plt.Rectangle((x_coord, 0.05), 0.28, 0.90, facecolor='#1f242c', 
                                 edgecolor='#30363d', transform=ax_kpi.transAxes, clip_on=False, lw=1.5)
            ax_kpi.add_patch(rect)

        # Inject Text Content dynamically into Box 1: Total Footfall
        ax_kpi.text(0.16, 0.65, "TOTAL SHOPPERS ACCOUNTED", color="#8b949e", fontsize=10, fontweight="bold", ha="center", transform=ax_kpi.transAxes)
        ax_kpi.text(0.16, 0.20, f"{total_tracked_footfall:,}", color="#58a6ff", fontsize=24, fontweight="bold", ha="center", transform=ax_kpi.transAxes)

        # Inject Text Content dynamically into Box 2: Peak Hours
        ax_kpi.text(0.50, 0.65, "MAXIMUM DAILY SURGE WINDOW", color="#8b949e", fontsize=10, fontweight="bold", ha="center", transform=ax_kpi.transAxes)
        ax_kpi.text(0.50, 0.20, f"{peak_hour_stamp}", color="#ff7b72", fontsize=24, fontweight="bold", ha="center", transform=ax_kpi.transAxes)

        # Inject Text Content dynamically into Box 3: Dwell Matrix
        ax_kpi.text(0.84, 0.65, "OVERALL ACCUMULATED ENGAGEMENT", color="#8b949e", fontsize=10, fontweight="bold", ha="center", transform=ax_kpi.transAxes)
        ax_kpi.text(0.84, 0.20, f"{overall_avg_dwell_mins:.2f} Mins", color="#56d364", fontsize=24, fontweight="bold", ha="center", transform=ax_kpi.transAxes)

        # -----------------------------------------------------------------
        # BOTTOM LEFT GRID: TEMPORAL CROWD DENSITY PEAK LINE GRAPH
        # -----------------------------------------------------------------
        ax_line = fig.add_subplot(gs[1, 0], facecolor='#161b22')
        hourly_traffic = df.groupby('hour_of_day')['total_visitor_count'].mean().reset_index()
        
        # Cyberpunk neon line charting with drop shading effect paths
        sns.lineplot(ax=ax_line, data=hourly_traffic, x="hour_of_day", y="total_visitor_count",
                     marker="o", color="#ff4560", linewidth=3.5, markersize=9, label='Footfall Density')
        ax_line.fill_between(hourly_traffic["hour_of_day"], hourly_traffic["total_visitor_count"], color="#ff4560", alpha=0.12)
        
        ax_line.set_title("STORE PEAK TRAFFIC TIMELINE (HOURLY AVERAGE)", fontsize=12, fontweight="bold", color="#ffffff", pad=15)
        ax_line.set_xlabel("Operational Workday Hours (24H Scale)", fontsize=10, color="#8b949e", labelpad=8)
        ax_line.set_ylabel("Mean Unique Customers Tracked", fontsize=10, color="#8b949e", labelpad=8)
        ax_line.set_xticks(range(8, 23))
        ax_line.grid(True, color="#30363d", linestyle="--", linewidth=0.5)
        ax_line.tick_params(colors='#8b949e', labelsize=9)
        ax_line.legend(facecolor='#1f242c', edgecolor='#30363d', loc='upper left')

        # -----------------------------------------------------------------
        # BOTTOM RIGHT GRID: ZONE AISLE ENGAGEMENT GRADIENT BAR CHART
        # -----------------------------------------------------------------
        ax_bar = fig.add_subplot(gs[1, 1], facecolor='#161b22')
        hourly_dwell = df.groupby('hour_of_day')['average_dwell_time_seconds'].mean().reset_index()
        hourly_dwell['average_dwell_minutes'] = hourly_dwell['average_dwell_time_seconds'] / 60.0

        # Implement smooth glowing neon gradient fill transitions via the cool 'plasma' sequence
        sns.barplot(ax=ax_bar, data=hourly_dwell, x="hour_of_day", y="average_dwell_minutes",
                    hue="hour_of_day", palette="plasma", legend=False, edgecolor='#30363d', linewidth=0.8)
        
        ax_bar.set_title("AVERAGE CUSTOMER DWELL TIME ENGAGEMENT TREND", fontsize=12, fontweight="bold", color="#ffffff", pad=15)
        ax_bar.set_xlabel("Operational Workday Hours (24H Scale)", fontsize=10, color="#8b949e", labelpad=8)
        ax_bar.set_ylabel("Dwell Metrics (Active Inside Store Minutes)", fontsize=10, color="#8b949e", labelpad=8)
        ax_bar.grid(True, color="#30363d", axis='y', linestyle="--", linewidth=0.5)
        ax_bar.tick_params(colors='#8b949e', labelsize=9)

        # -----------------------------------------------------------------
        # OUTPUT EXPORT AND RENDERING HANDLERS
        # -----------------------------------------------------------------
        output_asset_path = "retail_analytics_report.png"
        plt.savefig(output_asset_path, dpi=300, facecolor='#0d1117', edgecolor='none')
        print(f"✅ Success! Luxury visual dashboard reporting matrix exported to '{output_asset_path}'")
        
        plt.show()

    except Exception as dashboard_crash_error:
        print(f"❌ Failed to construct advanced reporting cockpit layer: {dashboard_crash_error}")

if __name__ == "__main__":
    generate_premium_retail_cockpit()
