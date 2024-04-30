import pandas as pd
from datetime import datetime
import re

# Helper functions
def parse_timestamp(ts):
    return datetime.strptime(ts, "%a %b %d %Y %H:%M:%S GMT-0500 (Central Daylight Time)")

def parse_interval_safe(interval, baseline):
    matches = re.findall(r'\[(.*?), (.*?)\]', interval)
    if matches:
        start_time, end_time = matches[0]
        start_dt = datetime.strptime(start_time, "%H:%M:%S")
        end_dt = datetime.strptime(end_time, "%H:%M:%S")
        start_seconds = int((datetime(baseline.year, baseline.month, baseline.day, start_dt.hour, start_dt.minute, start_dt.second) - baseline).total_seconds())
        end_seconds = int((datetime(baseline.year, baseline.month, baseline.day, end_dt.hour, end_dt.minute, end_dt.second) - baseline).total_seconds())
        return start_seconds, end_seconds
    else:
        return None

# Load and process CSV data
gcp1 = pd.read_csv('GCP1.csv')
gcp2 = pd.read_csv('GCP2.csv')
gcp1['TimeSeries'] = gcp1['TimeSeries ID'].apply(parse_timestamp)
gcp2['TimeSeries'] = gcp2['TimeSeries ID'].apply(parse_timestamp)
min_time = min(gcp1['TimeSeries'].min(), gcp2['TimeSeries'].min())

# Process interval data from text files
interval_types = ['Downsampling', 'Midblock', 'Upsampling']
files = ['downsampling.txt', 'midblock.txt', 'upsampling.txt']
interval_data = []
for interval_type, file_name in zip(interval_types, files):
    with open(file_name, 'r') as file:
        for interval in file.readlines():
            parsed = parse_interval_safe(interval, min_time)
            if parsed:
                start, end = parsed
                for second in range(start, end + 1):
                    interval_data.append((second, interval_type))

# Create interval DataFrame
interval_df = pd.DataFrame(interval_data, columns=['Seconds', 'Interval Type'])

# Load memory and CPU data
cpu_data = pd.read_csv('GCP_data.csv')

# Merge and finalize data
merged_data = pd.concat([cpu_data, interval_df])
merged_data = merged_data.sort_values('Seconds')
merged_data['Interval Type'] = merged_data['Interval Type'].fillna('No Interval')

columns_to_fill = ['CPU_utilization', 'Memory_utilization', 'network_received_bytes', 'Disk_IO', 'network_sent_bytes']
merged_data[columns_to_fill] = merged_data[columns_to_fill].interpolate()

merged_data.to_csv('GCP_data-2.csv', index=False)

print(merged_data.head())
