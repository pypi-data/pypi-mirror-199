#!/usr/bin/env python
# coding: utf-8

# ## **树叶分类课程竞赛**
# - 首先要多谢Neko Kiku提供的baseline代码，思路非常清晰；
# - 本代码思想很简单，三个臭皮匠赛过诸葛亮，总共训练了3个优秀的模型（ResNeSt+ResNeXt+DenseNet）,最后进行集成，结果会更加鲁棒（公榜第12升到私榜第7也侧面反映了其鲁棒性）；
# - 代码是在本地计算机上跑的，由于Kaggle的运行时间有限制，无法分享运行完所有模型的结果，在这里我将我本地各个模型运行的结果附在了input文件夹里提供结果参考，以及方便走完代码整个流程；
# - 总结了图像分类任务的几个小技巧：
# 1. 数据增强：特别是CutMix和预测时候对test样本进行TTA(Test Time Augmentation);
# 2. 模型：可使用表现较好的预训练过的模型；
# 3. 优化器：使用AdamW（对于含有L2正则项的优化，如weight decay），学习率采用cosine学习率CosineAnnealingLR;
# 4. 交叉验证：使用K折交叉验证；

# In[1]:


get_ipython().system('pip install ttach')
# 安装TTA包


# In[2]:


get_ipython().system('pip install git+https://github.com/ildoonet/cutmix ')
# 安装CutMix


# In[3]:


# 安装ResNeSt模型包
get_ipython().system('pip install resnest --pre')


# In[4]:


# 导入各种包
import torch
import torch.nn as nn
from torch.nn import functional as F
import ttach as tta
from resnest.torch import resnest50

from cutmix.cutmix import CutMix
from cutmix.utils import CutMixCrossEntropyLoss

import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader, TensorDataset
from torchvision import transforms
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.model_selection import KFold
from PIL import Image
import os
import matplotlib.pyplot as plt
import torchvision.models as models
# This is for the progress bar.
from tqdm import tqdm


# ### **整理数据集**

# ### **数据读取与预处理**

# In[5]:


# 看看label文件长啥样
labels_dataframe = pd.read_csv('../input/classify-leaves/train.csv')
labels_dataframe.head(5)


# In[6]:


# 把label文件排个序
leaves_labels = sorted(list(set(labels_dataframe['label'])))
n_classes = len(leaves_labels)
print(n_classes)
leaves_labels[:10]


# In[7]:


# 把label转成对应的数字
class_to_num = dict(zip(leaves_labels, range(n_classes)))
class_to_num


# In[8]:


# 再转换回来，方便最后预测的时候使用
num_to_class = {v : k for k, v in class_to_num.items()}
num_to_class


# In[9]:


# 继承pytorch的dataset，创建自己的
class TrainValidData(Dataset):
    def __init__(self, csv_path, file_path, resize_height=224, resize_width=224, transform=None):
        """
        Args:
            csv_path (string): csv 文件路径
            img_path (string): 图像文件所在路径

        """
        
        # 需要调整后的照片尺寸，我这里每张图片的大小尺寸不一致#
        self.resize_height = resize_height
        self.resize_width = resize_width

        self.file_path = file_path
        self.to_tensor = transforms.ToTensor() #将数据转换成tensor形式
        self.transform = transform

        # 读取 csv 文件
        # 利用pandas读取csv文件
        self.data_info = pd.read_csv(csv_path, header=None)  #header=None是去掉表头部分
        # 文件第一列包含图像文件名称
        self.image_arr = np.asarray(self.data_info.iloc[1:,0]) #self.data_info.iloc[1:,0]表示读取第一列，从第二行开始一直读取到最后一行
        # 第二列是图像的 label
        self.label_arr = np.asarray(self.data_info.iloc[1:,1])
        # 计算 length
        self.data_len = len(self.data_info.index) - 1

    def __getitem__(self, index):
        # 从 image_arr中得到索引对应的文件名
        single_image_name = self.image_arr[index]

        # 读取图像文件
        img_as_img = Image.open(self.file_path + single_image_name)
        
        #如果需要将RGB三通道的图片转换成灰度图片可参考下面两行
        # if img_as_img.mode != 'L':
        #     img_as_img = img_as_img.convert('L')
        
        #设置好需要转换的变量，还可以包括一系列的nomarlize等等操作
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])
        img_as_img = transform(img_as_img)

        # 得到图像的 label
        label = self.label_arr[index]
        number_label = class_to_num[label]

        return (img_as_img, number_label)  #返回每一个index对应的图片数据和对应的label

    def __len__(self):
        return self.data_len


# In[10]:


# 继承pytorch的dataset，创建自己的
class TestData(Dataset):
    def __init__(self, csv_path, file_path, resize_height=224, resize_width=224, transform = None):
        """
        Args:
            csv_path (string): csv 文件路径
            img_path (string): 图像文件所在路径

        """
        
        # 需要调整后的照片尺寸，我这里每张图片的大小尺寸不一致#
        self.resize_height = resize_height
        self.resize_width = resize_width

        self.file_path = file_path
        self.transform = transform
        self.to_tensor = transforms.ToTensor() #将数据转换成tensor形式

        # 读取 csv 文件
        # 利用pandas读取csv文件
        self.data_info = pd.read_csv(csv_path, header=None)  #header=None是去掉表头部分
        # 文件第一列包含图像文件名称
        self.image_arr = np.asarray(self.data_info.iloc[1:,0]) #self.data_info.iloc[1:,0]表示读取第一列，从第二行开始一直读取到最后一行
        # 计算 length
        self.data_len = len(self.data_info.index) - 1
        
    def __getitem__(self, index):
        # 从 image_arr中得到索引对应的文件名
        single_image_name = self.image_arr[index]

        # 读取图像文件
        img_as_img = Image.open(self.file_path + single_image_name)
        
        #如果需要将RGB三通道的图片转换成灰度图片可参考下面两行
        # if img_as_img.mode != 'L':
        #     img_as_img = img_as_img.convert('L')
        
        #设置好需要转换的变量，还可以包括一系列的nomarlize等等操作
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])
        img_as_img = transform(img_as_img)


        return img_as_img

    def __len__(self):
        return self.data_len


# In[11]:


train_transform = transforms.Compose([
    # 随机裁剪图像，所得图像为原始面积的0.08到1之间，高宽比在3/4和4/3之间。
    # 然后，缩放图像以创建224 x 224的新图像
    transforms.RandomResizedCrop(224, scale=(0.08, 1.0), ratio=(3.0 / 4.0, 4.0 / 3.0)),
    transforms.RandomHorizontalFlip(),
    # 随机更改亮度，对比度和饱和度
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4),
    # 添加随机噪声
    transforms.ToTensor(),
    # 标准化图像的每个通道
    transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])])
val_test_transform = transforms.Compose([
    transforms.Resize(256),
    # 从图像中心裁切224x224大小的图片
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])])


# In[12]:


train_val_path = '../input/classify-leaves/train.csv'
test_path = '../input/classify-leaves/test.csv'
# csv文件中已经images的路径了，因此这里只到上一级目录
img_path = '../input/classify-leaves/'

train_val_dataset = TrainValidData(train_val_path, img_path)
test_dataset = TestData(test_path, img_path, transform = val_test_transform)
print(train_val_dataset.data_info)
print(test_dataset.data_info)


# ## **基于ResNeSt模型部分**

# ### **ResNeSt模型**

# In[13]:


# 是否要冻住模型的前面一些层
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        model = model
        for param in model.parameters():
            param.requires_grad = False

# ResNeSt模型
def resnest_model(num_classes, feature_extract = False):
    model_ft = resnest50(pretrained=True)
    set_parameter_requires_grad(model_ft, feature_extract)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Sequential(nn.Linear(num_ftrs, num_classes))

    return model_ft


# In[ ]:


# 看一下是在cpu还是GPU上
def get_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'

device = get_device()
print(device)


# In[ ]:


get_ipython().system('nvidia-smi')


# In[14]:


# Configuration options
k_folds = 5
num_epochs = 30
learning_rate = 1e-4
weight_decay = 1e-3
train_loss_function = CutMixCrossEntropyLoss(True)
valid_loss_function = nn.CrossEntropyLoss()
# For fold results
results = {}

# Set fixed random number seed
torch.manual_seed(42)

# Define the K-fold Cross Validator
kfold = KFold(n_splits=k_folds, shuffle=True)


# ### **训练**

# In[ ]:


# Start print
print('--------------------------------------')

# K-fold Cross Validation model evaluation
for fold, (train_ids,valid_ids) in enumerate(kfold.split(train_val_dataset)):

  # Print
  print(f'FOLD {fold}')
  print('--------------------------------------')

  # Sample elements randomly from a given list of ids, no replacement.
  train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
  valid_subsampler = torch.utils.data.SubsetRandomSampler(valid_ids)

  # Define data loaders for training and testing data in this fold
  trainloader = torch.utils.data.DataLoader(
                      CutMix(TrainValidData(train_val_path, img_path, transform = train_transform), num_class=176, beta=1.0, prob=0.5, num_mix=2), 
                      batch_size=32, sampler=train_subsampler, num_workers=0)
  validloader = torch.utils.data.DataLoader(
                      TrainValidData(train_val_path, img_path, transform = val_test_transform),
                      batch_size=32, sampler=valid_subsampler, num_workers=0)
  
  # Initialize a model and put it on the device specified.
  model = resnest_model(176)
  model = model.to(device)
  model.device = device
  
  # Initialize optimizer
  optimizer = torch.optim.AdamW(model.parameters(),lr=learning_rate,weight_decay= weight_decay)
  scheduler = CosineAnnealingLR(optimizer,T_max=10)

  # Run the training loop for defined number of epochs
  for epoch in range(0,num_epochs):
    model.train()
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    # These are used to record information in training
    train_losses = []
    train_accs = []
    # Iterate the training set by batches
    for batch in tqdm(trainloader):
      # Move images and labels to GPU
      imgs, labels = batch
      imgs = imgs.to(device)
      labels = labels.to(device)
      # Forward the data
      logits = model(imgs)
      # Calculate loss
      loss = train_loss_function(logits,labels)
      # Clear gradients in previous step
      optimizer.zero_grad()
      # Compute gradients for parameters
      loss.backward()
      # Update the parameters with computed gradients
      optimizer.step()
      # Compute the accuracy for current batch.
      # acc = (logits.argmax(dim=-1) == labels).float().mean()
      # Record the loss and accuracy.
      train_losses.append(loss.item())
      # train_accs.append(acc)
    print("第%d个epoch的学习率：%f" % (epoch+1,optimizer.param_groups[0]['lr']))
    scheduler.step()
    # The average loss and accuracy of the training set is the average of the recorded values.
    train_loss = np.sum(train_losses) / len(train_losses)
    # train_acc = np.sum(train_accs) / len(train_accs)
    # Print the information.
    # print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}, acc = {train_acc:.5f}")
    print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}")

  # Train process (all epochs) is complete
  print('Training process has finished. Saving trained model.')
  print('Starting validation')

  # Saving the model
  print('saving model with loss {:.3f}'.format(train_loss))
  save_path = f'./model-fold-{fold}.pth'
  torch.save(model.state_dict(),save_path)
  # Start Validation
  model.eval()
  valid_losses = []
  valid_accs = []
  with torch.no_grad():
    for batch in tqdm(validloader):
      imgs, labels = batch
      # No gradient in validation
      logits = model(imgs.to(device))
      loss = valid_loss_function(logits,labels.to(device))
      acc = (logits.argmax(dim=-1) == labels.to(device)).float().mean()
      # Record loss and accuracy
      valid_losses.append(loss.item())        
      valid_accs.append(acc)
    # The average loss and accuracy
    valid_loss = np.sum(valid_losses)/len(valid_losses)
    valid_acc = np.sum(valid_accs)/len(valid_accs)
    print(f"[ Valid | {epoch + 1:03d}/{num_epochs:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f}")
    print('Accuracy for fold %d: %d' % (fold, valid_acc))
    print('--------------------------------------')
    results[fold] = valid_acc
# Print fold results
print(f'K-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS')
print('--------------------------------')
total_summation = 0.0
for key, value in results.items():
  print(f'Fold {key}: {value} ')
  total_summation += value
print(f'Average: {total_summation/len(results.items())} ')


# ### **预测**

# In[15]:


testloader = torch.utils.data.DataLoader(
                      TestData(test_path, img_path, transform = val_test_transform),
                      batch_size=32, num_workers=0)


# In[ ]:


## predict
model = resnest_model(176)

# create model and load weights from checkpoint
model = model.to(device)
# load the all folds
for test_fold in range(k_folds):
  model_path = f'./model-fold-{test_fold}.pth'
  saveFileName = f'./submission-fold-{test_fold}.csv'
  model.load_state_dict(torch.load(model_path))

  # Make sure the model is in eval mode.
  # Some modules like Dropout or BatchNorm affect if the model is in training mode.
  model.eval()
  tta_model = tta.ClassificationTTAWrapper(model, tta.aliases.five_crop_transform(200,200)) # Test-Time Augmentation

  # Initialize a list to store the predictions.
  predictions = []
  # Iterate the testing set by batches.
  for batch in tqdm(testloader):
      
      imgs = batch
      with torch.no_grad():
          logits = tta_model(imgs.to(device))
      
      # Take the class with greatest logit as prediction and record it.
      predictions.extend(logits.argmax(dim=-1).cpu().numpy().tolist())

  preds = []
  for i in predictions:
      preds.append(num_to_class[i])

  test_data = pd.read_csv(test_path)
  test_data['label'] = pd.Series(preds)
  submission = pd.concat([test_data['image'], test_data['label']], axis=1)
  submission.to_csv(saveFileName, index=False)
  print("ResNeSt Model Results Done!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# ### **ResNeSt的5折交叉验证的结果投票**

# In[ ]:


# 读取5折交叉验证的结果
df0 = pd.read_csv('./submission-fold-0.csv')
df1 = pd.read_csv('./submission-fold-1.csv')
df2 = pd.read_csv('./submission-fold-2.csv')
df3 = pd.read_csv('./submission-fold-3.csv')
df4 = pd.read_csv('./submission-fold-4.csv')


# In[ ]:


# 往第0折结果里添加数字化标签列
list_num_label0 = []
for i in df0['label']:
  list_num_label0.append(class_to_num[i])
df0['num_label0']=list_num_label0
df0.head()


# In[ ]:


# 往第1折结果里添加数字化标签列
list_num_label1 = []
for i in df1['label']:
  list_num_label1.append(class_to_num[i])
df1['num_label1']=list_num_label1
df1.head()


# In[ ]:


# 往第2折结果里添加数字化标签列
list_num_label2 = []
for i in df2['label']:
  list_num_label2.append(class_to_num[i])
df2['num_label2']=list_num_label2
df2.head()


# In[ ]:


# 往第3折结果里添加数字化标签列
list_num_label3 = []
for i in df3['label']:
  list_num_label3.append(class_to_num[i])
df3['num_label3']=list_num_label3
df3.head()


# In[ ]:


# 往第4折结果里添加数字化标签列
list_num_label4 = []
for i in df4['label']:
  list_num_label4.append(class_to_num[i])
df4['num_label4']=list_num_label4
df4.head()


# In[ ]:


# 准备整合5折的结果到同一个DataFrame
df_all = df0.copy()
df_all.drop(['label'],axis=1,inplace=True)
df_all.head()


# In[ ]:


# 整合5折的数字化标签结果到同一个DataFrame
df_all['num_label1']=list_num_label1
df_all['num_label2']=list_num_label2
df_all['num_label3']=list_num_label3
df_all['num_label4']=list_num_label4
df_all.head()


# In[ ]:


# 对df_all进行转置，方便求众数
df_all_transpose = df_all.copy().drop(['image'],axis=1).transpose()
df_all_transpose.head()


# In[ ]:


# 求得投票众数
df_mode = df_all_transpose.mode().transpose()
df_mode.head()


# In[ ]:


# 把投票结果的数字化标签转成字符串标签
voting_class = []
for each in df_mode[0]:
  voting_class.append(num_to_class[each])
voting_class


# In[ ]:


# 将投票结果的字符串标签添加到df_all中
df_all['label'] = voting_class
df_all.head()


# In[ ]:


# 提取image和label两列为最终的结果
df_submission = df_all[['image','label']].copy()
df_submission.head()


# In[ ]:


# 保存当前模型得到的最终结果
df_submission.to_csv('./submission-resnest.csv', index=False)
print('Voting results of resnest successfully saved!')


# ## **基于ResNeXt模型部分**

# ### **ResNeXt模型**

# In[ ]:


# 是否要冻住模型的前面一些层
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        model = model
        for param in model.parameters():
            param.requires_grad = False

# resnext50_32x4d模型
def resnext_model(num_classes, feature_extract = False, use_pretrained=True):

    model_ft = models.resnext50_32x4d(pretrained=use_pretrained)
    set_parameter_requires_grad(model_ft, feature_extract)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Sequential(nn.Linear(num_ftrs, num_classes))

    return model_ft


# In[ ]:


# Configuration options
k_folds = 5
num_epochs = 30
learning_rate = 1e-3
weight_decay = 1e-3
train_loss_function = CutMixCrossEntropyLoss(True)
valid_loss_function = nn.CrossEntropyLoss()
# For fold results
results = {}

# Set fixed random number seed
torch.manual_seed(42)

# Define the K-fold Cross Validator
kfold = KFold(n_splits=k_folds, shuffle=True)


# ### **训练**

# In[ ]:


# Start print
print('--------------------------------------')

# K-fold Cross Validation model evaluation
for fold, (train_ids,valid_ids) in enumerate(kfold.split(train_val_dataset)):

  # Print
  print(f'FOLD {fold}')
  print('--------------------------------------')

  # Sample elements randomly from a given list of ids, no replacement.
  train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
  valid_subsampler = torch.utils.data.SubsetRandomSampler(valid_ids)

  # Define data loaders for training and testing data in this fold
  trainloader = torch.utils.data.DataLoader(
                      CutMix(TrainValidData(train_val_path, img_path, transform = train_transform), num_class=176, beta=1.0, prob=0.5, num_mix=2), 
                      batch_size=128, sampler=train_subsampler, num_workers=0)
  validloader = torch.utils.data.DataLoader(
                      TrainValidData(train_val_path, img_path, transform = val_test_transform),
                      batch_size=128, sampler=valid_subsampler, num_workers=0)
  
  # Initialize a model and put it on the device specified.
  model = resnext_model(176)
  model = model.to(device)
  model.device = device
  
  # Initialize optimizer
  optimizer = torch.optim.AdamW(model.parameters(),lr=learning_rate,weight_decay= weight_decay)
#   optimizer = SWA(our_optimizer, swa_start=5, swa_freq =5, swa_lr=0.05)
  scheduler = CosineAnnealingLR(optimizer,T_max=10)

  # Run the training loop for defined number of epochs
  for epoch in range(0,num_epochs):
    model.train()
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    # These are used to record information in training
    train_losses = []
    train_accs = []
    # Iterate the training set by batches
    for batch in tqdm(trainloader):
      # Move images and labels to GPU
      imgs, labels = batch
      imgs = imgs.to(device)
      labels = labels.to(device)
      # Forward the data
      logits = model(imgs)
      # Calculate loss
      loss = train_loss_function(logits,labels)
      # Clear gradients in previous step
      optimizer.zero_grad()
      # Compute gradients for parameters
      loss.backward()
      # Update the parameters with computed gradients
      optimizer.step()
      # Compute the accuracy for current batch.
      # acc = (logits.argmax(dim=-1) == labels).float().mean()
      # Record the loss and accuracy.
      train_losses.append(loss.item())
      # train_accs.append(acc)
    print("第%d个epoch的学习率：%f" % (epoch+1,optimizer.param_groups[0]['lr']))
    scheduler.step()
    # The average loss and accuracy of the training set is the average of the recorded values.
    train_loss = np.sum(train_losses) / len(train_losses)
    # train_acc = np.sum(train_accs) / len(train_accs)
    # Print the information.
    # print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}, acc = {train_acc:.5f}")
    print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}")

  # Train process (all epochs) is complete
  print('Training process has finished. Saving trained model.')
  print('Starting validation')

  # Saving the model
  print('saving model with loss {:.3f}'.format(train_loss))
  save_path = f'./model-fold-{fold}.pth'
  torch.save(model.state_dict(),save_path)
  # Start Validation
  model.eval()
  valid_losses = []
  valid_accs = []
  with torch.no_grad():
    for batch in tqdm(validloader):
      imgs, labels = batch
      # No gradient in validation
      logits = model(imgs.to(device))
      loss = valid_loss_function(logits,labels.to(device))
      acc = (logits.argmax(dim=-1) == labels.to(device)).float().mean()
      # Record loss and accuracy
      valid_losses.append(loss.item())        
      valid_accs.append(acc)
    # The average loss and accuracy
    valid_loss = np.sum(valid_losses)/len(valid_losses)
    valid_acc = np.sum(valid_accs)/len(valid_accs)
    print(f"[ Valid | {epoch + 1:03d}/{num_epochs:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f}")
    print('Accuracy for fold %d: %d' % (fold, valid_acc))
    print('--------------------------------------')
    results[fold] = valid_acc
# Print fold results
print(f'K-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS')
print('--------------------------------')
total_summation = 0.0
for key, value in results.items():
  print(f'Fold {key}: {value} ')
  total_summation += value
print(f'Average: {total_summation/len(results.items())} ')


# ### **预测**

# In[ ]:


testloader = torch.utils.data.DataLoader(
                      TestData(test_path, img_path, transform = val_test_transform),
                      batch_size=128, num_workers=0)


# In[ ]:


## predict
model = resnext_model(176)

# create model and load weights from checkpoint
model = model.to(device)
# load the all folds
for test_fold in range(k_folds):
  model_path = f'./model-fold-{test_fold}.pth'
  saveFileName = f'./submission-fold-{test_fold}.csv'
  model.load_state_dict(torch.load(model_path))

  # Make sure the model is in eval mode.
  # Some modules like Dropout or BatchNorm affect if the model is in training mode.
  model.eval()
  tta_model = tta.ClassificationTTAWrapper(model, tta.aliases.five_crop_transform(200,200))

  # Initialize a list to store the predictions.
  predictions = []
  # Iterate the testing set by batches.
  for batch in tqdm(testloader):
      
      imgs = batch
      with torch.no_grad():
          logits = tta_model(imgs.to(device))
      
      # Take the class with greatest logit as prediction and record it.
      predictions.extend(logits.argmax(dim=-1).cpu().numpy().tolist())

  preds = []
  for i in predictions:
      preds.append(num_to_class[i])

  test_data = pd.read_csv(test_path)
  test_data['label'] = pd.Series(preds)
  submission = pd.concat([test_data['image'], test_data['label']], axis=1)
  submission.to_csv(saveFileName, index=False)
  print("ResNeXt Model Results Done!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# ### **ResNeXt的5折交叉验证的结果投票**

# In[ ]:


df0 = pd.read_csv('./submission-fold-0.csv')
df1 = pd.read_csv('./submission-fold-1.csv')
df2 = pd.read_csv('./submission-fold-2.csv')
df3 = pd.read_csv('./submission-fold-3.csv')
df4 = pd.read_csv('./submission-fold-4.csv')


# In[ ]:


list_num_label0 = []
for i in df0['label']:
  list_num_label0.append(class_to_num[i])
df0['num_label0']=list_num_label0
df0.head()


# In[ ]:


list_num_label1 = []
for i in df1['label']:
  list_num_label1.append(class_to_num[i])
df1['num_label1']=list_num_label1
df1.head()


# In[ ]:


list_num_label2 = []
for i in df2['label']:
  list_num_label2.append(class_to_num[i])
df2['num_label2']=list_num_label2
df2.head()


# In[ ]:


list_num_label3 = []
for i in df3['label']:
  list_num_label3.append(class_to_num[i])
df3['num_label3']=list_num_label3
df3.head()


# In[ ]:


list_num_label4 = []
for i in df4['label']:
  list_num_label4.append(class_to_num[i])
df4['num_label4']=list_num_label4
df4.head()


# In[ ]:


df_all = df0.copy()
df_all.drop(['label'],axis=1,inplace=True)
df_all.head()


# In[ ]:


df_all['num_label1']=list_num_label1
df_all['num_label2']=list_num_label2
df_all['num_label3']=list_num_label3
df_all['num_label4']=list_num_label4
df_all.head()


# In[ ]:


df_all_transpose = df_all.copy().drop(['image'],axis=1).transpose()
df_all_transpose.head()


# In[ ]:


df_mode = df_all_transpose.mode().transpose()
df_mode.head()


# In[ ]:


voting_class = []
for each in df_mode[0]:
  voting_class.append(num_to_class[each])
voting_class


# In[ ]:


df_all['label'] = voting_class
df_all.head()


# In[ ]:


df_submission = df_all[['image','label']].copy()
df_submission.head()


# In[ ]:


df_submission.to_csv('./submission-resnext.csv', index=False)
print('ResNeXt voting results successfully saved!')


# ## **基于DenseNet模型部分**

# ### **DenseNet模型**

# In[ ]:


# 是否要冻住模型的前面一些层
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        model = model
        for param in model.parameters():
            param.requires_grad = False

# densenet161模型
def dense_model(num_classes, feature_extract = False, use_pretrained=True):

    model_ft = models.densenet161(pretrained=use_pretrained)
    set_parameter_requires_grad(model_ft, feature_extract)
    num_ftrs = model_ft.classifier.in_features
    model_ft.classifier = nn.Sequential(nn.Linear(num_ftrs, num_classes))

    return model_ft


# In[ ]:


# Configuration options
k_folds = 5
num_epochs = 30
learning_rate = 1e-4
weight_decay = 1e-3
train_loss_function = CutMixCrossEntropyLoss(True)
valid_loss_function = nn.CrossEntropyLoss()
# For fold results
results = {}

# Set fixed random number seed
torch.manual_seed(42)

# Define the K-fold Cross Validator
kfold = KFold(n_splits=k_folds, shuffle=True)


# ### **训练**

# In[ ]:


# Start print
print('--------------------------------------')

# K-fold Cross Validation model evaluation
for fold, (train_ids,valid_ids) in enumerate(kfold.split(train_val_dataset)):

  # Print
  print(f'FOLD {fold}')
  print('--------------------------------------')

  # Sample elements randomly from a given list of ids, no replacement.
  train_subsampler = torch.utils.data.SubsetRandomSampler(train_ids)
  valid_subsampler = torch.utils.data.SubsetRandomSampler(valid_ids)

  # Define data loaders for training and testing data in this fold
  trainloader = torch.utils.data.DataLoader(
                      CutMix(TrainValidData(train_val_path, img_path, transform = train_transform), num_class=176, beta=1.0, prob=0.5, num_mix=2), 
                      batch_size=32, sampler=train_subsampler, num_workers=0)
  validloader = torch.utils.data.DataLoader(
                      TrainValidData(train_val_path, img_path, transform = val_test_transform),
                      batch_size=32, sampler=valid_subsampler, num_workers=0)
  
  # Initialize a model and put it on the device specified.
  model = dense_model(176)
  model = model.to(device)
  model.device = device
  
  # Initialize optimizer
  optimizer = torch.optim.AdamW(model.parameters(),lr=learning_rate,weight_decay= weight_decay)
  scheduler = CosineAnnealingLR(optimizer,T_max=10)

  # Run the training loop for defined number of epochs
  for epoch in range(0,num_epochs):
    model.train()
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    # These are used to record information in training
    train_losses = []
    train_accs = []
    # Iterate the training set by batches
    for batch in tqdm(trainloader):
      # Move images and labels to GPU
      imgs, labels = batch
      imgs = imgs.to(device)
      labels = labels.to(device)
      # Forward the data
      logits = model(imgs)
      # Calculate loss
      loss = train_loss_function(logits,labels)
      # Clear gradients in previous step
      optimizer.zero_grad()
      # Compute gradients for parameters
      loss.backward()
      # Update the parameters with computed gradients
      optimizer.step()
      # Compute the accuracy for current batch.
#       acc = (logits.argmax(dim=-1) == labels).float().mean()
      # Record the loss and accuracy.
      train_losses.append(loss.item())
#       train_accs.append(acc)
    print("第%d个epoch的学习率：%f" % (epoch+1,optimizer.param_groups[0]['lr']))
    scheduler.step()
    # The average loss and accuracy of the training set is the average of the recorded values.
    train_loss = np.sum(train_losses) / len(train_losses)
#     train_acc = np.sum(train_accs) / len(train_accs)
    # Print the information.
#     print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}, acc = {train_acc:.5f}")
    print(f"[ Train | {epoch + 1:03d}/{num_epochs:03d} ] loss = {train_loss:.5f}")

  # Train process (all epochs) is complete
  print('Training process has finished. Saving trained model.')
  print('Starting validation')

  # Saving the model
  print('saving model with loss {:.3f}'.format(train_loss))
  save_path = f'./model-fold-{fold}.pth'
  torch.save(model.state_dict(),save_path)
  # Start Validation
  model.eval()
  valid_losses = []
  valid_accs = []
  with torch.no_grad():
    for batch in tqdm(validloader):
      imgs, labels = batch
      # No gradient in validation
      logits = model(imgs.to(device))
      loss = valid_loss_function(logits,labels.to(device))
      acc = (logits.argmax(dim=-1) == labels.to(device)).float().mean()
      # Record loss and accuracy
      valid_losses.append(loss.item())        
      valid_accs.append(acc)
    # The average loss and accuracy
    valid_loss = np.sum(valid_losses)/len(valid_losses)
    valid_acc = np.sum(valid_accs)/len(valid_accs)
    print(f"[ Valid | {epoch + 1:03d}/{num_epochs:03d} ] loss = {valid_loss:.5f}, acc = {valid_acc:.5f}")
    print('Accuracy for fold %d: %d' % (fold, valid_acc))
    print('--------------------------------------')
    results[fold] = valid_acc
# Print fold results
print(f'K-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS')
print('--------------------------------')
total_summation = 0.0
for key, value in results.items():
  print(f'Fold {key}: {value} ')
  total_summation += value
print(f'Average: {total_summation/len(results.items())} ')


# ### **预测**

# In[ ]:


testloader = torch.utils.data.DataLoader(
                      TestData(test_path, img_path, transform = val_test_transform),
                      batch_size=32, num_workers=0)


# In[ ]:


## predict
model = dense_model(176)

# create model and load weights from checkpoint
model = model.to(device)
# load the all folds
for test_fold in range(k_folds):
  model_path = f'./model-fold-{test_fold}.pth'
  saveFileName = f'./submission-fold-{test_fold}.csv'
  model.load_state_dict(torch.load(model_path))

  # Make sure the model is in eval mode.
  # Some modules like Dropout or BatchNorm affect if the model is in training mode.
  model.eval()
  tta_model = tta.ClassificationTTAWrapper(model, tta.aliases.five_crop_transform(200,200))

  # Initialize a list to store the predictions.
  predictions = []
  # Iterate the testing set by batches.
  for batch in tqdm(testloader):
      
      imgs = batch
      with torch.no_grad():
          logits = tta_model(imgs.to(device))
      
      # Take the class with greatest logit as prediction and record it.
      predictions.extend(logits.argmax(dim=-1).cpu().numpy().tolist())

  preds = []
  for i in predictions:
      preds.append(num_to_class[i])

  test_data = pd.read_csv(test_path)
  test_data['label'] = pd.Series(preds)
  submission = pd.concat([test_data['image'], test_data['label']], axis=1)
  submission.to_csv(saveFileName, index=False)
  print("Dense Model Results Done!!!!!!!!!!!!!!!!!!!!!!!!!!!")


# ### **DenseNet的5折交叉验证的结果投票**

# In[ ]:


df0 = pd.read_csv('./submission-fold-0.csv')
df1 = pd.read_csv('./submission-fold-1.csv')
df2 = pd.read_csv('./submission-fold-2.csv')
df3 = pd.read_csv('./submission-fold-3.csv')
df4 = pd.read_csv('./submission-fold-4.csv')


# In[ ]:


list_num_label0 = []
for i in df0['label']:
  list_num_label0.append(class_to_num[i])
df0['num_label0']=list_num_label0
df0.head()


# In[ ]:


list_num_label1 = []
for i in df1['label']:
  list_num_label1.append(class_to_num[i])
df1['num_label1']=list_num_label1
df1.head()


# In[ ]:


list_num_label2 = []
for i in df2['label']:
  list_num_label2.append(class_to_num[i])
df2['num_label2']=list_num_label2
df2.head()


# In[ ]:


list_num_label3 = []
for i in df3['label']:
  list_num_label3.append(class_to_num[i])
df3['num_label3']=list_num_label3
df3.head()


# In[ ]:


list_num_label4 = []
for i in df4['label']:
  list_num_label4.append(class_to_num[i])
df4['num_label4']=list_num_label4
df4.head()


# In[ ]:


df_all = df0.copy()
df_all.drop(['label'],axis=1,inplace=True)
df_all.head()


# In[ ]:


df_all['num_label1']=list_num_label1
df_all['num_label2']=list_num_label2
df_all['num_label3']=list_num_label3
df_all['num_label4']=list_num_label4
df_all.head()


# In[ ]:


df_all_transpose = df_all.copy().drop(['image'],axis=1).transpose()
df_all_transpose.head()


# In[ ]:


df_mode = df_all_transpose.mode().transpose()
df_mode.head()


# In[ ]:


voting_class = []
for each in df_mode[0]:
  voting_class.append(num_to_class[each])
voting_class


# In[ ]:


df_all['label'] = voting_class
df_all.head()


# In[ ]:


df_submission = df_all[['image','label']].copy()
df_submission.head()


# In[ ]:


df_submission.to_csv('./submission-densenet.csv', index=False)
print('Densenet results successfully saved!')


# ## **最终结果集成（投票方式）**

# In[16]:


df_resnest = pd.read_csv('../input/classify-leaves-results/submission-resnest.csv')
df_resnext = pd.read_csv('../input/classify-leaves-results/submission-resnext.csv')
df_densenet = pd.read_csv('../input/classify-leaves-results/submission-densenet.csv')


# In[17]:


df_all = df_resnest.copy()
df_all.rename(columns = {'label':'label_resnest'},inplace=True)
df_all['label_resnext'] = df_resnext.copy()['label']
df_all['label_densenet'] = df_densenet.copy()['label']
df_all.head()


# In[18]:


df_all['label']=0
for rows in range(len(df_all)):
    if (df_all['label_resnest'].iloc[rows]==df_all['label_resnext'].iloc[rows]) or (df_all['label_resnest'].iloc[rows]==df_all['label_densenet'].iloc[rows]):
        df_all['label'].iloc[rows] = df_all.copy()['label_resnest'].iloc[rows]
    elif df_all['label_resnext'].iloc[rows]==df_all['label_densenet'].iloc[rows]:
        df_all['label'].iloc[rows] = df_all.copy()['label_resnext'].iloc[rows]
    else:
        df_all['label'].iloc[rows] = df_all.copy()['label_resnest'].iloc[rows]
df_all.head()


# In[19]:


df_final = df_all.copy()[['image','label']]
df_final.head()


# In[20]:


df_final.to_csv('./submission.csv', index=False)
print('Final results successfully saved!')

