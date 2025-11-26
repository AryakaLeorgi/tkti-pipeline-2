import json
import torch
from ml.model import PipelineDiagnosisModel
from ml.utils import tokenize_to_vector, graph_features_to_vector


def infer(g, feats, description: str):
    # 1. Convert text -> vector -> tensor
    text_vec = tokenize_to_vector(description)
    text_emb = torch.tensor(text_vec, dtype=torch.float32).unsqueeze(0)

    # 2. Convert graph features -> vector -> tensor
    graph_vec = graph_features_to_vector(feats)
    graph_emb = torch.tensor(graph_vec, dtype=torch.float32).unsqueeze(0)

    # 3. Load model
    model = PipelineDiagnosisModel()
    model.load_state_dict(torch.load("data/model.pth"))
    model.eval()

    # 4. Inference
    with torch.no_grad():
        out = model(text_emb, graph_emb)
        probs = torch.softmax(out, dim=-1)
        category = int(torch.argmax(probs))
        confidence = float(torch.max(probs))

    # 5. Return JSON text (main.py expects a string)
    return json.dumps({
        "category": category,
        "confidence": confidence,
        "description_used": description
    }, indent=2)
