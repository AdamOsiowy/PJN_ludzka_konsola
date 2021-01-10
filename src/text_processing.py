import spacy
import re

nlp = spacy.load("pl_core_news_lg")


def tokenize(text):
    global nlp
    return [tok for tok in nlp(text)]


def checkIfContainOrder(text) -> bool:
    tokens = tokenize(text)
    for tok in tokens:
        if tok.tag_ == "IMPT":
            return True
    return False


def tagPartOfSpeech(tokens):
    toks = [tok.text for tok in tokens]
    parts_of_speech = [tok.tag_ for tok in tokens]
    return dict(zip(toks, parts_of_speech))


def lematize(tokens):
    return [tok.lemma_ for tok in tokens]


def removeStopWords(tokens):
    return [tok for tok in tokens if tok.is_stop is False]


def findOrderAndArgs(tokens):
    order = ""
    args = dict()
    for i in range(len(tokens)):
        if tokens[i].tag_ == "IMPT":
            order = tokens[i]
            tokens = tokens[i + 1:]
            break
    order = lematize([order])[0]
    # args = lematize(tokens)
    # args = tokenize(' '.join(args))
    args = tagPartOfSpeech(tokens)
    return order, args


def getTaskAndArgs(text: str) -> dict:
    if checkIfContainOrder(text):
        tokens = tokenize(text)
        withoutStopWords = removeStopWords(tokens)
        order, args = findOrderAndArgs(withoutStopWords)
        return {'order': order, 'args': args}
    else:
        return {'order': '', 'args': dict()}
