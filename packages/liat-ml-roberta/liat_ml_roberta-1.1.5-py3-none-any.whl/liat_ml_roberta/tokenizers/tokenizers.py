import codecs

from subword_nmt.apply_bpe import BPE
from janome.tokenizer import Tokenizer as JanomeTokenizer
import nltk
from nltk.tokenize import wordpunct_tokenize

from ..utils.data import load_json


class BaseTokenizer(object):
    def __init__(
        self,
        codes_path,
        vocab_path,
        cls_token="<s>",
        pad_token="<pad>",
        sep_token="</s>",
        unk_token="<unk>",
    ):
        codes = codecs.open(codes_path, encoding="utf-8")
        self.bpe = BPE(codes)

        self.vocab = load_json(vocab_path)

        self.cls_token = cls_token
        self.pad_token = pad_token
        self.sep_token = sep_token
        self.unk_token = unk_token

        self.cls_token_id = self.vocab[self.cls_token]
        self.pad_token_id = self.vocab[self.pad_token]
        self.sep_token_id = self.vocab[self.sep_token]
        self.unk_token_id = self.vocab[self.unk_token]

    def tokenize(self, text):
        raise NotImplementedError()

    def convert_token_to_id(self, token):
        return self.vocab.get(token, self.unk_token_id)

    def convert_tokens_to_ids(self, tokens):
        token_ids = [self.convert_token_to_id(token) for token in tokens]
        return token_ids


class MeCabBPE(BaseTokenizer):
    def __init__(self, codes_path, vocab_path):
        super().__init__(codes_path, vocab_path)
        self.janome = JanomeTokenizer(wakati=True)

    def tokenize(self, text):
        tokens = list(self.janome.tokenize(text))
        tokens = self.bpe.process_line(" ".join(tokens))
        return tokens.split()


class NLTKwtBPE(BaseTokenizer):
    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = self.bpe.process_line(" ".join(tokens))
        return tokens.split()


class NLTKwptBPE(BaseTokenizer):
    def tokenize(self, text):
        tokens = wordpunct_tokenize(text)
        tokens = self.bpe.process_line(" ".join(tokens))
        return tokens.split()
