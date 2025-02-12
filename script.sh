#!/bin/bash

# 定义训练函数
train_model() {
    # 运行训练脚本，并将输出重定向到日志文件
    nohup bash -c "CUDA_VISIBLE_DEVICES=0,1 python /workspace/aldi/tools/train_net.py --config /workspace/aldi/configs/sim10k/burn-in-dense.yaml --num-gpus 2" > output.log 2>&1 &
    # 获取训练进程的PID
    TRAIN_PID=$!
    # 等待训练进程完成
    wait $TRAIN_PID
}

# 无限循环，训练完成后重新执行
while true; do
    # 执行训练
    train_model

    

    # 等待几秒，避免频繁重启（如果需要）
    sleep 2
done
