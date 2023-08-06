import torch
from torch_btg.confusion import confusion, EPS
from torch_btg.loss import _thresholds

def _indicator(x, t):
  ''' heaviside step function '''
  return torch.where(x < t, 0, 1)

def bce(gt, pt):
  return -1/gt.shape[0] * (gt * torch.log(pt) + (1-gt) * torch.log(1-pt)).nansum()

def fb(gt, pt, thresholds=_thresholds(), approx=_indicator, beta=1):
  tp, fn, fp, tn = confusion(gt, pt, thresholds, approx)
  precision = tp / (tp + fp + EPS)
  recall = tp / (tp + fn + EPS)
  return (1 + beta*beta) * (precision * recall) / (beta*beta * precision + recall)

def accuracy(gt, pt, thresholds=_thresholds(), approx=_indicator):
  tp, fn, fp, tn = confusion(gt, pt, thresholds, approx)
  return (tp + tn) / (tp + fn + fp + tn)

def kl(p, q):
  kl = p * torch.log(p/q)
  kl[torch.isnan(kl)] = 0
  kl[torch.isinf(kl)] = 0
  return kl