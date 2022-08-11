from utils.json_to_csv_chunk import json_to_csv
import threading
from utils.source import CATEGORIES,MAX_PART_SIZE,job_dispatch_in_dataSource,execute_job,PATH_JSON,PATH_CSV,PATH_OUT,PATH_CLEAR,METADATA_TYPE,REVIEWS_TYPE,PATH_MERGE,META_PARTS,PATH_SPM
import pandas as pd
import numpy as np
import time

all = CATEGORIES
done = []
dataSource=list(set(all) - set(done))
print(dataSource)

def pipeline():
    # 1. Convert CSV into JSON for better operability
    job_dispatch_in_dataSource(dataSource,job_json_to_csv,False)
    
    # 2. Quick Preliminary Analysis
    # 2.1 Rows analysis 
    # we want to discover if there are duplicated rows in different categories
    extract_asin_from_csv()
    merge_csv_files()
    find_duplicates()
    # 61913 rows are duplicated, so we need to merge the reviews of the duplicated rows
    find_duplicated_products_in_all_sources()
    
    # 2.2 Column analysis
    # we need to find the missing columns and fix them
    job_dispatch_in_dataSource(dataSource,job_print_column,True)
    count_missing_values("Patio_Lawn_and_Garden_5")
    # During the test we noticed that files are too big and we need to split them into smaller files, to prevent a memory overload and allow to run on multiple threads. 
    # Moreover the subdiviosion of big files in smaller files allow us to process them in parallel, which is much faster than processing them one by one.
    # To validate this concept we tested how much times the program takes to load 8 parts of the metadata file both in parallel and one by one.
    # The results are: 170.8 seconds for parallel loading and 312.2 seconds for one by one loading. The conclusion is that the parallel loading is much faster than the one by one loading.

    # 2.2.1 remove unuseful columns
    # image, overall, style ,vote 
    # {'Size:': ' 3.5 oz.'}
    # 'Size:': ' 3.5 oz.'}
    # vote because has a lot of missing values about 80% in sample of Luxury_Beauty_5.csv
    job_dispatch_in_dataSource(dataSource,job_drop_unuseful_column)

    # now that unusued columns and duplicated rows are removed we can merge the cleaned csv files but
    # before we need to check if there are other missing values.
    job_dispatch_in_dataSource(dataSource,job_check_for_missing_values,True)

    # as expected some missing values have been found in the fields summary and reviewText. This texts will be set to empty strings and ignored in the text mining process.
    # luckily there aren't any missing values in the fields overall, asin and reviewerID.
    # we can now merge all files togheter and make parts as we did before for the metadata file.

    job_dispatch_in_dataSource(dataSource,job_merge_csv_files)
    

###############################
##          JOBS            ###
###############################

def job_json_to_csv(i,source):
    json_to_csv(PATH_JSON+source+".json",PATH_CSV+source)
    print("done with {} ({}/{})\n\n".format(source,i+1,len(dataSource)))
    
def extract_asin_from_csv():
    for i,source in enumerate(dataSource):
        print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
        df = pd.read_csv(PATH_CSV+source+".csv")
        asin = df.loc[:, ['asin']]
        unique_asin = asin.drop_duplicates()
        unique_asin.to_csv(PATH_OUT+source+".csv",index=False)
        print("done with {} ({}/{})\n\n".format(source,i+1,len(dataSource)))

def merge_csv_files(output_file_name="CATEGORIES.csv"):
    for i,source in enumerate(dataSource):
        print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
        df = pd.read_csv(PATH_OUT+source+".csv")
        if(i==0):
            df_all = df
        else:
            df_all = df_all.append(df)
    df_all.to_csv(PATH_OUT+output_file_name,index=False)
    print("done with all\n\n")

def find_duplicates():
    df = pd.read_csv(PATH_OUT+"CATEGORIES.csv")
    df_duplicates = df.duplicated(keep="first")
    df.loc[df_duplicates].to_csv(PATH_OUT+"CATEGORIES_duplicates.csv",index=False)
    print("done with duplicates\n\n")

def find_duplicated_products_in_all_sources(asin="0151004714"):
    for i,source in enumerate(dataSource):
        print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
        df = pd.read_csv(PATH_CSV+source+".csv")
        products_match = df.loc[df['asin']==asin]
        if(len(products_match)>0):
            print(products_match.head())
    print("done with all\n\n")

def job_print_column(i,source):
    print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
    df = pd.read_csv(PATH_OUT+source+".csv")
    print(source)
    print(df.shape)
    print(df.columns)

def job_drop_unuseful_column(i, source):
    df = pd.read_csv(PATH_CSV+source+".csv")
    print(df.columns)
    cleared_df= df.drop(columns=['image', "style" ,"vote"]).drop_duplicates(subset=['asin','reviewerID'],keep= 'first')
    cleared_df.to_csv(PATH_CLEAR+source+"_cleared.csv",index=False)
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))
    
def job_check_for_missing_values(i, source):
    df = pd.read_csv(PATH_CLEAR+source+"_cleared.csv",dtype=REVIEWS_TYPE)
    print("overall {} reviewText {} reviewerID {} summary {} verified {} asin {} ".format(df.overall.isnull().sum(),df.reviewText.isnull().sum(),df.reviewerID.isnull().sum(),df.summary.isnull().sum(),df.verified.isnull().sum(),df.asin.isnull().sum()))
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))
    
def job_merge_csv_files(i, source):
    df = pd.read_csv(PATH_CLEAR+source+"_cleared.csv",dtype=REVIEWS_TYPE)
    if(df.shape[0]<MAX_PART_SIZE):
        return False
    chunks= np.array_split(df,df.shape[0]//MAX_PART_SIZE)
    for j,chunk in enumerate(chunks):
        chunk.to_csv(PATH_MERGE+source+"_"+str(j)+".csv",index=False)
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))



    

def split_csv_files(output_file_name="CATEGORIES.csv"):
    MAX_LEN= 500000
    for i,source in enumerate(dataSource):
        print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
        df = pd.read_csv(PATH_OUT+source+".csv")
        df_split = np.array_split(df,8)
        for j,df_part in enumerate(df_split):
            df_part.to_csv(PATH_OUT+source+"_"+str(j)+".csv",index=False)
    print("done with all\n\n")

def count_missing_values(source):
    df = pd.read_csv(PATH_CSV+source+".csv",dtype={"asin":str,"reviewerId":str,"vote":str})
    print(df.overall.isnull().sum())
    print(df.shape)



