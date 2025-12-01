import torch
import torchvision
from tqdm import tqdm
import onnx
import onnxruntime
import numpy

import time
import json

timing = {}
timing["training"] = {}
timing["inference"] = {}

train_dataset = torchvision.datasets.FashionMNIST("data/", transform=torchvision.transforms.ToTensor(), download=True, train=True)
test_dataset = torchvision.datasets.FashionMNIST("data/", transform=torchvision.transforms.ToTensor(), download=True, train=False)

classes = ("T-shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# Model structure from Graphcore example
class ClassificationModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(1, 5, 3)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(5, 12, 5)
        self.norm = torch.nn.GroupNorm(3, 12)
        self.fc1 = torch.nn.Linear(972, 100)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(100, 10)
        self.log_softmax = torch.nn.LogSoftmax(dim=1)
        self.loss = torch.nn.NLLLoss()

    def forward(self, x, labels=None):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.norm(self.relu(self.conv2(x)))
        x = torch.flatten(x, start_dim=1)
        x = self.relu(self.fc1(x))
        x = self.log_softmax(self.fc2(x))

        return x

model = ClassificationModel()

train_dataloader = torch.utils.data.DataLoader(
    train_dataset, batch_size=16, shuffle=True, num_workers=20
)

optimiser = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()

timing["training"]["start"] = time.time()

model = model.to(device)

epochs = 5
for epoch in tqdm(range(epochs), desc="epochs"):
    epoch_start = time.time()
    model.train()
    for images, labels in train_dataloader:
        images, labels = images.to(device), labels.to(device)
        optimiser.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimiser.step()
    epoch_finish = time.time()
    timing["training"][f"epoch_{epoch}"] = epoch_finish - epoch_start

cpu_model = model.to("cpu")

timing["training"]["finish"] = time.time()
timing["training"]["duration"] = timing["training"]["finish"] - timing["training"]["start"] 

torch.save(cpu_model.state_dict(), "fashion_classifier.pth")

print("\nDoing Inference... \n")

timing["inference"]["start"] = time.time()
model = model.eval()

test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=32, num_workers=10)

predictions, labels = [], []
for data, label in test_dataloader:
    predictions += model(data).data.max(dim=1).indices
    labels += label

timing["inference"]["finish"] = time.time()
timing["inference"]["duration"] = timing["inference"]["finish"] - timing["inference"]["start"] 

count_samples = len(labels)
correct = 0

for a in range(count_samples):
    if labels[a] == predictions[a]:
        correct += 1
    print(f"Label: {classes[labels[a]]} Prediction: {classes[predictions[a]]}")

percentage = 100 * (correct/count_samples)

print("\nThe Famous Ankle Boot Test!\n")

x, y = test_dataset[0][0], test_dataset[0][1]

from termshow import show, ANSI_COLOURS

print('Image:')
show(x[0], colours=ANSI_COLOURS)

print(f"Label: {classes[labels[0]]} Prediction: {classes[predictions[0]]}")
print(f"Prediction accuracy over test set: {percentage}% ({count_samples} images)")

# ONNX
gibberish = torch.randn(1, 1, 28, 28, requires_grad=True)
torch_gibberish = cpu_model(gibberish)
onnx_file = "fashion_classifier.onnx"
onnx_out_model = torch.onnx.export(cpu_model, 
                               gibberish,
                               onnx_file,
                               export_params=True,
                               input_names = ['input'],                       # the model's input names
                               output_names = ['output'],                     # the model's output names
                               dynamic_shapes={'input' : {0 : torch.export.Dim('batch_size')},    # variable length axes
                                             'output' : {0 : torch.export.Dim('batch_size')}})

print("Checking with ONNX")

onnx_model = onnx.load(onnx_file)

print("Checking with ONNX Runtime")

ort_session = onnxruntime.InferenceSession(onnx_file, providers=["CPUExecutionProvider"])

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

# compute ONNX Runtime output prediction
ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(gibberish)}
ort_outs = ort_session.run(None, ort_inputs)

# compare ONNX Runtime and PyTorch results
numpy.testing.assert_allclose(to_numpy(torch_gibberish), ort_outs[0], rtol=1e-03, atol=1e-05)

print("Exported model has been tested with ONNXRuntime, and the result looks good!")

print(json.dumps(timing, indent=4))
