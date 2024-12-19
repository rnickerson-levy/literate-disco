SUBCON_FOOD_LABEL = "SUB FOOD".lower()
SUBCON_BEV_LABEL = "SUB BEVERAGE".lower()
ALCOHOL_MENU_CATEGORIES = [
  "PKG BEER".lower(),
  "LIQUOR".lower(),
]

def getSubconFoodSales(amount, menuCategory):
  return amount if menuCategory.lower() == SUBCON_FOOD_LABEL else 0

def getSubconBevSales(amount, menuCategory):
  return amount if menuCategory.lower() == SUBCON_BEV_LABEL else 0

def getAlcoholSales(amount, menuCategory):
  return amount if menuCategory.lower() in ALCOHOL_MENU_CATEGORIES else 0

def getHouseSales(amount, menuCategory):
  if menuCategory.lower() in ALCOHOL_MENU_CATEGORIES:
    return 0
  
  if menuCategory.lower() == SUBCON_FOOD_LABEL:
    return 0
  
  if menuCategory.lower() == SUBCON_BEV_LABEL:
    return 0
  
  return amount
