import spacy
import re

nlp = spacy.load("pl_core_news_lg")


def tokenize(text):
    global nlp
    return [tok for tok in nlp(text)]


def checkIfContainOrder(text) -> bool:
    tokens = tokenize(text)
    if tokens[0].tag_ == "IMPT":
        return True
    return False


def tagPartOfSpeech(tokens):
    parts_of_speech = [tok.tag_ for tok in tokens]
    return dict(zip(tokens, parts_of_speech))


def lematize(tokens):
    return [tok.lemma_ for tok in tokens]


def removeStopWords(lemmas):
    tokens = tokenize(' '.join(lemmas))
    return [tok.text for tok in tokens if tok.is_stop is False]


def removePunctuationMarks(tokens):
    return [re.sub(r'[?:!,.;]', r'', tok) for tok in tokens]


def getTaskAndArgs(text: str) -> dict:
    if checkIfContainOrder(text):
        tokens = tokenize(text)
        lemmas = lematize(tokens)
        withoutStopWords = removeStopWords(lemmas)
        withoutPunctuationMarks = removePunctuationMarks(withoutStopWords)
        new_tokens = tokenize(' '.join(withoutPunctuationMarks))
        order = new_tokens[0]
        new_tokens = new_tokens[1:]
        parts_of_speech = tagPartOfSpeech(new_tokens)
        return {'order': order, 'args': parts_of_speech}
    else:
        return {'order': '', 'args': dict()}
