#!/usr/bin/env python3
# File: /home/mikel/GitSpace/swl-tools/updsked.py

import sys
import os
import subprocess
import urllib.request
import shutil

def main():
    # Configuration
    SCHED_DIR = "/home/mikel/Documents/Radio/sw-schedules"
    BASE_URL = "http://eibispace.de/dx"
    
    # Check if schedule period argument is provided
    if len(sys.argv) < 2:
        print("Usage: updsked.py <schedule_period>")
        print("Example: updsked.py A23")
        sys.exit(1)
    
    period = sys.argv[1]
    
    # Change to schedule directory
    original_dir = os.getcwd()
    os.chdir(SCHED_DIR)
    
    print()
    print(f"updating schedule {period}")
    print()
    
    # List of files to download and convert
    files_to_process = [
        (f"sked-{period}.csv", "sked-current.csv"),
        (f"freq-{period}.txt", "freq-current.dat"),
        (f"bc-{period}.txt", "bc-current.dat"),
    ]
    
    # Download and convert each file
    for source_file, target_file in files_to_process:
        source_path = os.path.join(SCHED_DIR, source_file)
        target_path = os.path.join(SCHED_DIR, target_file)
        url = f"{BASE_URL}/{source_file}"
        
        # Remove old file if exists
        if os.path.exists(source_path):
            os.remove(source_path)
        
        # Download file
        try:
            print(f"Downloading {source_file}...")
            urllib.request.urlretrieve(url, source_path)
            
            # Convert encoding from ISO-8859-1 to UTF-8
            print(f"Converting {source_file} to UTF-8...")
            with open(source_path, 'r', encoding='iso-8859-1') as f_in:
                content = f_in.read()
            with open(target_path, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
                
        except Exception as e:
            print(f"Error processing {source_file}: {e}")
    
    # Download and convert README
    readme_source = "README.TXT"
    readme_target = "README-current.TXT"
    readme_url = f"{BASE_URL}/{readme_source}"
    
    try:
        print(f"Downloading {readme_source}...")
        urllib.request.urlretrieve(readme_url, readme_source)
        
        print(f"Converting {readme_source} to UTF-8...")
        with open(readme_source, 'r', encoding='iso-8859-1') as f_in:
            content = f_in.read()
        with open(readme_target, 'w', encoding='utf-8') as f_out:
            f_out.write(content)
            
    except Exception as e:
        print(f"Error processing {readme_source}: {e}")
    
    # Display completion message
    try:
        # Try to use cowsay and lolcat if available
        cowsay_process = subprocess.Popen(['cowsay', 'All done!'], 
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL)
        subprocess.run(['lolcat'], 
                      stdin=cowsay_process.stdout,
                      stderr=subprocess.DEVNULL)
        cowsay_process.wait()
    except FileNotFoundError:
        # Fallback if cowsay/lolcat not available
        print("\n✓ All done!")
    
    # Return to original directory
    os.chdir(original_dir)

if __name__ == "__main__":
    main()