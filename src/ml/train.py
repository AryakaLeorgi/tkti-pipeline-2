import json
import torch
from torch.optim import Adam
from model import PipelineDiagnosisModel

def load_data(path="data/samples.jsonl"):
    samples = []
    with open(path) as f:
        for line in f:
            samples.append(json.loads(line))
    return samples

def train():
    model = PipelineDiagnosisModel()
    opt = Adam(model.parameters(), lr=1e-3)

    data = load_data()

    for epoch in range(5):
        for s in data:
            text_emb = torch.tensor(s["input"]["text_vector"])
            graph_emb = torch.tensor(s["input"]["graph_vector"])
            y = torch.tensor(s["label"]["category"])

            pred = model(text_emb, graph_emb)
            loss = torch.nn.CrossEntropyLoss()(pred.unsqueeze(0), y.unsqueeze(0))

            opt.zero_grad()
            loss.backward()
            opt.step()

        print(f"Epoch {epoch} done")

    torch.save(model.state_dict(), "data/model.pth")

if __name__ == "__main__":
    train()
