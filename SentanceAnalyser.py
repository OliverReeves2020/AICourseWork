# Import the Natural Language Toolkit (nltk) library
import nltk

class SentenceAnalyser():
    def __init__(self):


        # Download the nps_chat corpus from nltk
        nltk.download('nps_chat')



        # Get the xml_posts from the nps_chat corpus and select the first 10000 posts
        posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        # Extract the features from each post in the nps_chat corpus, and store them as a list of tuples
        featuresets = [(self.dialogue_act_features(post.text), post.get('class')) for post in posts]

        # Split the featuresets into a training set (90%) and a testing set (10%)
        size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[size:], featuresets[:size]

        # Train a Naive Bayes classifier on the training set
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

# Define a function to extract features from a post
    def dialogue_act_features(self,post):
        # Create an empty dictionary to store the features
        features = {}
        # Tokenize the post into words and iterate over each word
        for word in nltk.word_tokenize(post):
            # Add a feature for each word, with the key 'contains(word)' and value True
            features['contains({})'.format(word.lower())] = True
        # Return the dictionary of features
        return features
