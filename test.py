import torch

# 检查 MPS 是否可用
print("MPS Available:", torch.backends.mps.is_available())

# 选择设