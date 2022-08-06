import pandas as pd

reviews = pd.read_csv("./data/reviews_Digital_Music_5.csv", index_col=0)
print(reviews.head())
print(reviews.describe())
reviews = reviews.drop(columns=['unixReviewTime'])

groupByAsin = reviews.groupby('asin').describe().sort_values(by=[('overall', 'count')], ascending=False)

print(groupByAsin)

# groupByAsin.sort_values(by='count', ascending=False)
groupByReviewer = reviews.groupby('reviewerID').describe().sort_values(by=[('overall', 'count')], ascending=False)
print(groupByReviewer)