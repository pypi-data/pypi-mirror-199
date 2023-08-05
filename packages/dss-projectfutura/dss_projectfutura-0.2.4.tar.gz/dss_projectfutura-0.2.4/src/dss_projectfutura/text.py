from tokenizer import Tokenizer
from model import Model
import brotli

# Tokenizer built for representing text,
# limited to a set of defined tokens
# has extrapolation (token speculation) support
class TextTokenizer(Tokenizer):
    tokens = []
    indexes = {}

    def __init__(self, extrapolate=False):
        self.extrapolate = extrapolate

    def __words__(self, text):
        words = text.replace('\n', ' ').replace('\t', ' ').replace('?', ' ? ').lower().split(' ')
        return [ w for w in words if w.strip() != '' ]

    def adapt(self, text):
        words = self.__words__(text)
        for w in words:
            if w.strip() not in self.tokens:
                self.indexes[w.strip()] = len(self.tokens)
                self.tokens.append(w.strip())

    def load(self, bindata):
        self.tokens = brotli.decompress(bindata).decode('utf-8').split('\x00')
        for i, tok in enumerate(self.tokens):
            self.indexes[tok] = i

    def dump(self):
        return brotli.compress('\x00'.join(self.tokens).encode('utf-8'), mode=brotli.MODE_GENERIC, quality=6)

    def encode(self, text, fast=False):
        words = self.__words__(text)
        return [ self.indexes[w.strip()] for w in words if w.strip() in self.indexes ]

    def decode(self, tokens):
        return ' '.join([ self.tokens[x] for x in tokens ])

# Model built for completing text
class TextModel(Model):
    pass
