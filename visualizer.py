import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

reviews = pd.read_csv("./data/reviews_Digital_Music_5.csv").loc[0:1000]
# print(reviews.describe())
reviews = reviews.drop(columns=['unixReviewTime'])
print(reviews.head())


groupByAsin = reviews.groupby('asin').describe()
plt.figure(figsize=(14,6))
plt.title("groupByAsin")
sns.lineplot(data=groupByAsin)
sns.lineplot(data=groupByAsin)
plt.show()
# print(groupByAsin)

# # groupByAsin.sort_values(by='count', ascending=False)
# groupByReviewer = reviews.groupby('reviewerID').describe().sort_values(by=[('overall', 'count')], ascending=False)
# print(groupByReviewer)