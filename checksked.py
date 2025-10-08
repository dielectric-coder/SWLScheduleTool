#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime, timezone

def main():
    # Configuration
    SCHED_DIR = "/home/mikel/Documents/Radio/sw-schedules"
    
    # Check if frequency argument is provided
    if len(sys.argv) < 2:
        print("Usage: checksked.py <frequency_in_kHz>")
        sys.exit(1)
    
    frequency = sys.argv[1]
    
    # Get current UTC time in HHMM format
    current_utc = datetime.now(timezone.utc)
    current_time = int(current_utc.strftime("%H%M"))
    
    # Clear screen
    os.system('clear')
    
    # Display header
    print(f"Stations programmées à la fréquence {frequency} kHz")
    print(f"Pour l'heure UTC actuelle: {current_utc.strftime('%H:%M')}")
    print()
    
    # Process the CSV file
    csv_file = os.path.join(SCHED_DIR, "sked-current.csv")
    
    # ANSI color codes for highlighting
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    try:
        with open(csv_file, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                # Check if frequency matches (search in first column)
                if len(row) > 0 and frequency in row[0]:
                    # Extract fields (adjust indices based on CSV structure)
                    freq = row[0] if len(row) > 0 else ""
                    time_range = row[1] if len(row) > 1 else ""
                    country = row[3] if len(row) > 3 else ""
                    station = row[4] if len(row) > 4 else ""
                    language = row[5] if len(row) > 5 else ""
                    target = row[6] if len(row) > 6 else ""
                    site = row[7] if len(row) > 7 else ""
                    
                    # Use country code with '/' prefix if site is empty
                    if not site or site.strip() == "":
                        site = f"/{country}"
                    
                    # Calculate duration and check if currently broadcasting
                    duration = 0
                    is_active = False
                    
                    if '-' in time_range:
                        try:
                            start, end = time_range.split('-')
                            start_time = int(start)
                            end_time = int(end)
                            duration = end_time - start_time
                            
                            # Handle broadcasts that cross midnight
                            if duration < 0:
                                duration += 2400
                                # For broadcasts crossing midnight, check if current time is after start OR before end
                                is_active = (current_time >= start_time) or (current_time < end_time)
                            else:
                                # Normal broadcast within same day
                                is_active = (start_time <= current_time < end_time)
                                
                        except (ValueError, IndexError):
                            duration = 0
                    
                    # Format output line
                    output_line = (f"{freq} kHz {time_range} UTC "
                                  f"Pays: {country:>3} "
                                  f"Site: {site:<6} "
                                  f"Station: {station:<24} "
                                  f"Langue: {language:<3} "
                                  f"Cible: {target:>4} "
                                  f"{duration:04d}")
                    
                    # Highlight if currently active
                    if is_active:
                        print(f"{GREEN}{output_line} ◄ ON AIR{RESET}")
                    else:
                        print(output_line)
    
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()