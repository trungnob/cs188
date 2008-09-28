fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75, 
              'limes':0.75,'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
            
    Returns cost of order
    """ 
    total=0.0
    for FruitwithPrice in orderList:
        if FruitwithPrice.__class__==tuple : 
            f,p=FruitwithPrice
            if f in fruitPrices :
                total+=fruitPrices[f]*p;
            else :
                print("Sorry we don't have %s") %(f)
                return None 
        else:
             print "Don't understand what is %s." %(FruitwithPrice)
             return None    
    return total
    
if __name__ == '__main__':
    orderList = [ ('apples', 2.0), ('pears',3.0), ('limes',4.0)]
    print buyLotsOfFruit(orderList)