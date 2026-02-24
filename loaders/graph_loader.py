import os
import json
import torch
import torch_geometric
from torch_geometric.data import Data, InMemoryDataset

# ---- FIX: Allow PyG classes to load in PyTorch 2.6 ----
torch.serialization.add_safe_globals([
    torch_geometric.data.data.Data,
    torch_geometric.data.data.DataEdgeAttr
])

class CryptoGraphDataset(InMemoryDataset):
    def __init__(self, root="data/", transform=None, pre_transform=None):
        self.root = root
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0], weights_only=False)

    @property
    def raw_file_names(self):
        return ["graphs.json"]

    @property
    def processed_file_names(self):
        return ["graphs.pt"]

    def download(self):
        pass

    def process(self):
        raw_path = self.raw_paths[0]
        with open(raw_path, "r") as f:
            graphs = json.load(f)

        data_list = []

        for g in graphs:
            x = torch.tensor(g["node_features"], dtype=torch.float)
            edge_index = torch.tensor(g["edges"], dtype=torch.long).t().contiguous()
            y = torch.tensor([g["label"]], dtype=torch.long)

            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)

        torch.save(self.collate(data_list), self.processed_paths[0])
