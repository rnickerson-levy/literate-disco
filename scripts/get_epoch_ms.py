import time
from typing import Union

def getEpochMS(t: Union[float, int, None] = None):
  ts = t
  if ts is None:
    ts = time.time()
  
  return int(ts * 1000)