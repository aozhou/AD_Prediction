import torch
import torch.nn as nn
import torch.nn.functional as F

class Sideway(nn.Module):

	def __init__(self, features):
		super(Sideway, self).__init__()
		self.bn = nn.BatchNorm3d(num_features = features)
		self.conv = nn.Conv3d(  in_channels = features,
								out_channels = features,
								kernel_size = 3,
								stride = 1,
								padding = 1)
	def forward(self, out):
		out = F.relu(self.bn(out))
		out = F.relu(self.bn(self.conv(out)))
		out = self.conv(out)

class ResNet(nn.Module):

	def __init__(self):
		super(ResNet, self).__init__()
		self.conv1 = nn.Conv3d( in_channels = 32,
								out_channels = 32,
								kernel_size = 3,
								stride = 1,
								padding = 1)
		self.bn1 = nn.BatchNorm3d( num_features = 32)
		self.conv2 = nn.Conv3d( in_channels = 64,
								out_channels = 64,
								kernel_size = 3,
								stride = 2,
								padding = 1)
		self.sideway1 = Sideway(features = 64)
		self.bn2 = nn.BatchNorm3d(num_features = 64)
		self.conv3 = nn.Conv3d( in_channels =64,
								out_channels = 128,
								kernel_size = 3,
								stride = 2,
								padding =1)
		self.sideway2 = Sideway(features = 128)
		self.pool = nn.MaxPool3d(	kernel_size = 7,
								stride = 1)
		self.fc1 = nn.Linear(in_features = 216, 
							 out_features = 128)
		self.fc2 = nn.Linear(in_features = 128,
							 out_features = 2)
		self.softmax = nn.Softmax()


	def forward(self, out):
		out = F.relu(self.bn1(self.conv1(out)))
		out = F.relu(self.bn1(self.conv1(out)))
		out = self.conv2(out)
		out_s = self.sideway1(out)
		out += out_s
		out_s = self.sideway1(out)
		out += out_s
		out = F.relu(self.bn2(out))
		out = self.conv2(out)
		out_s = self.sideway1(out)
		out += out_s
		out_s = self.sideway1(out)
		out += out_s
		out = F.relu(self.bn2(out))
		out = conv3(out)
		out_s = self.sideway2(out)
		out += out_s
		out_s = self.sideway2(out)
		out += out_s 
		out = self.pool(out)
		out = F.relu(self.fc1(out))
		out = self.softmax(self.fc2(out))
