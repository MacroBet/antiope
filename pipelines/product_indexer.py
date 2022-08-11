import numpy as np
import pandas as pd
from PAMI.frequentPattern.basic import FPGrowth
from utils.source import CATEGORIES, MAX_PART_SIZE, META_PARTS, METADATA_TYPE, PATH_CLEAR, PATH_CSV, PATH_JSON, PATH_MERGE, PATH_OUT, PATH_SPM, PATH_SPM_OUT, REVIEWS_TYPE, job_dispatch_in_dataSource

all = CATEGORIES
done = []
dataSource=list(set(all) - set(done))
print(dataSource)

###############################
##          JOBS            ###
###############################

