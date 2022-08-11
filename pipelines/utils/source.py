import threading
import time


MAX_PART_SIZE= 30000
CATEGORIES =  ["AMAZON_FASHION_5","Gift_Cards_5","Patio_Lawn_and_Garden_5","All_Beauty_5","Grocery_and_Gourmet_Food_5","Pet_Supplies_5","Appliances_5","Home_and_Kitchen_5","Prime_Pantry_5","Arts_Crafts_and_Sewing_5","Industrial_and_Scientific_5","Software_5","Automotive_5","Kindle_Store_5","Sports_and_Outdoors_5","CDs_and_Vinyl_5","Luxury_Beauty_5","Tools_and_Home_Improvement_5","Cell_Phones_and_Accessories_5","Magazine_Subscriptions_5","Toys_and_Games_5","Clothing_Shoes_and_Jewelry_5","Movies_and_TV_5","Video_Games_5","Digital_Music_5","Musical_Instruments_5","reviews_Books_5","Electronics_5","Office_Products_5"]
META_PARTS = ['All_Amazon_Meta_part_19', 'All_Amazon_Meta_part_2', 'All_Amazon_Meta_part_17', 'All_Amazon_Meta_part_21', 'All_Amazon_Meta_part_24', 'All_Amazon_Meta_part_30', 'All_Amazon_Meta_part_29', 'All_Amazon_Meta_part_16', 'All_Amazon_Meta_part_14', 'All_Amazon_Meta_part_5', 'All_Amazon_Meta_part_15', 'All_Amazon_Meta_part_9', 'All_Amazon_Meta_part_12', 'All_Amazon_Meta_part_13', 'All_Amazon_Meta_part_28', 'All_Amazon_Meta_part_26', 'All_Amazon_Meta_part_8', 'All_Amazon_Meta_part_10', 'All_Amazon_Meta_part_22', 'All_Amazon_Meta_part_23', 'All_Amazon_Meta_part_0', 'All_Amazon_Meta_part_1', 'All_Amazon_Meta_part_7', 'All_Amazon_Meta_part_6', 'All_Amazon_Meta_part_20', 'All_Amazon_Meta_part_3', 'All_Amazon_Meta_part_25', 'All_Amazon_Meta_part_18', 'All_Amazon_Meta_part_4', 'All_Amazon_Meta_part_27', 'All_Amazon_Meta_part_11']
# File name sources

PATH_JSON="/Volumes/Extreme SSD/data/json/"
PATH_CSV="/Volumes/Extreme SSD/data/csv/"
PATH_MERGE= "/Volumes/Extreme SSD/data/csv/merged/"
PATH_SPM= "/Volumes/Extreme SSD/data/sequential_pattern_mining/data/"
PATH_TM= "/Volumes/Extreme SSD/data/text_mining/"
PATH_SPM_OUT= "/Volumes/Extreme SSD/data/sequential_pattern_mining/out/"
PATH_SPM_OUT_100= "/Volumes/Extreme SSD/data/sequential_pattern_mining/support 100/"
PATH_CLEAR="/Volumes/Extreme SSD/data/csv/cleared/"
PATH_OUT="/Volumes/Extreme SSD/data/output/"
REVIEWS_TYPE={"asin": "string","overall":int,"reviewerID": "string","reviewerName": "string","reviewText": "string","summary": "string","unixReviewTime": int,"verified":bool}
METADATA_TYPE= {'asin':"string", 'image':"string", 'overall':"string", 'reviewText':"string", 'reviewTime':"string", 'reviewerID':"string",'reviewerName':"string", 'style':"string", 'summary':"string", 'unixReviewTime':"string", 'verified':"string",'vote':"string"}
# Index(['asin',sis 'image', 'overall', 'reviewText', 'reviewTime', 'reviewerID','reviewerName', 'style', 'summary', 'unixReviewTime', 'verified','vote'],



def thread_starter(threads,thread_max=16):
    OBSERVED_THREAD_COUNT = 4
    avg_execution_time= 0
    for i,thread in enumerate(threads):
        if(i<OBSERVED_THREAD_COUNT):
            start_time=time.time()
            thread.start()
            thread.join()
            avg_execution_time+=(time.time() - start_time)/OBSERVED_THREAD_COUNT
            print("execution time {}".format(avg_execution_time))
        else:
            thread.start()
            time.sleep(avg_execution_time/thread_max)
    for thread in threads:
        thread.join()
    print("done with all threads")


def thread_dispatcher(dataSource,target,thread_max=16):
    threads = []
    for i,source in enumerate(dataSource):
        t = threading.Thread(target=target, args=[i,source])
        threads.append(t)
    thread_starter(threads,thread_max)
  

def job_dispatch_in_dataSource(dataSource,target,thread=True,thread_max=20):
    start = time.time()
    if(thread):
        thread_dispatcher(dataSource,target,thread_max)
    else:
        for i,source in enumerate(dataSource):
            target(i,source)
    end = time.time()
    print( "All done in {}".format(end - start))
