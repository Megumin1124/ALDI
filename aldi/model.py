import torch
from typing import Dict, List

from detectron2.config import configurable
from detectron2.modeling.meta_arch.build import META_ARCH_REGISTRY
from detectron2.utils.logger import _log_api_usage

from aldi.align import AlignMixin
from aldi.distill import DistillMixin


def build_aldi(cfg):
    # model 继承自 nn.module/GeneralizedRCNN
    # 这个 model 是 模型 接受输入（batch_inputs）进行推理返回标准字典格式的损失值

    """Add Align and Distill capabilities to any Meta Architecture dynamically."""
    # META_ARCHITECTURE: GeneralizedRCNN
    base_cls = META_ARCH_REGISTRY.get(cfg.MODEL.META_ARCHITECTURE)

    class ALDI(AlignMixin, DistillMixin, base_cls):    
        @configurable
        def __init__(self, **kwargs):
            super(ALDI, self).__init__(**kwargs)
 
        @classmethod
        def from_config(cls, cfg):
            return super(ALDI, cls).from_config(cfg)

        def forward(self, batched_inputs: List[Dict[str, torch.Tensor]], 
                    labeled: bool = True, do_align: bool = False):
            return super(ALDI, self).forward(batched_inputs, do_align=do_align, labeled=labeled)
        
    model = ALDI(cfg)
    model.to(torch.device(cfg.MODEL.DEVICE))
    _log_api_usage("modeling.meta_arch." + cfg.MODEL.META_ARCHITECTURE)
    return model