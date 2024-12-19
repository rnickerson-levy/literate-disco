from datetime import datetime

class Logger:
  def __init__(self, ts = True):
    self.ts = ts
    
  def p(self, *messages):
    timestamp = ""
    
    if self.ts:
      timestamp = f"[{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}] "
      
    print(f"{timestamp}{" ".join(str(s) for s in messages)}")
  