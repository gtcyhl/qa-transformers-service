from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from qa_db import fetch_data_from_mysql

model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
cache_dir = "model/sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

class QA_MODEL:

    def __init__(self):
        self.model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
        self.tokenizer =  AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

        self.docs = fetch_data_from_mysql()
        self.doc_emb = self.encode(self.docs)

    def query_doc(self, query):
        query_emb = self.encode(query)
        scores = torch.mm(query_emb, self.doc_emb.transpose(0, 1))[0].cpu().tolist()
        doc_score_pairs = list(zip(self.docs, scores))
        doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)
        return doc_score_pairs[0]
    
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    

    def encode(self, texts):
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input, return_dict=True)
        embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings
    
 

