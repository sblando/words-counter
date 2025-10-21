# words-counter

A beginner-friendly **text mining** project written in Python.  
It reads multiple `.txt` files from a folder, cleans the text in English, and generates the **top N most frequent words** per document and overall.

---

## Dataset

The dataset consists of the **top 5 ebooks** from [Project Gutenberg](https://www.gutenberg.org) at the time of this project’s creation:

- *Alice's Adventures in Wonderland* — Lewis Carroll  
- *Frankenstein; or, The Modern Prometheus* — Mary Wollstonecraft Shelley  
- *Moby Dick; or, The Whale* — Herman Melville  
- *Pride and Prejudice* — Jane Austen  
- *Romeo and Juliet* — William Shakespeare  

All texts are stored in the `data/` folder in plain `.txt` format.

---

## Installation

- Python 3.10–3.12
- Install dependencies:

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

### NLTK data (once)

```python
import nltk
```

```python
nltk.download("stopwords")
```

---

## How to run

This repository uses a flat `src/` layout, so run the script directly:

```bash
python src/main.py --input data --output output --top 20
```


 or with short flags


```bash
python src/main.py -i data -o output -t 20
```

---

## Outputs

CSV files are written to `output/`:

- `frequencies_global.csv`
- `top_global.csv`
- `top_per_document.csv`

> Note: `output/` is ignored in version control (only `.gitkeep` is tracked).  
> Small preview images live in `examples/` (e.g., `examples/top_global.png`, `examples/top_per_document.png`).

---

## Reproducibility

To reproduce the same results:

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```python
import nltk
```

```python
nltk.download("stopwords")
```

```bash
python src/main.py -i data -o output -t 20
```
