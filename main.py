import argparse
import logging
from collections import Counter

def main(args):
    """
    :return: vocab
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.info(args)

    logging.info("1. Obtain vocab")
    vocab = None
    for each_file in args.file_path:
        word2freq = Counter()
        with open(each_file) as fp:
            for line in fp:
                words = line.strip().split()
                for word in words:
                    word2freq[word] += 1
        logging.debug(word2freq.most_common()[:10])
        if vocab is None:
            vocab = [w for w, freq in word2freq.items() if freq >= args.threshold]
        else:
            vocab = [w for w in vocab if word2freq[w] >= args.threshold]
    logging.info(f" vocab: {len(vocab)} words")
    with open("vocab.txt", "w") as wp:
        for word in vocab:
            wp.write(f"{word}\n")

    logging.info("2. Load target words")
    if args.target_words is not None:
        target_words = []
        with open(args.target_words) as fp:
            for line in fp:
                word = line.strip()
                target_words.append(word)
    else:
        target_words = vocab
    logging.info(f" target words: {len(target_words)} words")
    
    logging.info("3. Replace corpora")
    with open("corpus_replaced.txt", "w") as wp:
        for file_id, each_file in enumerate(args.file_path):
            logging.info(f"{file_id}th corpus")
            with open(each_file) as fp:
                for line in fp:
                    words = line.strip().split()
                    words = [f"{word}_{file_id}" if word in target_words else word for word in words]
                    wp.write(f"{' '.join(words)}\n")

    logging.info("4. Fix vocab")
    for target_word in target_words:
        if target_word in vocab:
            vocab.remove(target_word)
        for file_id in range(len(args.file_path)):
            vocab.append(f"{target_word}_{file_id}")

    logging.info(f" vocab (fixed): {len(vocab)} words")
    with open("vocab_fixed.txt", "w") as wp:
        for word in vocab:
            wp.write(f"{word}\n")

def cli_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path", nargs="*", help="path to target files")
    parser.add_argument("-w", "--target_words", help="path to a list of target words")
    parser.add_argument("-t", "--threshold", type=int, help="frequency threshold for vocab")
    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    cli_main()
