# src/words_counter/counter.py
from collections import Counter
from pathlib import Path
from .cleaner import TextCleaner  # if not in a package yet: from cleaner import TextCleaner


class WordCounter:
    """Load .txt files, clean tokens, and build per-document/global counters."""

    def __init__(self, input_dir: str = "data", output_dir: str = "output", language: str = "english"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.cleaner = TextCleaner(language)
        self.output_dir.mkdir(parents=True, exist_ok=True)  # ensure output folder exists

    def _load_texts(self) -> dict[str, str]:
        """Read every *.txt in input_dir into memory."""
        texts: dict[str, str] = {}
        for f in self.input_dir.glob("*.txt"):
            # errors='ignore' avoids breaking on rare encodings; utf-8 is default here
            texts[f.name] = f.read_text(encoding="utf-8", errors="ignore")
        return texts

    def analyze(self, top: int = 20) -> tuple[Counter, dict[str, Counter]]:
        """
        Build:
          - global_counter: frequencies across all documents
          - per_doc: a Counter per document
        """
        texts = self._load_texts()

        global_counter = Counter()
        per_doc: dict[str, Counter] = {}

        for name, txt in texts.items():
            tokens = self.cleaner.clean_and_tokenize(txt)  # normalize + tokenize + filter
            c = Counter(tokens)                            # per-document frequencies
            per_doc[name] = c
            global_counter.update(c)                       # aggregate globally

        # Return counters for now; CSV export will be added in the next commit.
        return global_counter, per_doc
