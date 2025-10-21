import argparse
from .counter import WordCounter

def main():
    # Command Line Interface: minimal, explicit flags
    parser = argparse.ArgumentParser(description="Word Counter")
    parser.add_argument("--input", "-i", default="data", help="Folder with .txt files")
    parser.add_argument("--output", "-o", default="output", help="Folder to write CSV reports")
    parser.add_argument("--language", "-l", default="english", help="Stopwords language (NLTK)")
    parser.add_argument("--top", "-t", type=int, default=20, help="Top-N most frequent words")
    args = parser.parse_args()

    # Build the pipeline and run
    counter = WordCounter(
        input_dir=args.input,
        output_dir=args.output,
        language=args.language
    )
    counter.analyze(top=args.top)  # writes CSVs to output/

if __name__ == "__main__":
    main()
