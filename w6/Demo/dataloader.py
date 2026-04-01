import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import numpy as np
from PIL import Image


# Fake an image dataloader/dataset

class FakeImageDataset(Dataset):
    def __init__(self, num_samples, transform=None):
        self.num_samples = num_samples
        self.image_paths = [f"image_{i}.jpg" for i in range(num_samples)]
        self.image_lables = [np.random.randint(0,2) for _ in range(num_samples)]
        self.transform = transform

    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # get the image path and label
        image_path = self.image_paths[idx]
        image_label = self.image_lables[idx]

        # Load the image to a tensor
        image = Image.fromarray(np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8))

        if self.transform:
            image = self.transform(image)

        # Convert the label to a tensor
        return image, torch.tensor(image_label, dtype=torch.float32)

def dataloaderDemo():
    print()
    print(" -- Dataloader Demo -- ")

    # Transform the data to make the most of it
    # torvision can supply some helper functions for this!
    custom_transforms = transforms.Compose([
        # resize the image to 32x32 pxl
        transforms.Resize((32, 32)),

        # Flip the image
        #transforms.HorizontalFlip(),
        # Randomly flip the image half the time
        transforms.RandomHorizontalFlip(p=0.5),

        # Convert the image to a tensor
        transforms.ToTensor(),

        # Normalize the image
        # normalized from 0-1, to -1 to 1
        # transforms.Normalize(mean, std)
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    print()
    print(" -- Instantiate the Dataset -- ")

    dataset = FakeImageDataset(num_samples=30, transform=custom_transforms)
    print({'Length of dataset': len(dataset)})

    img, label = dataset[0]
    print()
    print({'Image shape': img.shape})
    print({'Label': label})


    print()
    print(" -- Instantiate the Dataloader -- ")

    dataloader = DataLoader(
        dataset=dataset,
        batch_size=4, # grouping 4 images at a time into a thick tensor to pass to the GPU (we hope)
        shuffle=True, # randomize the order of the images
        num_workers=4 # use 4 workers to load the images in parallel - throretically: you can pass tensors to the GPU while the cpu is gethering the next batch 
    )

    print()
    print(" -- Iterate over Epochs --")
    epochs = 3
    for epoch in range(epochs):
        print(f"Epoch {epoch}")

        # the loader automatically calls the getitem method, and stacks the image and labes into tensors
        for batch_inx, (images, labels) in enumerate(dataloader):
            print(f"Batch {batch_inx}")
            print(f"Images shape: {images.shape}")
            print(f"Labels shape: {labels.shape}")

if __name__ == "__main__":
    dataloaderDemo()