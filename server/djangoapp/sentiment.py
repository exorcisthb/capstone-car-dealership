"""
Lightweight, dependency-free sentiment analysis.

Uses a curated lexicon of positive/negative words commonly used
in car dealership reviews. This produces deterministic output
without any external API keys or network calls.
"""
POSITIVE_WORDS = {
    'fantastic', 'excellent', 'great', 'good', 'amazing', 'wonderful', 'awesome',
    'love', 'loved', 'best', 'perfect', 'perfectly', 'superb', 'outstanding',
    'happy', 'glad', 'satisfied', 'recommend', 'recommended', 'pleasant',
    'friendly', 'helpful', 'professional', 'smooth', 'easy', 'comfortable',
    'nice', 'fine', 'positive', 'fast', 'quick', 'reliable', 'trustworthy',
    'honest', 'fair', 'quality', 'brilliant', 'enjoy', 'enjoyed', 'clean',
    'beautiful', 'fun', 'cool', 'impressive', 'remarkable', 'exceptional',
    'top', 'top-notch', 'delightful', 'kind', 'polite', 'efficient', 'responsive',
    'reasonable', 'affordable', 'worth', 'worthwhile', 'incredible', 'fabulous',
    'phenomenal', 'stellar', 'splendid', 'lovely', 'pleasant', 'stellar',
    'knowledgeable', 'courteous', 'transparent', 'no-pressure', 'no pressure',
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'worst', 'poor', 'disappointing',
    'disappointed', 'hate', 'hated', 'unhappy', 'unsatisfied', 'rude',
    'unprofessional', 'difficult', 'uncomfortable', 'unpleasant', 'slow',
    'unreliable', 'dishonest', 'unfair', 'overpriced', 'expensive', 'waste',
    'wasted', 'regret', 'regretful', 'never', 'avoid', 'scam', 'fraud',
    'fraudulent', 'broken', 'damage', 'damaged', 'dirty', 'ugly', 'annoying',
    'annoyed', 'frustrated', 'frustrating', 'angry', 'mad', 'horrible',
    'lousy', 'terrible', 'sucks', 'horrendous', 'dreadful', 'appalling',
    'catastrophic', 'nightmare', 'misleading', 'deceptive', 'pushy', 'aggressive',
    'late', 'delayed', 'unhelpful', 'unresponsive', 'ignored', 'rushed',
}


def analyze_sentiment(text):
    """
    Analyze sentiment of a text.

    Returns:
        (sentiment, score) where sentiment is one of
        'positive' / 'negative' / 'neutral', and score is
        the (positive_count - negative_count) / total_words ratio.
    """
    if not text or not text.strip():
        return 'neutral', 0.0

    words = [w.strip('.,!?;:"\'()[]{}').lower() for w in text.split()]
    words = [w for w in words if w]

    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = len(words) or 1

    score = (pos - neg) / total

    if score > 0.05:
        sentiment = 'positive'
    elif score < -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment, round(score, 3)
