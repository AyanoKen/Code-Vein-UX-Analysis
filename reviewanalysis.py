
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
import matplotlib.pyplot as plt
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')

# Function to preprocess text
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Convert tokens to lowercase
    tokens = [token.lower() for token in tokens if token.isalnum()]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    return filtered_tokens

# Function to perform NLP analysis
def analyze_reviews(csv_file):
    # Open the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if it exists
        
        # Initialize variables for analysis
        all_tokens = []
        all_sentences = []
        all_tags = []
        positive_reviews = 0
        negative_reviews = 0
        neutral_reviews = 0
        
        # Initialize sentiment analyzer
        sid = SentimentIntensityAnalyzer()
        
        # Process each row in the CSV file
        for row in reader:
            review = row[2]  # Assuming reviews are in column 3 (index 2)
            
            # Tokenize the review
            tokens = preprocess_text(review)
            all_tokens.extend(tokens)
            
            # Tokenize sentences
            sentences = sent_tokenize(review)
            all_sentences.extend(sentences)
            
            # Perform sentiment analysis
            sentiment_score = sid.polarity_scores(review)['compound']
            if sentiment_score > 0:
                positive_reviews += 1
            elif sentiment_score < 0:
                negative_reviews += 1
            else:
                neutral_reviews += 1
                
            # Perform part-of-speech tagging
            tagged_tokens = pos_tag(tokens)
            all_tags.extend(tagged_tokens)
            
    # Calculate word frequency distribution      
    
    fdist = FreqDist(all_tokens)
    most_common_words = fdist.most_common(21)[1:]
    
    # Print analysis results
    # print("Total reviews:", positive_reviews + negative_reviews + neutral_reviews)
    # print("Positive reviews:", positive_reviews)
    # print("Negative reviews:", negative_reviews)
    # print("Neutral reviews:", neutral_reviews)
    # print("\nMost common words:")
    # for word, frequency in most_common_words:
    #     print(f"{word}: {frequency}")

    words, frequencies = zip(*most_common_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies)
    plt.title('Top Used Words in Reviews')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

    filtered_tokens = [token[0] for token in tagged_tokens if token[1] not in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
                
    # Find and score bigrams
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(filtered_tokens)
    scored_bigrams = finder.score_ngrams(bigram_measures.raw_freq)

    top_bigrams = scored_bigrams[:10]
    
    # Plot top used phrases
    phrases = [' '.join(bigram) for bigram, _ in top_bigrams]
    frequencies = [freq for _, freq in top_bigrams]
    
    plt.figure(figsize=(10, 5))
    plt.bar(phrases, frequencies)
    plt.title('Top Used Phrases in Reviews (Excluding Verbs)')
    plt.xlabel('Phrases')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()
    
    # Print tagged tokens
    # print("\nPart-of-speech tagging:")
    # print(all_tags)



csv_file = "output.csv"
analyze_reviews(csv_file)    
    
    
