burn-in:
CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/burn-in-baseline.yaml\
                        --num-gpus 2

CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/burn-in-casual.yaml\
                        --num-gpus 2

CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/burn-in-SUFL.yaml\
                        --num-gpus 2   

nohup bash -c "CUDA_VISIBLE_DEVICES=0,1,2,3 python /workspace/aldi/tools/train_net.py --config /workspace/aldi/configs/sim10k/burn-in-dense.yaml --num-gpus 4" > output.log 2>&1 &

CUDA_VISIBLE_DEVICES=0,1,2,3 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/burn-in-dense.yaml\
                        --num-gpus 4  
distill:
CUDA_VISIBLE_DEVICES=0 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/distill-baseline.yaml \
                        --num-gpus 1

CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/energy_train_net.py \
                        --config /workspace/aldi/configs/sim10k/distill-energy.yaml \
                        --num-gpus 2
#now
nohup bash -c "CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/energy_train_net.py --config /workspace/aldi/configs/sim10k/distill-dense-energy.yaml --num-gpus 2" > output_distill.log 2>&1 &

CUDA_VISIBLE_DEVICES=0,1,2,3 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/distill-casual.yaml\
                        --num-gpus 4
                        

CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/train_net.py \
                        --config /workspace/aldi/configs/sim10k/distill-SUFL.yaml\
                        --num-gpus 2   

eval-only:
python tools/train_net.py --eval-only \
    --config /workspace/aldi/configs/sim10k/distill-baseline.yaml \
                MODEL.WEIGHTS /workspace/aldi/output/sim10k/distill/energy/1/cityscapes_cars_val_model_best_7807.pth

    
visualize:
python tools/visualize_featurespace.py \
            --config /workspace/aldi/configs/sim10k/distill-baseline.yaml \
            MODEL.WEIGHTS /workspace/aldi/output/sim10k/distill/energy/1/cityscapes_cars_val_model_best.pth
                        
                        
            
