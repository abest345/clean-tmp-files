Uploads and Deletes files older than X years in the specified locations. (Excluding .json and symlink files)

Can be run manually using:
nice -5 python run.py

nice -5: Is required as script is IO intensive if there are significant volume files to proccess.