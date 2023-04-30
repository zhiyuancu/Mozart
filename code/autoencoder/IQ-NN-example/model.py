import torch
import torch.nn as nn


class pixelWise(nn.Module):
    def __init__(self, in_channels=6):
        super(pixelWise, self).__init__()
        self.lin1 = nn.Linear(in_features=in_channels, out_features=in_channels*2)
        self.lin2 = nn.Linear(in_features=in_channels*2, out_features=in_channels*4)
        self.lin3 = nn.Linear(in_features=in_channels*4, out_features=in_channels*2)
        self.lin4 = nn.Linear(in_features=in_channels*2, out_features=in_channels)
        self.lin5 = nn.Linear(in_features=in_channels, out_features=1)

    def forward(self, x):
        x = nn.ReLU(self.lin1(x))
        x = nn.ReLU(self.lin2(x))
        x = nn.ReLU(self.lin3(x))
        x = nn.ReLU(self.lin4(x))
        x = nn.ReLU(self.lin5(x))
        return x


class Net(nn.Module):
    def __init__(self, in_channels=2, out_channels=1, layers=1):
        super(Net, self).__init__()
        self.cin = in_channels
        self.cout = out_channels
        self.conv1 = nn.Conv2d(in_channels, in_channels, kernel_size=1, bias=True)
        self.conv2 = nn.Conv2d(in_channels, in_channels, kernel_size=1, bias=True)
        self.conv3 = nn.Conv2d(in_channels, in_channels, kernel_size=1, bias=True)
        self.conv4 = nn.Conv2d(in_channels, 1, kernel_size=1, bias=True)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        x = self.sigmoid(self.conv4(x))
        return x


class EncoderNet(nn.Module):
    def __init__(self, in_channels=2, out_channels=1, layers=1):
        super(EncoderNet, self).__init__()

        self.en_conv = nn.Sequential(
            nn.Conv2d(in_channels, 8, kernel_size=3, padding=1, bias=True),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),

            nn.Conv2d(8, 16, kernel_size=3, padding=1, bias=True),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),

            nn.Conv2d(16, 32, kernel_size=3, padding=1, bias=True),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),

            )

        self.pool = nn.MaxPool2d(2, 2)

        self.de_conv = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, bias=True),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),

            nn.ConvTranspose2d(16, 8, kernel_size=3, padding=1, bias=True),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),

            nn.ConvTranspose2d(8, out_channels, kernel_size=4, padding=1, bias=True),
            nn.ReLU(inplace=True),

            )

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):

        x = self.en_conv(x)
        # print(x.shape)
        x = self.pool(x)
        # print(x.shape)
        x = self.de_conv(x)
        x = self.sigmoid(x)
        # print(x.shape)

        return x


