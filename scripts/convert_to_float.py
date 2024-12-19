def convertToFloat(value):
  valueString = str(value).replace("$", "").replace(",", "")
  return float(valueString)
