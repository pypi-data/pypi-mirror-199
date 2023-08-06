# liat_ml_roberta
RoBERTa trained on Wikipedia Dump.

## How to install

Can use pip to install.

~~~bash
pip install liat_ml_roberta
~~~

## How to use

The loaded models and configurations can be used in the same way as [transformers.roberta](https://huggingface.co/docs/transformers/model_doc/roberta).

~~~python
from liat_ml_roberta import RoBERTaTokenizer


def main():
    tokenizer = RoBERTaTokenizer.from_pretrained(version="en_20190121_m10000_v24000_base")
    print(tokenizer.tokenize("This is a pen."))

    config = RoBERTaConfig.from_pretrained("roberta_base_en_20190121_m10000_v24000_u125000")
    model = RoBERTaModel.from_pretrained("roberta_base_en_20190121_m10000_v24000_u125000", config=config)


if __name__ == "__main__":
    main()
~~~

## Models

|name|lang|size|bpe merges|vocab size|updates|wikipedia version|  
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|  
|roberta_base_ja_20190121_m10000_v24000_u125000|ja|roberta-base|10000|24000|125000|20190121|  
|roberta_base_ja_20190121_m10000_v24000_u500000|ja|roberta-base|10000|24000|500000|20190121|  
|roberta_base_en_20190121_m10000_v24000_u125000|en|roberta-base|10000|24000|125000|20190121|  
|roberta_base_en_20190121_m10000_v24000_u500000|en|roberta-base|10000|24000|500000|20190121|  
|roberta_base_fr_20190121_m10000_v24000_u500000|fr|roberta-base|10000|24000|500000|20190121|  
|roberta_base_de_20190121_m10000_v24000_u500000|de|roberta-base|10000|24000|500000|20190121|  
