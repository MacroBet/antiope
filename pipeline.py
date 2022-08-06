from util.json_to_csv_chunk import json_to_csv
import threading
import time

all =["All_Amazon_Meta"]# ["AMAZON_FASHION_5","Gift_Cards_5","Patio_Lawn_and_Garden_5","All_Beauty_5","Grocery_and_Gourmet_Food_5","Pet_Supplies_5","Appliances_5","Home_and_Kitchen_5","Prime_Pantry_5","Arts_Crafts_and_Sewing_5","Industrial_and_Scientific_5","Software_5","Automotive_5","Kindle_Store_5","Sports_and_Outdoors_5","CDs_and_Vinyl_5","Luxury_Beauty_5","Tools_and_Home_Improvement_5","Cell_Phones_and_Accessories_5","Magazine_Subscriptions_5","Toys_and_Games_5","Clothing_Shoes_and_Jewelry_5","Movies_and_TV_5","Video_Games_5","Digital_Music_5","Musical_Instruments_5","reviews_Books_5","Electronics_5","Office_Products_5","reviews_Movies_and_TV_5"]
done = []#["AMAZON_FASHION_5","Home_and_Kitchen_5","Pet_Supplies_5","All_Beauty_5","Industrial_and_Scientific_5","Prime_Pantry_5","CDs_and_Vinyl_5","Kindle_Store_5","Software_5","Cell_Phones_and_Accessories_5","Luxury_Beauty_5","Sports_and_Outdoors_5","Clothing_Shoes_and_Jewelry_5","Magazine_Subscriptions_5","Tools_and_Home_Improvement_5","Digital_Music_5","Movies_and_TV_5","Toys_and_Games_5","Electronics_5","Musical_Instruments_5","Video_Games_5","Gift_Cards_5","Office_Products_5","reviews_Movies_and_TV_5","Grocery_and_Gourmet_Food_5","Patio_Lawn_and_Garden_5"]

dataSource=list(set(all) - set(done))


base_json_path= "/Volumes/Extreme SSD/data/json/"
base_csv_path= "/Volumes/Extreme SSD/data/csv/"
print(dataSource)



def execute_job(i,source):
    json_to_csv(base_json_path+source+".json",base_csv_path+source)
    print("done with {} ({}/{})\n\n".format(source,i+1,len(dataSource)))


start = time.perf_counter()
threads = []

for i,source in enumerate(dataSource):
    execute_job(i,source)
#     t = threading.Thread(target=execute_job, args=[i,source])
#     t.start()
#     threads.append(t)
# for thread in threads:
#     thread.join()
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds') 