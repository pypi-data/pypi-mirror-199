"""
.. image:: https://img.shields.io/badge/classification-yes-brightgreen?style=flat-square
   :alt: classification badge
.. image:: https://img.shields.io/badge/segmentation-yes-brightgreen?style=flat-square
   :alt: classification badge

..  autoclass:: pytorch_ood.detector.MaxLogit
    :members:

"""
from typing import TypeVar

import torch

from ..api import Detector

Self = TypeVar("Self")


class MaxLogit(Detector):
    """
    Implements the Max Logit Method for OOD Detection as proposed in
    *Scaling Out-of-Distribution Detection for Real-World Settings*.

    .. math:: - \\max_y f_y(x)

    where :math:`f_y(x)` indicates the :math:`y^{th}` logits value predicted by :math:`f`.

    :see Paper:
       `ArXiv <https://.org/abs/1911.11132>`__
    """

    def __init__(self, model: torch.nn.Module):
        """
        :param t: temperature value T. Default is 1.
        """
        super(MaxLogit, self).__init__()
        self.model = model

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """
        :param x:  model inputs
        """
        return self.score(self.model(x))

    def fit(self: Self, *args, **kwargs) -> Self:
        """
        Not required
        """
        return self

    @staticmethod
    def score(logits: torch.Tensor) -> torch.Tensor:
        """
        :param logits: logits for samples
        """
        return -logits.max(dim=1).values
