from typing import List
import string

class TextCleaner:
    def __init__(self):
        self.cleaned_words: List[str] = []

    def text_to_words(self, text: str) -> List[str]:
        text = text.replace("\n", " ")
        words = text.split(" ")
        return words

    def clean_words(self, unsorted_words: List[str]) -> List[str]:
        cleaned_words = []
        for word in unsorted_words:
            clean_word = word.strip(string.punctuation)
            if clean_word != "":
                cleaned_words.append(clean_word)
        return cleaned_words

    def clean(self, text: str) -> List[str]:
        words = self.text_to_words(text)
        self.cleaned_words = self.clean_words(words)
        return self.cleaned_words
