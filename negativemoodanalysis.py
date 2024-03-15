import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Download NLTK resources
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load the CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# Perform mood analysis
def analyze_reviews(data):
    sid = SentimentIntensityAnalyzer()
    data['sentiment'] = data['review'].apply(lambda x: sid.polarity_scores(x)['compound'])
    return data

# Extract phrases containing negative adjectives and their associated nouns
def extract_negative_phrases(data):
    negative_phrases = []
    stop_words = set(stopwords.words('english'))

    for review in data['review']:
        sentences = sent_tokenize(review)
        for sentence in sentences:
            words = word_tokenize(sentence)
            tagged_words = nltk.pos_tag(words)
            for i in range(len(tagged_words) - 1):
                if tagged_words[i][1] == 'JJ' and tagged_words[i][0] in ['difficult', 'hard', 'challenging', 'complicated', 'frustrating', 'annoying'] \
                   and tagged_words[i+1][1] == 'NN' and tagged_words[i][0] not in stop_words:
                    phrase = tagged_words[i][0] + ' ' + tagged_words[i+1][0]
                    negative_phrases.append(phrase)
    return negative_phrases


file_path = 'output.csv'
data = load_data(file_path)
data = analyze_reviews(data)
negative_phrases = extract_negative_phrases(data)

freq_dist = nltk.FreqDist(negative_phrases)

print("\nTop 10 Negative Phrases:")
for phrase, frequency in freq_dist.most_common(10):
    print(f"{phrase}: {frequency}")

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
freq_dist.plot(30, cumulative=False)
plt.title('Frequency Distribution of Negative Phrases')
plt.xlabel('Phrases')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


