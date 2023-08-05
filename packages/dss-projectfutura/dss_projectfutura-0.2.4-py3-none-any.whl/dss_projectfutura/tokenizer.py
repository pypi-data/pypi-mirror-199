# The base class for a Tokenizer
# Methods are used to convert input to tokens through it
class Tokenizer:
    def adapt(self, inp):
        pass

    def load(self, bindata):
        pass

    def dump(self):
        return b''

    def encode(self, inp, fast=False):
        return inp

    def decode(self, tokens):
        return tokens


