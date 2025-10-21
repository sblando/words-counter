import re
import nltk

class TextCleaner:
    """Minimal cleaner/tokenizer for English text."""

    # Keep only A–Z letters and whitespace; drop everything else.
    LETTERS = r"A-Za-z"
    RE_KEEP = re.compile(fr"[^ {LETTERS}\s]", re.UNICODE)

    def __init__(self, language: str = "english", min_len: int = 3):
        self.language = language
        self.min_len = min_len
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self) -> set:
        """Return NLTK stopwords for the chosen language (download if missing)."""
        try:
            return set(nltk.corpus.stopwords.words(self.language))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(nltk.corpus.stopwords.words(self.language))

    def clean_and_tokenize(self, text: str) -> list[str]:
        """
        Lowercase → remove non-letters → collapse spaces → split → filter
        (min length + not a stopword).
        """
        text = text.lower()
        text = self.RE_KEEP.sub(" ", text)          # strip punctuation/symbols/numbers
        text = re.sub(r"\s+", " ", text).strip()    # normalize whitespace
        tokens = [
            t for t in text.split(" ")
            if len(t) >= self.min_len and t not in self.stopwords
        ]
        return tokens
