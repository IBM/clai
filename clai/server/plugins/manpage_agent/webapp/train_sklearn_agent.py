#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import logging
import pathlib
import pickle
import sys
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer

_BASE_PATH = os.path.dirname(os.path.realpath(__file__))


PATTERN_DASH = re.compile("[-_]+")
PATTERN_SPACES = re.compile("\s+")


def absolute_path(relative_path):
    return os.path.join(_BASE_PATH, relative_path)


def cleanup(text: str) -> str:
    text = PATTERN_SPACES.sub(" ", text).strip()
    text = PATTERN_DASH.sub("", text).strip()
    return text


def identify_sections(sentences: list):
    sentences = [cleanup(sentence) for sentence in sentences]
    segments = []
    start_index = 0
    empty_sentence = 0
    for idx, sentence in enumerate(sentences):
        if not sentence:
            if empty_sentence >= 1:
                segments.append(sentences[start_index:idx])
                start_index = idx + 1
                empty_sentence = 0
            else:
                empty_sentence += 1

    sections = list()
    for segment in segments:
        sentences = list(filter(None, segment))
        if sentences:
            sections.append(" ".join([sentences for sentences in segment if sentences]))

    return sections


def parse_manpage(text: list) -> str:
    return " ".join(identify_sections(text))


def load_manpages(print_every=1e3) -> dict:
    logging.info("==================================")
    logging.info("Processing manpages")
    logging.info("==================================")

    documents = {}
    files = pathlib.Path("./data/manpages/").glob("*.txt")
    for idx, f in enumerate(files):
        with open(f, "r") as fp:
            content = parse_manpage(fp.readlines())
            if content:
                documents[f.name.split(".txt")[0]] = content

        if idx % print_every == 0:
            msg = "Finished processing {} manpages.".format(idx)
            logging.info(msg)
    return documents


def transform(corpus) -> (TfidfVectorizer, list):
    vectorizer = TfidfVectorizer(
        input="content",
        lowercase=True,
        analyzer="word",
        stop_words="english",
        ngram_range=(1, 2),
    )

    vectors = vectorizer.fit_transform(corpus)

    # Set stop_words_ attr to None to save on disk space
    # See the `Notes` here:
    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

    vectorizer.stop_words_ = None

    return vectorizer, vectors


def save(func, vectors, keys):

    with open(absolute_path("./data/model/func.p"), "wb") as fp:
        pickle.dump(func, fp)

    with open(absolute_path("./data/model/vectors.p"), "wb") as fp:
        pickle.dump(vectors, fp)

    with open(absolute_path("./data/model/keys.p"), "wb") as fp:
        pickle.dump(keys, fp)


if __name__ == "__main__":
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(
        format=LOG_FORMAT, level=getattr(logging, "INFO"), stream=sys.stdout
    )

    # Read and process manpages
    manpages = load_manpages()

    # Index processed manpages data
    logging.info("==================================")
    logging.info("Transforming manpages")
    logging.info("==================================")

    transformer_func, vectors = transform(manpages.values())

    logging.info("==================================")
    logging.info("Saving model information")
    logging.info("==================================")
    # Save model information
    save(transformer_func, vectors, list(manpages.keys()))

    logging.info("==================================")
    logging.info("Installation complete")
    logging.info("==================================")
