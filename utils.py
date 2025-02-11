import contractions
import re

from textacy import preprocessing
from textacy.datasets.imdb import IMDB


def read_imdb(subset=None, with_label=True):
    """Read IMDB Dataset (via ``textacy.datasets.imdb.IMDB``).
    Args:
        subset (str): subset (e.g `train` / `test`).
        with_label (bool): whether to include only "labeled" samples.
    Returns:
        tuple(X[], y[])
    """
    dataset = IMDB()
    dataset.download()

    label = ['neg', 'pos'] if with_label else None
    samples = list(dataset.records(subset=subset, label=label))

    X = [sample[0] for sample in samples]
    y = [sample[1]['label'] for sample in samples]
    return X, y


def preprocess_sentence(sent, lower=True):
    """Pre-process a sentence ( via ``textacy.preprocess` module ).
    Args:
        sent (str): text.
        lower (bool): whether to return a lowercase string.
    Returns:
        str
    """
    # normalize unicode
    sent = preprocessing.normalize.unicode(sent)

    # deaccent
    sent = preprocessing.remove.accents(sent)

    # replace newline chars
    sent = re.sub("\n|\r", " ", sent)

    # unpack contractions
    sent = contractions.fix(sent)

    # replace emoji symbols
    sent = preprocessing.replace.emojis(sent)

    # replace hashtags
    sent = preprocessing.replace.hashtags(sent)

    # replace user handles
    sent = preprocessing.replace.user_handles(sent)

    # replace currency symbols
    sent = preprocessing.replace.currency_symbols(sent)

    # replace emails
    sent = preprocessing.replace.emails(sent)

    # replace URLs
    sent = preprocessing.replace.urls(sent)

    # remove punctuation
    sent = preprocessing.remove.punctuation(sent)

    # normalize whitespace
    sent = preprocessing.normalize.whitespace(sent)

    if lower:
        sent = sent.lower()
    return sent
