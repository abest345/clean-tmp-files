import os 
import datetime
import glob
import boto3 #pip install boto3 - is required if not already installed - this is what aws requires

#Logging is done via crontab

target_dirs = ['/tmp/', '/home/tmp/'] # Local directories
my_s3_bucket = 'mybucket' # Your AWS S3 bucket name
s3_file_location = 'tmp-files/' # Location in the S3 bucket to move files to
file_expiry_age = -1095 # How many days old before file force upload and delete (3 years)

s3 = boto3.resource('s3') # Setting up s3 resource
today = datetime.datetime.today()# Gets current time

# Counters for output
json_files = 0
processed_files = 0
broken_files = 0

for target_path in target_dirs:
    print('Searching --> ' + target_path)
    # Changing path to current path (same as cd command)
    os.chdir(target_path) 
    # Going through the entire directory tree
    for root,directories,files in os.walk(target_path,topdown=False): 
        for name in files:
            # Main loop for trying to upload then delete the file
            try:
                file_name = os.path.join(root, name)
                time = os.stat(file_name)[8]
                filetime = datetime.datetime.fromtimestamp(time) - today # Getting the last modified time
                # Checking if file is more than X days old
                if filetime.days <= file_expiry_age:
                    # Skip json files
                    if 'json' in file_name:
                        json_files +=1
                        print('Skipped json --> ' + file_name)
                        break
                    # Upload it to s3
                    s3.Bucket(my_s3_bucket).upload_file(file_name, s3_file_location) # Source, dest
                    # Delete it now that its uploaded
                    os.remove(file_name)
                    processed_files +=1
                    print('Processed --> ' + file_name)
            except Exception as error: # If it doesnt work for whatever reason just skip it (will happen for symlinks and unexpected chars)
                print(error)
                broken_files +=1

print('Processed Files: ', processed_files)
print('Skipped Files: ', json_files)
print('Broken Files:', broken_files)
