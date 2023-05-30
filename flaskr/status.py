from datetime import datetime

now = datetime.now()

current_minutes = int(now.strftime("%M"))

status = ""

if current_minutes % 5 == 0:
    status = "Add Substrate"
elif current_minutes % 3 == 0:
    status = "Add Water"
else:
    status = "All Good"
