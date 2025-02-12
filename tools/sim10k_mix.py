import os
import random
import shutil

# 定义源文件夹和目标文件夹路径
dir1 = "/workspace/aldi/datasets/sim10k/images"  # 替换为dir1的路径
dir2 = "/workspace/aldi/datasets/sim10k_mix_1.0/images"  # 替换为dir2的路径
dir_target = "/workspace/aldi/datasets/sim10k_mix_0.1/images"  # 替换为dir1抽取目标路径




# 获取dir1中的所有文件名
all_files = [f for f in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, f))]

# 确保dir2中的文件名和dir1完全一致
assert set(all_files) == set(os.listdir(dir2)), "dir1 和 dir2 的文件名必须完全一致！"

# 随机抽取3000个文件到dir1_target
dir1_files = random.sample(all_files, 9000)

# 剩下的7000个文件到dir2_target
dir2_files = list(set(all_files) - set(dir1_files))

# 移动文件到目标文件夹
for file_name in dir1_files:
    shutil.copy(os.path.join(dir1, file_name), os.path.join(dir_target, file_name))

for file_name in dir2_files:
    shutil.copy(os.path.join(dir2, file_name), os.path.join(dir_target, file_name))

print(f"从 {dir1} 中抽取了 {len(dir1_files)} 个文件到 {dir_target}")
print(f"从 {dir2} 中抽取了 {len(dir2_files)} 个文件到 {dir_target}")
