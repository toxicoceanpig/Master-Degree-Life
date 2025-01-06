import torch
import torchvision
from torch._numpy.random import random
from torch.optim import lr_scheduler
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
import matplotlib.pyplot as plt
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, random_split
from PIL import Image
import random
import os

# 配置设备
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# transformer = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.RandomHorizontalFlip(p=0.5),
#     transforms.RandomRotation(30),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# def show_image_before_and_after(data_dir, transformer):
#     # 随机选择一张图片
#     class_dirs = os.listdir(data_dir)
#     class_dir = random.choice(class_dirs)
#     class_path = os.path.join(data_dir, class_dir)
#     image_name = random.choice(os.listdir(class_path))
#     image_path = os.path.join(class_path, image_name)
#
#     # 加载原始图片
#     original_image = Image.open(image_path).convert("RGB")
#
#     # 处理图片
#     processed_image = transformer(original_image)
#
#     # 转换处理后的图片为可显示的格式
#     processed_image = processed_image.permute(1, 2, 0).numpy()  # 转换维度
#     processed_image = processed_image * [0.229, 0.224, 0.225] + [0.485, 0.456, 0.406]  # 反归一化
#     processed_image = processed_image.clip(0, 1)  # 限制值的范围在 [0, 1]
#
#     # 显示图片
#     fig, axes = plt.subplots(1, 2, figsize=(10, 5))
#     axes[0].imshow(original_image)
#     axes[0].set_title("Original Image")
#     axes[0].axis("off")
#
#     axes[1].imshow(processed_image)
#     axes[1].set_title("Processed Image")
#     axes[1].axis("off")
#
#     plt.tight_layout()
#     plt.show()


# 1. 数据处理模块
def get_data_loaders(data_dir, batch_size=64, val_split=0.2):
    transformer = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(30),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = ImageFolder(data_dir, transform=transformer)
    train_size = int((1 - val_split) * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


# 2. 模型定义模块
def get_model(num_classes=5):
    model = models.resnet18()
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(model.fc.in_features, num_classes)
    )
    return model.to(device)


# 3. 训练与验证模块
def train_one_epoch(model, train_loader, criterion, optimizer):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)
    epoch_loss = running_loss / len(train_loader.dataset)
    return epoch_loss


def validate(model, val_loader, criterion):
    model.eval()
    correct = 0
    total = 0
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    val_loss /= len(val_loader.dataset)
    return val_loss, accuracy


# 4. 模型保存与加载模块
def save_model(model, optimizer, epoch, path="model_checkpoint.pth"):
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)


def load_model(model, optimizer, path="model_checkpoint.pth"):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch']
    return model, optimizer, start_epoch

# 5. 主训练循环
def main(data_dir='flowers', num_epochs=2, batch_size=64, learning_rate=0.001, checkpoint_path="model_checkpoint.pth"):
    train_loader, val_loader = get_data_loaders(data_dir, batch_size)
    model = get_model()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 设置学习率调度器，每 5 个 epoch 将学习率乘以 0.1
    scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

    # 如果存在检查点文件，加载上次训练的结果
    start_epoch = 0
    if os.path.exists(checkpoint_path):
        model, optimizer, start_epoch = load_model(model, optimizer, checkpoint_path)
        print(f"Loaded checkpoint from epoch {start_epoch}")

    # 确保从上次的 epoch 开始，训练到指定的总 epoch 数
    end_epoch = start_epoch + num_epochs

    for epoch in range(start_epoch, end_epoch):
        train_loss = train_one_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_accuracy = validate(model, val_loader, criterion)

        print(f'Epoch {epoch + 1}/{end_epoch}, '
              f'Train Loss: {train_loss:.4f}, '
              f'Validation Loss: {val_loss:.4f}, '
              f'Validation Accuracy: {val_accuracy:.2f}%')

        # 更新学习率
        scheduler.step()
        # 每个 epoch 后保存模型
        save_model(model, optimizer, epoch + 1, checkpoint_path)


# 执行训练
if __name__ == "__main__":
    # show_image_before_and_after('flowers', transformer)
    main()