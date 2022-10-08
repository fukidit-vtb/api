from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers.models.roberta.modeling_roberta import RobertaForMaskedLM
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
import pandas as pd
import numpy as np
import torch
import torch.nn.functional as F

device = torch.device('cpu')

tokenizer_RabotaRu = AutoTokenizer.from_pretrained("RabotaRu/HRBert-mini",
                                                   low_memory=True)
model_RabotaRu = AutoModelForMaskedLM.from_pretrained("RabotaRu/HRBert-mini",
                                                      low_cpu_mem_usage=True)
model_RabotaRu = model_RabotaRu.eval()

df = pd.read_feather("rabota_interfax_vac_news.feather")


class NewsSearcher:
    def __init__(
            self,
            dataframe: pd.DataFrame,
            model: RobertaForMaskedLM,
            tokenizer: PreTrainedTokenizerFast,
            device_: str = "cpu"):
        self.dataframe = dataframe.drop(["embeddings_text"], axis=1)

        embeddings = dataframe["embeddings_text"].to_list()
        self.embeddings = torch.from_numpy(np.stack(embeddings)).to(device_)

        self.model = model
        self.tokenizer = tokenizer
        self.device = device_

    def encode_text(self, query: str):
        encoded = self.tokenizer(
            query,
            padding=True,
            max_length=300,
            truncation=True,
            return_tensors='pt')
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
        return results["text"].to_list()[:10][:3]


search_instance = NewsSearcher(df, model_RabotaRu, tokenizer_RabotaRu, device)
