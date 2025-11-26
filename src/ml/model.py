import torch
import torch.nn as nn
import torch.nn.functional as F

class TinyTextEncoder(nn.Module):
    def __init__(self, vocab=5000, dim=128):
        super().__init__()
        self.embed = nn.Embedding(vocab, dim)
        self.fc = nn.Linear(dim, dim)

    def forward(self, tokens):
        x = self.embed(tokens).mean(dim=1)
        return F.relu(self.fc(x))

class SimpleGNN(nn.Module):
    def __init__(self, dim=128):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.fc2 = nn.Linear(dim, dim)

    def forward(self, node_feats, adj):
        x = F.relu(self.fc1(node_feats))
        x = adj @ x
        x = F.relu(self.fc2(x))
        return x.mean(dim=0)

class PipelineDiagnosisModel(nn.Module):
    def __init__(self, text_dim=128, graph_dim=128, hidden=256):
        super().__init__()
        self.text = TinyTextEncoder()
        self.classifier = nn.Sequential(
            nn.Linear(text_dim + graph_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 5)  # 5 categories
        )

    def forward(self, text_emb, graph_emb):
        x = torch.cat([text_emb, graph_emb], dim=-1)
        return self.classifier(x)
