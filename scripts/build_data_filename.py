from typing import Optional

def buildDataFilename(filename: str, datestamp: str, timestamp: Optional[str] = None):
  name = filename
  name = name.replace("[[YYYYMMDD]]", datestamp)
  name = name.replace("[[yyyymmdd]]", datestamp)
  if timestamp is not None:
    name = name.replace("[[TS]]", timestamp)
    name = name.replace("[[ts]]", timestamp)
  
  return name
