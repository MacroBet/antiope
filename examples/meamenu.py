

import pandas as pd

reviews = pd.read_csv("/Users/marco/Desktop/data.csv", index_col=0)

filtered= reviews.loc[reviews["Territorio"]=="Italia"]
filtered2= filtered.loc[filtered["Sesso"]=="totale"]
output = filtered2[["Territorio", "Sesso","Età","Value"]]
output.to_csv("italiani.csv")
print(int("1 anni".split(" ")[0]))

print(filtered2.head())
print(filtered2.describe())

# # Accessing Data
# reviews.set_index("title")
# reviews.loc[0:10, ['col1', 'col2']]

# # Conditional selection
# reviews.country == 'Italy' # return Series array of boolean
# reviews.loc[(reviews.country == 'Italy') & (reviews.points >= 90)]
# reviews.loc[reviews.country.isin(['Italy', 'France'])]
# reviews.loc[reviews.price.notnull()]

# # Assigning data
# reviews['index_backwards'] = range(len(reviews), 0, -1)
# reviews['index_backwards']

# ###########################
# # CAP 3 Summary functions #
# ###########################

# reviews.points.describe()
# reviews.taster_name.describe()
# reviews.points.mean()
# reviews.taster_name.unique()

# reviews.taster_name.value_counts()
# # Roger Voss           25514
# # Michael Schachner    15134
# #                      ...  
# # Fiona Adams             27
# # Christina Pickard        6
# # Name: taster_name, Length: 19, dtype: int64

# review_points_mean = reviews.points.mean()
# reviews.points.map(lambda p: p - review_points_mean)
# # 0        -1.447138
# # 1        -1.447138
# #             ...   
# # 129969    1.552862
# # 129970    1.552862

# def remean_points(row):
#     row.points = row.points - review_points_mean
#     return row

# reviews.apply(remean_points, axis='columns')

# # which is the same as 
# review_points_mean = reviews.points.mean()
# reviews.points - review_points_mean

# # very cool!
# reviews.country + " - " + reviews.region_1

# # examples:
# bargain_idx = (reviews.points / reviews.price).idxmax()
# bargain_wine = reviews.loc[bargain_idx, 'title']

# # There are only so many words you can use when describing a bottle of wine. 
# # Is a wine more likely to be "tropical" or "fruity"? 
# # Create a Series descriptor_counts counting how many times each of these two words
# # appears in the description column in the dataset. 
# # (For simplicity, let's ignore the capitalized versions of these words.)
# n_trop = reviews.description.map(lambda desc: "tropical" in desc).sum()
# n_fruity = reviews.description.map(lambda desc: "fruity" in desc).sum()
# descriptor_counts = pd.Series([n_trop, n_fruity], index=['tropical', 'fruity'])


# ##############################
# # CAP 4 Grouping and sorting #
# ##############################

# reviews.groupby('points').points.count()

# reviews.groupby(['country', 'province']).apply(lambda df: df.loc[df.points.idxmax()])

# reviews.groupby(['country']).price.agg([len, min, max])

# # Multi index
# countries_reviewed = reviews.groupby(['country', 'province']).description.agg([len])
# # first index is country, second is province
# # to get back to the original index progressives, use .reset_index()
# countries_reviewed.reset_index()

# # Sorting 
# countries_reviewed.sort_values(by='len')
# countries_reviewed.sort_values(by=['country', 'len'])
# # get back to original sorting
# countries_reviewed.sort_index()

# # examples
# best_rating_per_price = reviews.groupby('price')['points'].max().sort_index()

