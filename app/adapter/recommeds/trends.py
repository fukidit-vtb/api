from itertools import groupby
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pandas as pd

model_name = "0x7194633/keyt5-large"  # or 0x7194633/keyt5-base
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def get_algo_trend(df, top_n=5):
    tags = set()
    for elem in df.tags:
        tags.update(elem.split('###'))
    min_date = df.date.min()
    max_date = df.date.max()
    stat = {elem: 0 for elem in tags}
    for tag, date in zip(df.tags, df.date):
        for t in tag.split('###'):
            stat[t] += (date - min_date).days / (max_date - min_date).days
    return sorted(stat.items(), key=lambda x: -x[1])[:top_n]


def generate(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        hypotheses = model.generate(**inputs, num_beams=5, **kwargs)
    s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
    s = [el for el, _ in groupby(s)]
    return s


def get_model_trend(df, top_n=10):
    trends = set()
    df = df.sort_values(by=['date'], ascending=False).iloc[:top_n]
    for i in range(top_n):
        article = df.iloc[i].title + ' ' + df.iloc[i].text
        trends.update(generate(article, top_p=1.0, max_length=64))
    return list(trends)


news_df = pd.read_csv("assets/ml/tags.csv")
trends_items = get_model_trend(df=news_df)
