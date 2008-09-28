import shop
name = 'CS 188'
fruitPrices = {'apple':2.00, 'orange': 1.50, 'pear': 1.75}
myFruitShop = shop.FruitShop(name, fruitPrices)
myFruitShop.state='jjhg';
print myFruitShop.getCostPerPound('apple')

otherName = 'CS 170'
otherFruitPrices = {'kiwi':1.00, 'bannana': 1.50, 'peach': 2.75}
otherFruitShop = shop.FruitShop(otherName, otherFruitPrices)
print otherFruitShop.getCostPerPound('bannana')