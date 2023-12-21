import os
import datetime

path = 'C:\\Users\\Jonas\\Desktop\\testeren\\'
status = os.stat(path).st_mtime


timestamp = status
readable_time = datetime.datetime.fromtimestamp(timestamp)
formatted_time = readable_time.strftime("%d-%m-%Y %H:%M")
print(f"Last modification: {formatted_time}")