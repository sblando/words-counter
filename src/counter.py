# src/words_counter/counter.py
from collections import Counter
from pathlib import Path
from typing import Tuple, Dict
import pandas as pd
from cleaner import TextCleaner  # if not in a package yet: from cleaner import TextCleaner


class WordCounter:
    """Load .txt files, clean tokens, count frequencies, and export CSV reports."""

    def __init__(self, input_dir: str = "data", output_dir: str = "output", language: str = "english"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.cleaner = TextCleaner(language)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_texts(self) -> Dict[str, str]:
        """Read every *.txt in input_dir into memory."""
        texts: Dict[str, str] = {}
        for f in self.input_dir.glob("*.txt"):
            texts[f.name] = f.read_text(encoding="utf-8", errors="ignore")
        return texts

    def analyze(self, top: int = 20) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Returns:
          df_global         : full frequencies across all docs  (cols: word, freq)
          df_top_global     : top-N overall                      (cols: word, freq)
          df_top_per_doc    : top-N per document                 (cols: document, word, freq)
        Also saves them into self.output_dir.
        """
        texts = self._load_texts()

        global_counter = Counter()
        per_doc: Dict[str, Counter] = {}

        # 1) Build per-document and global counters
        for name, txt in texts.items():
            tokens = self.cleaner.clean_and_tokenize(txt)
            c = Counter(tokens)
            per_doc[name] = c
            global_counter.update(c)

        # 2) Convert to DataFrames (sorted by frequency desc)
        df_global = (
            pd.DataFrame(global_counter.items(), columns=["word", "freq"])
            .sort_values("freq", ascending=False, kind="mergesort")
            .reset_index(drop=True)
        )
        df_top_global = df_global.head(top)

        # 3) Top-N per document
        rows = []
        for doc, counter in per_doc.items():
            for word, freq in counter.most_common(top):
                rows.append({"document": doc, "word": word, "freq": freq})
        df_top_per_doc = pd.DataFrame(rows, columns=["document", "word", "freq"])

        # 4) Save CSVs
        (self.output_dir / "frequencies_global.csv").write_text(
            df_global.to_csv(index=False), encoding="utf-8"
        )
        (self.output_dir / "top_global.csv").write_text(
            df_top_global.to_csv(index=False), encoding="utf-8"
        )
        (self.output_dir / "top_per_document.csv").write_text(
            df_top_per_doc.to_csv(index=False), encoding="utf-8"
        )

        print(f"✓ Results saved in {self.output_dir.resolve()}")
        return df_global, df_top_global, df_top_per_doc
