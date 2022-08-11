from PAMI.frequentPattern.basic import FPGrowth 
from PAMI.frequentPattern.basic import Apriori 

print("leggo")
# fp = FPGrowth.FPGrowth('/Volumes/Extreme SSD/data/sequential_pattern_mining/Pet_Supplies_5.csv',50,';')
apriori = Apriori.Apriori('/Volumes/Extreme SSD/data/sequential_pattern_mining/Pet_Supplies_5.csv',50,';')
print("letto")


def func():
    try:
        fp = FPGrowth.FPGrowth('/Volumes/Extreme SSD/data/sequential_pattern_mining/Pet_Supplies_5.csv',50,';')
        fp.startMine()
        fp.savePatterns('frequentPatters_100.txt')
        df = fp.getPatternsAsDataFrame()
        print(df)
        print('Runtime: ' + str(fp.getRuntime()))
        print('Memory: ' + str(fp.getMemoryRSS()))

        # apriori.startMine()
        # apriori.savePatterns('frequentPatters_100.txt')
        # df = apriori.getPatternsAsDataFrame()
        # print(df)
        # print('Runtime: ' + str(apriori.getRuntime()))
        # print('Memory: ' + str(apriori.getMemoryRSS()))



    except: 
        print("error")

func()