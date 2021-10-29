import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

links_small = pd.read_csv('data/links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')

data = pd.read_csv('data/movies_metadata.csv')
data = data.drop([19730, 29503, 35587])
data['id'] = data['id'].astype('int')

eco = data[data['id'].isin(links_small)]
eco['overview'] = eco['overview'].fillna(' ')
eco = eco.reset_index()

titles = eco['title']

vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tf_idf = vectorizer.fit_transform(eco['overview'])
print(tf_idf)
linear = linear_kernel(tf_idf, tf_idf)
print(linear.shape)

def close_matches(fav_movie):
    all_close_matches = []
    for id, title in enumerate(eco['title']):
        title = str(title)
        fav_movie = str(fav_movie)
        close_match = fuzz.ratio(title.lower(), fav_movie.lower())

        if close_match >= 50:
            all_close_matches.append((title, id, close_match))

    all_close_matches = sorted(all_close_matches, key=lambda x: x[2])[::-1]
    return all_close_matches[0]

# stemmer = nltk.stem.porter.PorterStemmer()
# remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
#
# def stem_tokens(tokens):
#     return [stemmer.stem(item) for item in tokens]
#
# def normalize(text):
#     return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
# vectorizer = TfidfVectorizer(analyzer='word',ngram_range=(1, 3),min_df=0, stop_words='english')
# def cosine_sim(text1, text2):
#     tfidf = vectorizer.fit_transform([text1, text2])
#     return linear_kernel(tfidf,tfidf)


def Rec(value):
    close_match = close_matches(value)
    cos_sim = linear[close_match[1]]
    sim = list(enumerate(cos_sim))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    top_5 = [(titles.iloc[movie[0]], movie[1]) for movie in sim[1:6]]
    return top_5