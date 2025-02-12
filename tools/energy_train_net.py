#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.
"""
Copied directly from detectron2/tools/train_net.py except where noted.
"""
from datetime import timedelta

import detectron2.utils.comm as comm
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import default_argument_parser, default_setup, launch
from detectron2.evaluation import verify_results

from aldi.checkpoint import DetectionCheckpointerWithEMA
from aldi.config import add_aldi_config
from aldi.ema import EMA
from aldi.energy_trainer import ALDITrainer
import aldi.datasets # register datasets with Detectron2
import aldi.model # register ALDI R-CNN model with Detectron2
import aldi.backbone # register ViT FPN backbone with Detectron2

import random
import numpy as np
import torch
from detectron2.utils.comm import get_rank


import atexit
import signal
import gc

def cleanup():
    print("Cleaning up resources...")
    gc.collect()
    # 在这里添加清理操作，如释放信号量、关闭文件等
    torch.cuda.empty_cache()  # 清理 GPU 内存

    # 如果有其他清理资源的操作，可以在这里添加

#atexit.register(cleanup)

# 捕获 Ctrl+C 中断信号并清理资源
def signal_handler(sig, frame):
    print("\nCtrl+C detected. Cleaning up resources...")
    cleanup()
    print("over clean task")
    exit(0)

#signal.signal(signal.SIGINT, signal_handler)
def setup(args):
    """
    Copied directly from detectron2/tools/train_net.py
    """
    cfg = get_cfg()

    ## Change here
    add_aldi_config(cfg)
    ## End change

    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    return cfg

def main(args):
    """
    Copied directly from detectron2/tools/train_net.py
    But replace Trainer with DATrainer and disable TTA.
    """
    cfg = setup(args)
    try:
        if args.eval_only:
            model = ALDITrainer.build_model(cfg)
            ## Change here
            ckpt = DetectionCheckpointerWithEMA(model, save_dir=cfg.OUTPUT_DIR)
            if cfg.EMA.ENABLED and cfg.EMA.LOAD_FROM_EMA_ON_START:
                ema = EMA(ALDITrainer.build_model(cfg), cfg.EMA.ALPHA)
                ckpt.add_checkpointable("ema", ema)
            ckpt.resume_or_load(cfg.MODEL.WEIGHTS, resume=args.resume)
            ## End change
            res = ALDITrainer.test(cfg, model)
            if cfg.TEST.AUG.ENABLED:
                raise NotImplementedError("TTA not supported")
            if comm.is_main_process():
                verify_results(cfg, res)
            return res

        trainer = ALDITrainer(cfg)
        trainer.resume_or_load(resume=args.resume)
        return trainer.train()
    except KeyboardInterrupt:
        print("training interru[ted.cleaning up ing]")
        #cleanup()

if __name__ == "__main__":

    args = default_argument_parser().parse_args()
    
    print("Command Line Args:", args)
    launch(
        main,
        args.num_gpus,
        num_machines=args.num_machines,
        machine_rank=args.machine_rank,
        dist_url=args.dist_url,
        timeout=timedelta(minutes=1), # added for debugging
        args=(args,),
    )
   
