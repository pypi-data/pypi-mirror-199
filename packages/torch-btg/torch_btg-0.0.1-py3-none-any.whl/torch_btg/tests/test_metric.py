from unittest import TestCase

import torch
import torch_btg.metric as metrics

class TestMetric(TestCase):
  def test_f1(self):
    f1 = metrics.fb(torch.tensor([1.0,0.0,0.0]), torch.tensor([0.5, 0.5, 0.5]), torch.tensor([0.5]), beta=1)
    torch.testing.assert_close(f1, torch.tensor([0.4]), check_device=False)

  def test_f2(self):
    f2 = metrics.fb(torch.tensor([1.0,0.0,0.0]), torch.tensor([0.5, 0.5, 0.5]), torch.tensor([0.5]), beta=2)
    torch.testing.assert_close(f2, torch.tensor([0.45454547]), check_device=False)

  def test_f3(self):
    f3 = metrics.fb(torch.tensor([1.0,0.0,0.0]), torch.tensor([0.5, 0.5, 0.5]), torch.tensor([0.5]), beta=3)
    torch.testing.assert_close(f3, torch.tensor([0.4762]), check_device=False)