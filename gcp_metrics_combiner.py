#CSV clean
import pandas as pd
from datetime import datetime
import re

# Function to parse timestamps from CSV files
def parse_timestamp(ts):
    return datetime.strptime(ts, "%a %b %d %Y %H:%M:%S GMT-0500 (Central Daylight Time)")

# Function to safely parse time intervals from text files
def parse_interval_safe(interval, baseline):
    matches = re.findall(r'\[(.*?), (.*?)\]', interval)
    if matches:
        start_time, end_time = matches[0]
        start_dt = datetime.strptime(start_time, "%H:%M:%S")
        end_dt = datetime.strptime(end_time, "%H:%M:%S")
        start_seconds = (datetime(baseline.year, baseline.month, baseline.day, start_dt.hour, start_dt.minute, start_dt.second) - baseline).total_seconds()
        end_seconds = (datetime(baseline.year, baseline.month, baseline.day, end_dt.hour, end_dt.minute, end_dt.second) - baseline).total_seconds()
        return start_seconds, end_seconds
    else:
        return None

# Load CSV files
gcp1 = pd.read_csv('GCP1.csv')
gcp2 = pd.read_csv('GCP2.csv')
gcp3 = pd.read_csv('GCP3.csv')
gcp4 = pd.read_csv('GCP4.csv')
gcp5 = pd.read_csv('GCP5.csv')

# Parse timestamps
gcp1['TimeSeries'] = gcp1['TimeSeries ID'].apply(parse_timestamp)
gcp2['TimeSeries'] = gcp2['TimeSeries ID'].apply(parse_timestamp)
gcp3['TimeSeries'] = gcp3['TimeSeries ID'].apply(parse_timestamp)
gcp4['TimeSeries'] = gcp4['TimeSeries ID'].apply(parse_timestamp)
gcp5['TimeSeries'] = gcp5['TimeSeries ID'].apply(parse_timestamp)
min_time = min(gcp1['TimeSeries'].min(), gcp2['TimeSeries'].min())

# Adjust time to start from 0 seconds
gcp1['Seconds'] = (gcp1['TimeSeries'] - min_time).dt.total_seconds()
gcp2['Seconds'] = (gcp2['TimeSeries'] - min_time).dt.total_seconds()
gcp3['Seconds'] = (gcp3['TimeSeries'] - min_time).dt.total_seconds()
gcp4['Seconds'] = (gcp4['TimeSeries'] - min_time).dt.total_seconds()
gcp5['Seconds'] = (gcp5['TimeSeries'] - min_time).dt.total_seconds()


# Merge
merged_data = pd.merge(gcp1[['Seconds', 'CPU_utilization']], gcp2[['Seconds', 'Memory_utilization']], on='Seconds', how='outer')
merged_data = pd.merge(merged_data, gcp3[['Seconds', 'Disk_IO']], on='Seconds', how='outer')
merged_data = pd.merge(merged_data, gcp4[['Seconds', 'network_received_bytes']], on='Seconds', how='outer')
combined_data = pd.merge(merged_data, gcp5[['Seconds', 'network_sent_bytes']], on='Seconds', how='outer')

combined_data.to_csv('GCP_data.csv', index=False)

