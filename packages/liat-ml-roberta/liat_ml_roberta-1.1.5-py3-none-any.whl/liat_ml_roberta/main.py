import os

from transformers import RobertaModel, RobertaConfig

from .tokenizers import select_tokenizer
from .utils.data import load_json


class RoBERTaTokenizer:
    @staticmethod
    def from_pretrained(model_name):
        return select_tokenizer(model_name)


class RoBERTaModel:
    @staticmethod
    def from_pretrained(model_name, config=None):
        meta_config_path = os.path.join(os.path.dirname(__file__), "data", model_name, "config.json")
        meta_config = load_json(meta_config_path)
        return RobertaModel.from_pretrained(meta_config["transformers_name"], config=config)


class RoBERTaConfig:
    @staticmethod
    def from_pretrained(model_name):
        meta_config_path = os.path.join(os.path.dirname(__file__), "data", model_name, "config.json")
        meta_config = load_json(meta_config_path)
        return RobertaConfig.from_pretrained(meta_config["transformers_name"])
