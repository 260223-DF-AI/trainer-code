import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

class ResNetBlock(nn.Module): # mayhaps, a ResNet exists???
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResNetBlock, self).__init__()

        # Conv2d is a 2D convolution layer, finding features in an image
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)

        # BatchNorm2d is a batch normalization layer, normalizing to 2d
        # normalizing 4d batches of 2d
        self.bn1 = nn.BatchNorm2d(out_channels)

        # ReLu is a rectified linear unit, learning the non-linearity
        self.relu = nn.ReLU(inplace=True)

        # Conv2d is another 2D convolution layer - refining the features
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)

        # BatchNorm2d is another batch normalization layer
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()

        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        
    def forward(self, x):
        identity = self.shortcut(x)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        out += identity
        out = self.relu(out)

        return out


def visualize(image_tensor):
    # using a sample image, run a single convolution
    conv_layer = nn.Conv2d(in_channels=3, out_channels=4, kernel_size=3, padding=1)

    feature_map = conv_layer(image_tensor)
    print(f"feature map: {feature_map.shape}")
    # torch.size([1,4,224,224])
        # batch , features/filters, height, width

    pool = nn.MaxPool2d(kernel_size=2, stride=2)
    feature_map = pool(feature_map)
    print(f"pooled feature map: {feature_map.shape}") 
    # torch.size([1,4,112,112]


def RunRezNet(image_tensor):

    print(F"image tensor shape: {image_tensor.shape}")
    # image_tensor = nn.Flatten()(image_tensor) DONT FLATTEN when you're sending it to a conv2d layer
    block = ResNetBlock(in_channels=3, out_channels=128, stride=2)
    out = block(image_tensor)

    print(f"result shape: {out.shape}")
    # torch.size([1,128,112,112])


def main(): 
    preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
    raw_image = Image.open("./../Notes/img_0_403.jpg").convert("RGB")
    image_tensor = preprocess(raw_image).unsqueeze(0)

    #visualize(image_tensor)
    RunRezNet(image_tensor)


if __name__ == "__main__":
    main()

