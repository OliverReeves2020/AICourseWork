import csv
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import pos_tag, ne_chunk

#using tfid rather than bow but can easily switch with one line change

class QnAMatcher:
    def __init__(self, qna_file):
        self.qna_pairs = []
        with open(qna_file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                question = row[0]
                answer = row[1]
                self.qna_pairs.append((question, answer))
        self.vectorizer = CountVectorizer()
        self.tdvectorizer = TfidfVectorizer()
        self.corpus = [q for q, a in self.qna_pairs]
        self.X = self.vectorizer.fit_transform(self.corpus)
        self.Y = self.tdvectorizer.fit_transform(self.corpus)
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_input(self, user_input):
        # Tokenize the user's input
        tokens = word_tokenize(user_input)

        # Remove punctuation and stop words
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in string.punctuation and t not in stop_words]

        # Lemmatize the tokens
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]

        # Part-of-speech (POS) tag the tokens
        tagged_tokens = pos_tag(tokens)

        # Identify named entities in the tokens
        named_entities = ne_chunk(tagged_tokens)

        # Flatten the named entities into strings
        named_entities = [' '.join([t[0] for t in ne.leaves()]) for ne in named_entities if hasattr(ne, 'label')]

        # Add the named entities back to the token list
        tokens += named_entities

        # Convert the tokens back to a string
        processed_input = ' '.join(tokens)

        return processed_input

    def find_similar_question(self, user_input):
        u=user_input
        # Preprocess the user's input
        user_input = self.preprocess_input(user_input)

        # Use bow to represent the Q/As
        user_input_vector = self.vectorizer.transform([user_input])

        # Use cosine similarity to find the most similar question
        similarities = cosine_similarity(user_input_vector, self.X)
        most_similar_idx = similarities.argmax()
        most_similar_question = self.qna_pairs[most_similar_idx][0]
        most_similar_answer = self.qna_pairs[most_similar_idx][1]

        if(similarities[0][most_similar_idx])<0.2:
            # Preprocess the user's input
            user_input = self.preprocess_input(u)

            # Use tf-idf to represent the Q/As
            user_input_vector = self.tdvectorizer.transform([user_input])

            # Use cosine similarity to find the most similar question
            similarities = cosine_similarity(user_input_vector, self.Y)
            most_similar_idx = similarities.argmax()
            most_similar_question = self.qna_pairs[most_similar_idx][0]
            most_similar_answer = self.qna_pairs[most_similar_idx][1]


            if (similarities[0][most_similar_idx]) < 0.2:
                return(None,None)
            else:
                return most_similar_question,most_similar_answer
        else:
            return most_similar_question,most_similar_answer


