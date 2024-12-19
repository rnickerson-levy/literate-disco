from datetime import datetime

def getYYYYMMDD(dateString):
  for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y"):
    try:
      dt = datetime.strptime(dateString, fmt)
      return f"{dt.year}{str(dt.month).rjust(2, "0")}{str(dt.day).rjust(2, "0")}"
    except ValueError:
      pass
  raise ValueError('no valid date format found')