
# import json
# import re
# result= ""
# allBeauty = []

# with open('All_Beauty_fixed.json', 'r') as f:
#     allBeauty=json.load(f)

# print(len(allBeauty))
allBeauty=[

{"overall": 1.0, "verified": True, "reviewTime": "02 19, 2015", "reviewerID": "A1V6B6TNIC10QE", "asin": "0143026860", "reviewerName": "theodore j bigham", "reviewText": "great", "summary": "One Star", "unixReviewTime": 1424304000},
{"overall": 4.0, "verified": True, "reviewTime": "12 18, 2014", "reviewerID": "A2F5GHSXFQ0W6J", "asin": "0143026860", "reviewerName": "Mary K. Byke", "reviewText": "My  husband wanted to reading about the Negro Baseball and this a great addition to his library\n Our library doesn't haveinformation so this book is his start. Tthank you", "summary": "... to reading about the Negro Baseball and this a great addition to his library Our library doesn't haveinformation so ...", "unixReviewTime": 1418860800}
]


mapp= map(lambda x:x["asin"],allBeauty)
beaty_dictionary = { review : "In stock" for review in allBeauty }
print(beaty_dictionary.items())
# mylist = [["A",0], ["B",1], ["C",0], ["D",2], ["E",2]]

# values = set(map(lambda x:x["asin"], allBeauty))
# newlist = [[y[0] for y in allBeauty if y[1]==x] for x in values]