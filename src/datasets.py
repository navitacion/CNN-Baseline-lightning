import os
import cv2
from torch.utils.data import Dataset
import torch


class ImageDataset(Dataset):
    def __init__(self, df, data_dir, transform=None, phase='train'):
        self.df = df
        self.data_dir = data_dir
        self.transform = transform
        self.phase = phase

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_id = row['image_id']
        img_path = os.path.join(self.data_dir, f'{img_id}.jpg')
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if self.transform is not None:
            img = self.transform(img, self.phase)
        else:
            img = torch.from_numpy(img.transpose((2, 0, 1)))
            img = img / 255.

        if self.phase != 'test':
            label = row['target']
            label = torch.tensor(label, dtype=torch.float)

            return img, label
        else:
            return img, img_id
