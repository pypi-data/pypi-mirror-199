from collections import Counter

## SUBTEXT 2 ##
class SentimentAnalyser:
    """
    An object you can train with sentences and their corresponding sentiment scores to analyse some text.
    """
    def __init__(self):
        self.grams = {}
        self.gram_count = {}

    def generate_ngrams(self, sentence, n):
        words = sentence.split()
        ngrams = [words[i:i + n] for i in range(len(words) - n + 1)]
        return ngrams

    def add_sentences(self, sentences, scores, n_grams=1):
        """
        Add sentences and their corresponding sentiment scores to the analyser. 
        """
        for i, sentence in enumerate(sentences):
            ngrams = self.generate_ngrams(sentence, n_grams)
            for ngram in ngrams:
                ngram_tuple = tuple(ngram)
                if ngram_tuple in self.grams:
                    self.grams[ngram_tuple] += scores[i]
                    self.gram_count[ngram_tuple] += 1
                else:
                    self.grams[ngram_tuple] = scores[i]
                    self.gram_count[ngram_tuple] = 1

        self.calculate_average_scores()

    def calculate_average_scores(self):
        self.average_scores = {ngram: self.grams[ngram] / self.gram_count[ngram] for ngram in self.grams}

    def analyse(self, sentence, n_grams=1, detailed_view=False):
        """
        Analyse the sentiment of a sentence.
        """

        sentiment_scores = []
        total_ngrams = 0

        for n in range(1, n_grams + 1):
            ngrams = self.generate_ngrams(sentence, n)

            for ngram in ngrams:
                ngram_tuple = tuple(ngram)
                if ngram_tuple in self.average_scores:
                    sentiment_scores.append((ngram_tuple, self.average_scores[ngram_tuple]))
                    total_ngrams += 1

        if total_ngrams == 0:
            return None  # The sentiment analysis cannot be done for this sentence

        if detailed_view:
            return sentiment_scores
        else:
            sentiment_score = sum(score for _, score in sentiment_scores) / total_ngrams
            return sentiment_score

def n_grams(self, sentence, n):
    """
    Turn a sentence into n-grams.
    """
    words = sentence.split()
    ngrams = [words[i:i + n] for i in range(len(words) - n + 1)]
    return ngrams



