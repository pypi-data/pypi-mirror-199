import os

from ..utils.data import load_json
from ..tokenizers.tokenizers import MeCabBPE, NLTKwtBPE, NLTKwptBPE


def select_tokenizer(version):
    config_path = os.path.join(os.path.dirname(__file__), "../data", version, "config.json")
    config = load_json(config_path)

    codes_path = os.path.join(os.path.dirname(__file__), "../data", version, "codes.txt")
    vocab_path = os.path.join(os.path.dirname(__file__), "../data", version, "vocab.json")

    return eval(config["tokenizer_cls"])(codes_path, vocab_path)
