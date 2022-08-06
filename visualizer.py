from traceback import print_tb
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

reviews = pd.read_csv("/Volumes/Extreme SSD/data/reviews_Digital_Music_5.csv")

print(reviews.head())
print(reviews.describe())


groupByAsin = reviews.groupby('asin')
print(groupByAsin.describe())
groupByAsin.sort_values(by='count', ascending=False)
# groupByReviewer = reviews.groupby('reviewerID').describe().sort_values(by=[('overall', 'count')], ascending=False)
# print(groupByReviewer)


# plt.figure(figsize=(14,6))
# plt.title("groupByAsin")
# sns.lineplot(data=groupByAsin)
# sns.lineplot(data=groupByAsin)
# plt.show()
# print(groupByAsin)