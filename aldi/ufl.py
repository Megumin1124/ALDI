
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable,Function
import numpy as np
import sys

class SymmetricFocalLoss(nn.Module):
    def __init__(self, delta=0.7, gamma=2, epsilon = 1e-6,reduction='mean'):
        super(SymmetricFocalLoss, self).__init__()
        self.delta = delta
        self.gamma = gamma
        self.epsilon = epsilon
        self.reduction = reduction
    def forward(self, y_pred, y_true):
        y_pred = torch.clamp(y_pred, self.epsilon, 1. - self.epsilon)
        y_pred = y_pred.view(-1)
        y_true = y_true.view(-1)
        cross_entropy = -y_true * torch.log(y_pred[0])
        focal_loss = - self.delta * torch.pow((1 - y_pred[0]) ,  self.gamma) * cross_entropy
        if self.reduction == 'none':
            return focal_loss
        elif self.reduction == 'mean':
            return torch.mean(focal_loss)
        elif self.reduction == 'sum':
            return torch.sum(focal_loss)
class SymmetricFocalTverskyLoss(nn.Module):
    def __init__(self, delta=0.7, gamma=2, epsilon=1e-07):
        super(SymmetricFocalTverskyLoss, self).__init__()
        self.delta = delta
        self.gamma = gamma
        self.epsilon = epsilon
    def forward(self, y_pred, y_true):
        y_pred = torch.clamp(y_pred, self.epsilon, 1. - self.epsilon)
        y_true = torch.clamp(y_true, self.epsilon, 1. - self.epsilon)
        y_pred = y_pred.view(-1)
        y_true = y_true.view(-1)
        tp = torch.sum(y_pred[1] * y_true)
        fp = torch.sum(y_pred[1] * (1 - y_true))
        fn = torch.sum(y_pred[0] * y_true)
        tversky_loss =  (tp + self.epsilon) / (tp + self.delta * fp + (1 - self.delta ) * fn + self.epsilon)
        focal_tversky_loss = torch.pow(1 - tversky_loss, self.gamma)
        return focal_tversky_loss
class SymmetricUnifiedFocalLoss(nn.Module):
    def __init__(self, lambd = 0.3, epsilon=1e-6):
        super(SymmetricUnifiedFocalLoss, self).__init__()
        self.lambd = lambd
        self.epsilon = epsilon
    def forward(self, inputs, targets):
      '''
      with open('/workspace/aldi/input_of_SUFL.txt', 'w') as f:
            f.write(f"inputs:\n{inputs}\n")
               
            f.write(f"targets:\n{targets}\n")
            sys.exit("Training stopped after writing the file.")
            inputs:
            tensor([[0.2755, 0.3272]], device='cuda:0', grad_fn=<AddmmBackward>)
            targets:
            tensor([0], device='cuda:0')
      '''
      y_pred = inputs
      #y_pred = F.softmax(inputs)
      y_true = targets
      symmetric_ftl = SymmetricFocalTverskyLoss()(y_pred, y_true)
      symmetric_fl = SymmetricFocalLoss()(y_pred, y_true)
      #L_auF = weight*LmaF + (1-weight)*L_maFT
      if self.lambd is not None:
        return (self.lambd * symmetric_ftl) + ((1-self.lambd) * symmetric_fl)  
      else:
        return symmetric_ftl + symmetric_fl