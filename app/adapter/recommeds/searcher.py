from transformers import (
    AutoTokenizer,
    AutoModelForMaskedLM,
    T5ForConditionalGeneration,
    T5Tokenizer,
)
from transformers.models.roberta.modeling_roberta import RobertaForMaskedLM
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
from transformers import set_seed
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F

device = torch.device("cpu")

tokenizer_RabotaRu = AutoTokenizer.from_pretrained("RabotaRu/HRBert-mini",
                                                   low_memory=True)
model_RabotaRu = AutoModelForMaskedLM.from_pretrained("RabotaRu/HRBert-mini",
                                                      low_cpu_mem_usage=True)
model_RabotaRu = model_RabotaRu.eval()

news_df = pd.read_feather("rabota_interfax_vac_news.feather")
inside_df = pd.read_feather("tinkoff_invest_emb.feather")

MODEL_NAME = 'cointegrated/rut5-base-absum'
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model.eval()


def summarize(
        text, n_words=10, compression=None,
        max_length=150, num_beams=3, do_sample=False, repetition_penalty=10.0,
        **kwargs
):
    set_seed(42)
    if n_words:
        text = '[{}] '.format(n_words) + text
    elif compression:
        text = '[{0:.1g}] '.format(compression) + text
    x = tokenizer(text, return_tensors='pt', padding=True).to(model.device)
    with torch.inference_mode():
        out = model.generate(
            **x,
            max_length=max_length, num_beams=num_beams,
            do_sample=do_sample, repetition_penalty=repetition_penalty,
            **kwargs
        )
    return tokenizer.decode(out[0], skip_special_tokens=True)


class SearchAdapter:
    def __init__(
            self,
            dataframe: pd.DataFrame,
            model_: RobertaForMaskedLM,
            tokenizer_: PreTrainedTokenizerFast,
            device_: str = "cpu"):
        self.dataframe = dataframe.drop(["embeddings_text"], axis=1)

        embeddings = dataframe["embeddings_text"].to_list()
        self.embeddings = torch.from_numpy(np.stack(embeddings)).to(device_)

        self.model = model_
        self.tokenizer = tokenizer_
        self.device = device_

    def encode_text(self, query: str):
        encoded = self.tokenizer(
            query,
            padding=True,
            max_length=300,
            truncation=True,
            return_tensors="pt")
        return encoded.to(self.device)

    def encode_model(self, encoded):
        with torch.no_grad():
            outputs = self.model.roberta(**encoded).last_hidden_state.mean(-2)
        return outputs

    def search(self, query: str) -> list:
        encoded = self.encode_text(query)
        outputs = self.encode_model(encoded)

        self.dataframe["similarity"] = F.cosine_similarity(
            outputs,
            self.embeddings) \
            .detach() \
            .cpu() \
            .numpy()
        results = self.dataframe.sort_values(by="similarity", ascending=False)
        return results["text"].to_list()


digest_instance = SearchAdapter(news_df, model_RabotaRu, tokenizer_RabotaRu,
                                device)

news_instance = SearchAdapter(news_df, model_RabotaRu, tokenizer_RabotaRu,
                              device)

inside_instance = SearchAdapter(inside_df, model_RabotaRu, tokenizer_RabotaRu,
                                device)
