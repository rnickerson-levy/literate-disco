from datetime import datetime
from yyyymmdd import getYYYYMMDD

# def getYYYYMMDD(dateString):
#   for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y"):
#     try:
#       dt = datetime.strptime(dateString, fmt)
#       return f"{dt.year}{str(dt.month).rjust(2, "0")}{str(dt.day).rjust(2, "0")}"
#     except ValueError:
#       pass
#   raise ValueError('no valid date format found')

print(getYYYYMMDD("1/10/2024"))


# import os

# fp1 = os.getcwd()
# fp2 = os.path.realpath(__file__)
# print(fp1)
# print(fp2)

# import datetime
# import dateutil.parser # type: ignore

# d1 = dateutil.parser.parse("2024-11-14")
# d2 = dateutil.parser.parse("2024-11-15 09:58:53")

# print(d1)
# print(d2)

# 2024-11-15 09:58:53
# date_string = "2024-11-15 09:58:53"
# format_string = "%Y-%m-%d %H:%M:%S"
# datee = datetime.strptime(date_string, format_string)
# print(datee)
# print(datee.day)


# def isOnDate(targetDateString, datetimeString):
#   targetDate = "%m-%d-%Y"

# from line_items import LineItems

# lineItems = LineItems("./data/items.csv")
# lineItems.load()
# print(len(lineItems.getRawData()))
# lineItems.filter()
# print(len(lineItems.getFilteredData()))

# def isSameDay(date1, date2):
#   if not isinstance(date1, datetime.date) or not isinstance(date2, datetime.date):
#     raise ValueError("Value is not a date")
  
#   if not date1.month == date2.month:
#     return False
  
#   if not date1.day == date2.day:
#     return False
  
#   if not date1.year == date2.year:
#     return False
  
#   return True

# print(isSameDay(d1, d2))
