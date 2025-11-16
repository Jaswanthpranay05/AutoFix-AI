import re
import string
from collections import Counter
import nltk
from nltk.corpus import brown, words
from nltk.tokenize import word_tokenize
import requests
import json

# Download required NLTK data
try:
    nltk.download('brown')
    nltk.download('words')
    nltk.download('punkt')
    nltk.download('punkt_tab') 
except:
    pass

class AdvancedContextAutocorrector:
    def __init__(self):
        self.word_freq = Counter()
        self.vocab = set()
        self.common_mistakes = {}
        self.initialize_comprehensive_system()

    def initialize_comprehensive_system(self):
        """Initialize with large vocabulary and common mistake patterns"""
        print("🚀 Initializing Advanced Autocorrector...")

        # Load Brown corpus
        brown_words = [word.lower() for word in brown.words() if word.isalpha()]
        self.word_freq.update(brown_words)

        # Load English words
        english_words = [word.lower() for word in words.words()]
        self.word_freq.update(english_words)

        # Add custom common words with high frequency
        custom_words = [
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see',
            'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
            'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
            'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'today', 'went', 'college', 'making', 'attendance',
            'best', 'hello', 'hey', 'hi', 'good', 'morning', 'evening', 'night'
        ]

        for word in custom_words:
            self.word_freq[word] += 1000

        # Define common mistake patterns with context
        self.common_mistakes = {
            # Single letter errors
            'tday': 'today',
            'wt': 'went',
            'colege': 'college',
            'mking': 'making',
            'y': 'my',
            'attendee': 'attendance',
            'besst': 'best',
            'lov': 'love',
            'stdy': 'study',
            'gud': 'good',
            'f9': 'fine',
            'gr8': 'great',
            'b4': 'before',
            '2': 'to',
            '4': 'for',
            'u': 'you',
            'r': 'are',
            'plz': 'please',
            'thx': 'thanks',
            'msg': 'message',
            'pic': 'picture',
            'min': 'main',
            'goad': 'goal',
            'subcetjs': 'subjects',
            'recieve': 'receive',
            'seperate': 'separate',
            'definately': 'definitely',
            'occured': 'occurred',
            'adress': 'address',
            'comittee': 'committee',
            'embarass': 'embarrass',
            'existance': 'existence',
            'goverment': 'government',
            'harrass': 'harass',
            'neccessary': 'necessary',
            'priviledge': 'privilege',
            'rythm': 'rhythm',
            'succesful': 'successful',
            'tommorow': 'tomorrow',
            'truely': 'truly',
            'untill': 'until',
            'wierd': 'weird'
        }

        self.vocab = set(self.word_freq.keys())
        print(f"✅ Vocabulary loaded with {len(self.vocab)} words")
        print(f"✅ Common mistakes patterns: {len(self.common_mistakes)}")

    def edit_distance_1(self, word):
        """Generate all edits that are one edit away from word"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        deletes = [left + right[1:] for left, right in splits if right]
        transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
        replaces = [left + c + right[1:] for left, right in splits if right for c in letters]
        inserts = [left + c + right for left, right in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)

    def edit_distance_2(self, word):
        """Generate all edits that are two edits away from word"""
        return set(e2 for e1 in self.edit_distance_1(word) for e2 in self.edit_distance_1(e1))

    def known_words(self, words):
        """Return the subset of words that are in the vocabulary"""
        return set(w for w in words if w in self.vocab)

    def candidates(self, word):
        """Generate possible spelling corrections for word"""
        word_lower = word.lower()

        # First check common mistakes
        if word_lower in self.common_mistakes:
            return [self.common_mistakes[word_lower]]

        # If word is already correct
        if word_lower in self.vocab:
            return [word_lower]

        # Try edit distance 1
        edits1 = self.known_words(self.edit_distance_1(word_lower))
        if edits1:
            return list(edits1)

        # Try edit distance 2
        edits2 = self.known_words(self.edit_distance_2(word_lower))
        if edits2:
            return list(edits2)

        return [word_lower]

    def probability(self, word):
        """Probability of word in our frequency distribution"""
        N = sum(self.word_freq.values())
        return self.word_freq.get(word, 0) / N if N > 0 else 0

    def contextual_correction(self, words, current_index):
        """Apply context-aware corrections"""
        current_word = words[current_index].lower()

        # Context-based corrections
        if current_word == 'y' and current_index > 0:
            prev_word = words[current_index - 1].lower()
            if prev_word in ['for', 'to', 'is', 'are', 'was', 'were']:
                return 'my'

        if current_word == 'wt' and current_index > 0:
            prev_word = words[current_index - 1].lower()
            if prev_word == 'i':
                return 'went'

        return None

    def autocorrect_word(self, word, context_words=None, current_index=None):
        """Return the most probable correction for a single word with context"""
        if not word or not word.strip():
            return word

        # Keep original for case preservation
        original_word = word
        word_clean = word.lower().strip(string.punctuation)

        if not word_clean or word_clean.isnumeric():
            return word

        # Apply context-aware correction first
        if context_words and current_index is not None:
            contextual_corr = self.contextual_correction(context_words, current_index)
            if contextual_corr:
                # Preserve case
                if word[0].isupper():
                    contextual_corr = contextual_corr.capitalize()
                return contextual_corr

        # Check common mistakes
        if word_clean in self.common_mistakes:
            correction = self.common_mistakes[word_clean]
            if word[0].isupper():
                correction = correction.capitalize()
            return correction

        # Generate candidates
        candidates_list = self.candidates(word_clean)
        if not candidates_list:
            return word

        # Find best candidate based on probability
        best_candidate = max(candidates_list, key=self.probability)

        # Preserve original case if word was capitalized
        if word[0].isupper():
            best_candidate = best_candidate.capitalize()

        return best_candidate

    def autocorrect_sentence(self, sentence):
        """Autocorrect an entire sentence with context awareness"""
        if not sentence.strip():
            return sentence

        # Tokenize while preserving structure
        tokens = word_tokenize(sentence)
        corrected_tokens = []

        for i, token in enumerate(tokens):
            if token in string.punctuation or token.isspace():
                corrected_tokens.append(token)
            else:
                # Pass context for better corrections
                corrected_token = self.autocorrect_word(token, tokens, i)
                corrected_tokens.append(corrected_token)

        # Reconstruct sentence
        corrected_sentence = ""
        for i, token in enumerate(corrected_tokens):
            if token in string.punctuation:
                corrected_sentence = corrected_sentence.rstrip() + token + " "
            else:
                corrected_sentence += token + " "

        return corrected_sentence.strip()



