# Import spaCy
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Token
from spacy.tokens import Span
from spacy.tokens import Doc

nlp = spacy.load("en_core_web_sm")

print("\n### Token properties ###\n")
print("It costs $5.")
doc = nlp("It costs $5.")
print("Index:   ", [token.i for token in doc])
print("Text:    ", [token.text for token in doc])
print("is_alpha:", [token.is_alpha for token in doc])
print("is_punct:", [token.is_punct for token in doc])
print("like_num:", [token.like_num for token in doc])

print("\nShe ate the pizza")
doc = nlp("She ate the pizza")
for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)


print("\n### Docs entities ###\n")
# print(spacy.glossary.GLOSSARY)
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for ent in doc.ents:
    print(ent.text, ent.label_,"->",spacy.explain(ent.label_))


print("\n### Rule Base match ###\n")
matcher = Matcher(nlp.vocab)
iphonePattern = [{"LOWER": "iphone"}, {"LOWER": "x"}]
iosPattern = [{"TEXT": "iOS"}, {"IS_DIGIT": True}]
matcher.add("IPHONE_PATTERN", [iphonePattern])
matcher.add("IOS_VERSION_PATTERN", [iosPattern])
# exact text [{"TEXT": "iPhone"}, {"TEXT": "X"}] 
# lexical attributes [{"LOWER": "iphone"}, {"LOWER": "x"}]
# [{"LEMMA": "buy"}, {"POS": "NOUN"}]

doc = nlp(
    "After making the iOS update iPhone X you won't notice a radical system-wide "
    "redesign: nothing like the aesthetic upheaval we got with iOS 7. Most of "
    "iOS 11's furniture remains the same as in iOS 10. But you will discover "
    "some tweaks once you delve a little deeper in iphone X ."
)
matches = matcher(doc)
print("Apple total matches found:", len(matches))
for match_id, start, end in matches:
    print("Match found:", doc[start:end].text)

doc = nlp(
    "Twitch Prime, the perks program for Amazon Prime members offering free "
    "loot, games and other benefits, is ditching one of its best features: "
    "ad-free viewing. According to an email sent out to Amazon Prime members "
    "today, ad-free viewing will no longer be included as a part of Twitch "
    "Prime for new members, beginning on September 14. However, members with "
    "existing annual subscriptions will be able to continue to enjoy ad-free "
    "viewing until their subscription comes up for renewal. Those with "
    "monthly subscriptions will have access to ad-free viewing until October 15."
)


doc = nlp(
    "Features of the app include a beautiful design, smart search, automatic "
    "labels and optional voice responses."
)

# Write a pattern for adjective plus one or two nouns
pattern = [{"POS": "ADJ"}, {"POS": "NOUN"}, {"POS": "NOUN", "OP": "?"}]

# Add the pattern to the matcher and apply the matcher to the doc
matcher.add("ADJ_NOUN_PATTERN", [pattern])
matches = matcher(doc)
print("\nPos <ADJ NOUN NOUN?> total matches found:", len(matches))

# Iterate over the matches and print the span text
for match_id, start, end in matches:
    print("Match found:", doc[start:end].text)


print("\n### Extension Attribute ###\n")
def get_is_color(token):
    colors = ["red", "yellow", "blue"]
    return token.text in colors

Token.set_extension("is_color", getter=get_is_color)
doc = nlp("The sky is blue.")
print(doc[3]._.is_color, "-", doc[3].text)

# Define getter function
def get_has_color(span):
    colors = ["red", "yellow", "blue"]
    return any(token.text in colors for token in span)
# Set extension on the Span with getter
Span.set_extension("has_color", getter=get_has_color)

doc = nlp("The sky is blue.")
print(doc[1:4]._.has_color, "-", doc[1:4].text)
print(doc[0:2]._.has_color, "-", doc[0:2].text)

# Define method with arguments
def has_token(doc, token_text):
    in_doc = token_text in [token.text for token in doc]
    return in_doc

# Set extension on the Doc with method
Doc.set_extension("has_token", method=has_token)

doc = nlp("The sky is blue.")
print(doc._.has_token("blue"), "- blue")
print(doc._.has_token("cloud"), "- cloud")

# good
# docs = list(nlp.pipe(LOTS_OF_TEXTS))
# bad
# docs = [nlp(text) for text in LOTS_OF_TEXTS]
