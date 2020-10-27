from datetime import date

import datetime
from datetime import datetime

date_time_str = '09/02/20 01:55:19'

date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)
#weekno = date.weekday())

if date_time_obj.weekday()<5:
    print("Weekday")
else:
    print ("Weekend")