import numpy as np
import pandas as pd
from PAMI.frequentPattern.basic import FPGrowth
from PAMI.frequentPattern.basic import ECLAT
from utils.source import CATEGORIES, MAX_PART_SIZE, META_PARTS, METADATA_TYPE, PATH_CLEAR, PATH_CSV, PATH_JSON, PATH_MERGE, PATH_OUT, PATH_SPM, PATH_SPM_OUT, REVIEWS_TYPE, job_dispatch_in_dataSource
import seaborn as sns
import matplotlib.pyplot as plt

all= CATEGORIES
done = []
dataSource=list(set(all) - set(done))
print(dataSource)

###############################
##          JOBS            ###
###############################

def prepare_reviews_for_mining_categorized(i, source):
    df = pd.read_csv(PATH_CLEAR+source+"_cleared.csv",dtype=REVIEWS_TYPE)
    print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
    spm =df.loc[:,["reviewerID","asin","unixReviewTime"]].sort_values(['reviewerID','asin'],ascending=False).groupby("reviewerID")['asin'].apply(list)
    spm = spm.apply(lambda x: ";".join(x, ))
    spm.to_csv(PATH_SPM+source+".csv",index=False)
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))

def job_merge_csv_files(i, source):
    df = pd.read_csv(PATH_SPM+source+".csv",dtype=REVIEWS_TYPE)
    if(df.shape[0]<MAX_PART_SIZE):
        return False
    chunks= np.array_split(df,df.shape[0]//MAX_PART_SIZE)
    for j,chunk in enumerate(chunks):
        chunk.to_csv(PATH_MERGE+source+"_"+str(j)+".csv",index=False)
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))

def job_mine_patterns(i,source):
    path= PATH_SPM+source+".csv"
    df = pd.read_csv(path,dtype=REVIEWS_TYPE)
    support = int(df.shape[0]*0.0001)
    print("working on {} ({}/{}) SUP:{}".format(source,i+1,len(dataSource),support))
    fp = ECLAT.ECLAT(path,int(support),';')
    fp.startMine()
    fp.savePatterns(PATH_SPM_OUT+source+".csv")

    print('Runtime: {};{}'.format(str(fp.getRuntime()),source))
    print('Memory: ' + str(fp.getMemoryRSS()))
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))

def job_merge_data_files():
    for i,source in enumerate(dataSource):
        job_merge_csv_files(i,source)


def job_reveal_patterns(i,source):
    print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
    df = pd.read_csv(PATH_SPM_OUT+source+".csv",sep=":",header=None)
    
    print(df.tail)
    print(df.shape)
    # sorted= df.sort_values(by=1,ascending=False,inplace=False).filter(regex="([ ])",axis=0)
        # Transform the DataFrame of rules into a matrix using the lift metric
    # pivot = [].pivot(index = 'consequents', 
    #                     columns = 'antecedents', values= 'lift')

    # # Generate a heatmap with annotations on and the colorbar off
    # plt.figure(figsize=(10,6))
    # sns.heatmap(pivot, annot = True, cbar = False)
    # b, t = plt.ylim() 
    # b += 0.5 
    # t -= 0.5 
    # plt.ylim(b, t) 
    # plt.yticks(rotation=0)
    # plt.xticks(rotation=90)
    # plt.show()


###############################
##        PIPELINE          ###
###############################

def pipeline():
    # job_dispatch_in_dataSource(dataSource,prepare_reviews_for_mining_categorized,True)
    job_dispatch_in_dataSource(dataSource,job_mine_patterns,True)
    
# job_merge_data_files()
# pipeline()

job_mine_patterns(0,"reviews_Books_5")


# job_mine_patterns(0,"Gift_Cards_5")

# SEQUENTIAL PATTERN MINING
# we can now start the sequential pattern mining process.
# we will use the following parameters:
# - min_support: the minimum support of a pattern to be considered frequent
# - min_confidence: the minimum confidence of a pattern to be considered strong
# - min_lift: the minimum lift of a pattern to be considered relevant
# - min_length: the minimum length of a pattern to be considered long
# - max_length: the maximum length of a pattern to be considered long
# - max_patterns: the maximum number of patterns to be considered long
# - max_words: the maximum number of words to be considered long
# - max_ngrams: the maximum number of ngrams to be considered long
# - max_characters: the maximum number of characters to be considered long
# - max_tokens: the maximum number of tokens to be considered long
# - max_entities: the maximum number of entities to be considered long
# - max_concepts: the maximum number of concepts to be considered long
# - max_keywords: the maximum number of keywords to be considered long
# - max_sentences: the maximum number of sentences to be considered long




# 1. 
# from reviews in category 
# asin,reviewerID
# to reviewerID asin[]
# 2.
# TODO extract time required to perform pattern mining
# from freq patterns to => alone, coupled
# ???? extract products id wich are in more than 1 category and are not in metadata list


# to start as licterature suggests, we try to mine the frequent patterns divided in categories with a low support of 1% but no pattern appears.
# Dropping the support at a 0.1% we notice that some patters came out, but thoose patterns were caused by an unwated data duplication.
# Basically reviews of certain items like shoes were duplicated for each model or color, so we had do get back to the clearing process to remove those duplicates.

# e.g. B001IKJOLW B014IBJKNO B0058YEJ5K B005AGO4LU B0014F7B98 B0092UF54A B010RRWKT4 B009MA34NY :358 
# see oh no2