import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DATA_DEFAULT = "nn/data/default"
DATA_ALIGNED = "nn/data/aligned"
