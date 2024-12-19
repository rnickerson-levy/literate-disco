import datetime

def isSameDay(date1, date2):
  if not isinstance(date1, datetime.date) or not isinstance(date2, datetime.date):
    raise ValueError("Value is not a date")
  
  if not date1.month == date2.month:
    return False
  
  if not date1.day == date2.day:
    return False
  
  if not date1.year == date2.year:
    return False
  
  return True