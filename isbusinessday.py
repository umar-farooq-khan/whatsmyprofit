# Test if a date is a business day
from bdateutil import isbday
from datetime import date
isbday(date(2014, 1, 1))

# Date parameters are no longer limited to datetime objects
isbday("2020-05-29")
xx=isbday("1/1/2014")
type(xx)
isbday(1388577600)  # Unix timestamp = Jan 1, 2014
