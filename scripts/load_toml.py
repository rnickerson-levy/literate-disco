import tomllib
  
def loadToml(filepath: str):
  with open(filepath, "rb") as f:
    contents = tomllib.load(f)
    
  return contents