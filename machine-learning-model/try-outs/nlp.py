# %% 
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# nltk.download('punkt')

text = "NLTK is a powerful tool for natural language processing."
words = word_tokenize(text)
sentences = sent_tokenize(text)

print(words)
print(sentences)

# %%

from nltk.corpus import stopwords

# nltk.download('stopwords')

words = ["This", "is", "an", "example", "sentence"]
filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]

print(filtered_words)

# %%

from nltk.stem import PorterStemmer

words = ["running", "jumps", "plays"]
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in words]

print(stemmed_words)

# %%
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# nltk.download('averaged_perceptron_tagger')

text = "NLTK is a powerful tool for natural language processing."
words = word_tokenize(text)
pos_tags = pos_tag(words)

print(pos_tags)


# %% 
from nltk import ne_chunk
from nltk.tokenize import word_tokenize

# nltk.download('maxent_ne_chunker')
# nltk.download('words')

text = "Barack Obama was born in Hawaii on August 4, 1961."
words = word_tokenize(text)
pos_tags = pos_tag(words)
named_entities = ne_chunk(pos_tags)

print(named_entities)


# %% Feature Extraction

from sklearn.feature_extraction.text import CountVectorizer

corpus = ["This is the first document.", "This document is the second document.", "And this is the third one."]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

print(X.toarray())

# %% 
'''
TF-IDF is a more advanced technique than BoW. It considers not only the 
frequency of a word in a document but also its importance in the entire dataset.
It assigns higher weights to words that are rare in the entire dataset but 
frequent in a specific document
'''
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = ["This is the first document.", "This document is the second document.", "And this is the third one."]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

print(X.toarray())

# %%
from gensim.models import Word2Vec

sentences = [["this", "is", "the", "first", "sentence"], ["this", "is", "the", "second", "sentence"], ["this", "is", "the", "third", "line"]]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
word_vec = model.wv['this']
print(word_vec)

similar_words = model.wv.most_similar('line', topn=5)
print(f"Words similar to 'this':\n{similar_words}")

# %% Text Summarization

import gensim
from gensim.summarization import summarize

original_text = 'Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. They generally ask for the junk food daily because they have been trend so by their parents from the childhood. They never have been discussed by their parents about the harmful effects of junk foods over health. According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways. They are generally fried food found in the market in the packets. They become high in calories, high in cholesterol, low in healthy nutrients, high in sodium mineral, high in sugar, starch, unhealthy fat, lack of protein and lack of dietary fibers. Processed and junk foods are the means of rapid and unhealthy weight gain and negatively impact the whole body throughout the life. It makes able a person to gain excessive weight which is called as obesity. Junk foods tastes good and looks good however do not fulfil the healthy calorie requirement of the body. Some of the foods like french fries, fried foods, pizza, burgers, candy, soft drinks, baked goods, ice cream, cookies, etc are the example of high-sugar and high-fat containing foods. It is found according to the Centres for Disease Control and Prevention that Kids and children eating junk food are more prone to the type-2 diabetes. In type-2 diabetes our body become unable to regulate blood sugar level. Risk of getting this disease is increasing as one become more obese or overweight. It increases the risk of kidney failure. Eating junk food daily lead us to the nutritional deficiencies in the body because it is lack of essential nutrients, vitamins, iron, minerals and dietary fibers. It increases risk of cardiovascular diseases because it is rich in saturated fat, sodium and bad cholesterol. High sodium and bad cholesterol diet increases blood pressure and overloads the heart functioning. One who like junk food develop more risk to put on extra weight and become fatter and unhealthier. Junk foods contain high level carbohydrate which spike blood sugar level and make person more lethargic, sleepy and less active and alert. Reflexes and senses of the people eating this food become dull day by day thus they live more sedentary life. Junk foods are the source of constipation and other disease like diabetes, heart ailments, clogged arteries, heart attack, strokes, etc because of being poor in nutrition. Junk food is the easiest way to gain unhealthy weight. The amount of fats and sugar in the food makes you gain weight rapidly. However, this is not a healthy weight. It is more of fats and cholesterol which will have a harmful impact on your health. Junk food is also one of the main reasons for the increase in obesity nowadays.This food only looks and tastes good, other than that, it has no positive points. The amount of calorie your body requires to stay fit is not fulfilled by this food. For instance, foods like French fries, burgers, candy, and cookies, all have high amounts of sugar and fats. Therefore, this can result in long-term illnesses like diabetes and high blood pressure. This may also result in kidney failure. Above all, you can get various nutritional deficiencies when you don’t consume the essential nutrients, vitamins, minerals and more. You become prone to cardiovascular diseases due to the consumption of bad cholesterol and fat plus sodium. In other words, all this interferes with the functioning of your heart. Furthermore, junk food contains a higher level of carbohydrates. It will instantly spike your blood sugar levels. This will result in lethargy, inactiveness, and sleepiness. A person reflex becomes dull overtime and they lead an inactive life. To make things worse, junk food also clogs your arteries and increases the risk of a heart attack. Therefore, it must be avoided at the first instance to save your life from becoming ruined.The main problem with junk food is that people don’t realize its ill effects now. When the time comes, it is too late. Most importantly, the issue is that it does not impact you instantly. It works on your overtime; you will face the consequences sooner or later. Thus, it is better to stop now.You can avoid junk food by encouraging your children from an early age to eat green vegetables. Their taste buds must be developed as such that they find healthy food tasty. Moreover, try to mix things up. Do not serve the same green vegetable daily in the same style. Incorporate different types of healthy food in their diet following different recipes. This will help them to try foods at home rather than being attracted to junk food.In short, do not deprive them completely of it as that will not help. Children will find one way or the other to have it. Make sure you give them junk food in limited quantities and at healthy periods of time. '
short_summary = summarize(original_text)
print(short_summary)
