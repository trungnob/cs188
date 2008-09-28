def static_num2():
    static_num2.x+=1;
    return static_num2.x
    

static_num2.x=0

for i in range(0,10) :
    print static_num2()