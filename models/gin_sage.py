import torch
import torch.nn as nn
from torch_geometric.nn import GINConv, SAGEConv, global_mean_pool

class CryptoGNN(nn.Module):
    def __init__(self, num_features=8, num_classes=3):
        super().__init__()

        # --- GIN Layer ---
        self.gin = GINConv(
            nn.Sequential(
                nn.Linear(num_features, 64),
                nn.ReLU(),
                nn.Linear(64, 64)
            )
        )

        # --- GraphSAGE Layer ---
        self.sage = SAGEConv(64, 64)

        # --- Normalization ---
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(64)

        # --- Classifier ---
        self.classifier = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, num_classes)
        )

    def forward(self, x, edge_index, batch):
        # GIN
        x = torch.relu(self.bn1(self.gin(x, edge_index)))

        # GraphSAGE
        x = torch.relu(self.bn2(self.sage(x, edge_index)))

        # Global pooling (graph-level)
        x = global_mean_pool(x, batch)

        # Predict class
        return self.classifier(x)
