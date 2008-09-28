#Trung Tran cs188-iy 
import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    #TODO: your implemenstation here
    shopReturn=fruitShops[0];
    min =shopReturn.getPriceOfOrder(orderList) 
    for eachShop in fruitShops:
        CostTotalofEachShop=eachShop.getPriceOfOrder(orderList)
        if min>=CostTotalofEachShop:
            shopReturn=eachShop
            min=CostTotalofEachShop
    return shopReturn;
if __name__ == '__main__':
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print "For orders: ", orders, "best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, "best shop is", shopSmart(orders, shops).getName()
