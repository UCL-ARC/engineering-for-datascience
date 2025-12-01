# This script exports the FashionMNIST datasets into PGMs so they can be imported into non-PyTorch programs.

from imageio import writepgm

def ensure_directories(output_directories = ['train', 'test']):
    import os
    for a in output_directories:
        os.makedirs(a, exist_ok=True)

def export_sets():
    import torch, torchvision
    dataset_names = ['train', 'test']
    classes = ("T-shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot")
    ensure_directories(dataset_names)

    datasets = {}
    datasets["train"] = torchvision.datasets.FashionMNIST("data/", transform=torchvision.transforms.ToTensor(), download=True, train=True)
    datasets["test"] = torchvision.datasets.FashionMNIST("data/", transform=torchvision.transforms.ToTensor(), download=True, train=False)

    for dataset in dataset_names:
        index = 0
        for element in datasets[dataset]:
            image = element[0][0]
            category = classes[element[1]]

            filename = f"{dataset}/{index}.pgm"
            print(f"Writing out {filename}")
            writepgm(image, filename, category)
            index += 1


if __name__ == "__main__":
    export_sets()



