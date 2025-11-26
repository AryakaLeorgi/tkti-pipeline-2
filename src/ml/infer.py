import json
import torch
from .model import PipelineDiagnosisModel


def infer(text_emb, graph_emb):
    model = PipelineDiagnosisModel()
    model.load_state_dict(torch.load("data/model.pth"))
    model.eval()

    with torch.no_grad():
        out = model(text_emb, graph_emb)
        probs = torch.softmax(out, dim=-1)
        category = int(torch.argmax(probs))
        confidence = float(torch.max(probs))

    return category, confidence
