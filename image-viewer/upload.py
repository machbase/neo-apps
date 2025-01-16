import os
import glob
from datetime import datetime
import requests
import time

def datetime_to_epoch(date_str, time_str):
    """Convert date and time strings to epoch timestamp"""
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    hour = time_str[:2]
    minute = time_str[2:4]
    second = time_str[4:6]

    dt = datetime.strptime(f"{year}-{month}-{day} {hour}:{minute}:{second}",
                          "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())

def process_images():
    """Process all madrid_*.jpg files in the org-image directory"""
    # Save current working directory
    current_dir = os.getcwd()

    # Match file pattern
    pattern = os.path.join('org-image', 'madrid_*.jpg')
    image_files = glob.glob(pattern)

    for file_path in sorted(image_files):
        # Extract date and time from filename
        filename = os.path.basename(file_path)
        date_time_str = filename.replace('madrid_', '').replace('.jpg', '')
        date_str = date_time_str[:8]      # YYYYMMDD
        time_str = date_time_str[9:15]    # HHMMSS

        # Convert to epoch time
        epoch_time = datetime_to_epoch(date_str, time_str)

        # Prepare multipart form data
        store_dir = f'{current_dir}/uploaded'

        # Open file in binary mode
        with open(file_path, 'rb') as image_file:
            # Prepare multipart form-data
            files = {
                'NAME': ('', 'camera1'),
                'TIME': ('', str(epoch_time * 1000000000)),
                'VALUE': ('', '0'),
                'IMAGE': (
                    filename,           # filename
                    image_file,         # file object
                    'image/jpeg',       # content-type
                    {'X-Store-Dir': store_dir}  # custom headers
                )
            }

            try:
                # Send POST request with multipart form-data
                response = requests.post(
                    'http://127.0.0.1:5654/db/write/complex',
                    files=files
                )

                # Check response
                if response.status_code == 200:
                    print(f"Successfully processed: {filename}")
                    print(f"Epoch time: {epoch_time}")
                else:
                    print(f"Error processing {filename}. Status code: {response.status_code}")
                    print(f"Response: {response.text}")

                print("-" * 50)

            except Exception as e:
                print(f"Exception while processing {filename}: {str(e)}")

        # Add delay between requests to prevent overload
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        process_images()
        print("Processing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
