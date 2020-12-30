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
    parts_of_speech = [tok.tag_ for tok in tokens]
    return dict(zip(tokens, parts_of_speech))


def lematize(tokens):
    return [tok.lemma_ for tok in tokens]


def removeStopWords(lemmas):
    tokens = tokenize(' '.join(lemmas))
    return [tok.text for tok in tokens if tok.is_stop is False]


def removePunctuationMarks(tokens):
    return [re.sub(r'[?:!,.;]', r'', tok) for tok in tokens]


def getTaskAndArgs(text: str):
    tokens = tokenize(text)
    lemmas = lematize(tokens)
    withoutStopWords = removeStopWords(lemmas)
    withoutPunctuationMarks = removePunctuationMarks(withoutStopWords)
    new_tokens = tokenize(' '.join(withoutPunctuationMarks))
    parts_of_speech = tagPartOfSpeech(new_tokens)
    print(parts_of_speech)


if __name__ == "__main__":
    doc1 = 'wyłącz Spotify'
    doc2 = 'zmniejsz głośność odtwarzacza muzyki'
    doc3 = 'wyszukaj w internecie informacje o drugiej wojnie światowej'
    doc4 = 'zrób zrzut ekranu i zapisz go jako screenshot1'
    doc5 = 'zapisać zapisz'

    # for token in doc1:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)
    getTaskAndArgs(doc1)
    checkIfContainOrder(doc1)
    getTaskAndArgs(doc2)
    checkIfContainOrder(doc2)
    getTaskAndArgs(doc3)
    checkIfContainOrder(doc3)
    getTaskAndArgs(doc4)
    checkIfContainOrder(doc4)
    getTaskAndArgs(doc5)
    checkIfContainOrder(doc5)
