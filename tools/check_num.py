import cv2
import numpy as np
import glob
import os
if __name__ == "__main__":
    img_path =  '/workspace/aldi/datasets/sim10k_mix_0.1/images'
 
    img_lists = glob.glob(img_path + '/*.jpg')
    img_basenames = []

    # 遍历所有的图片，取图片名
    
    #print(img_lists)
    for item in img_lists:
        img_basenames.append(os.path.basename(item))
    all_num = len(img_lists)
    print("all num is ",all_num)
    '''
    img_path1 = '/workspace/aldi/datasets/sim10k/images'
    img_path2 = '/workspace/aldi/datasets/sim10k_casual/images'

    # Get image file lists for both directories
    img_lists1 = glob.glob(img_path1 + '/*.jpg')
    img_lists2 = glob.glob(img_path2 + '/*.jpg')

    img_basenames1 = []
    for item in img_lists1:
        img_basenames1.append(os.path.basename(item))
    img_basenames2 = []
    for item in img_lists2:
        img_basenames2.append(os.path.basename(item))
    # Extract basenames
   
    print(len(img_basenames2))

    # Compare images
    for i in range(all_num):
        if i >= len(img_basenames1) or i >= len(img_basenames2):
            print(f"Not enough images in one of the directories. Index: {i}")
            break
        
        # Read images
        img1 = cv2.imread(os.path.join(img_path1, img_basenames1[i]), 0)
        img2 = cv2.imread(os.path.join(img_path2, img_basenames2[i]), 0)
        
        # Check if images have the same shape
        if img1 is None or img2 is None:
            print(f"Error reading images at index {i}:")
            print(f"  img1 path: {os.path.join(img_path1, img_basenames1[i])}")
            print(f"  img2 path: {os.path.join(img_path2, img_basenames2[i])}")
        elif img1.shape != img2.shape:
            print(f"Image shapes differ at index {i}:")
            print(f"  img1 shape: {img1.shape}")
            print(f"  img2 shape: {img2.shape}")
        else:
            pass
            #print(f"Images at index {i} are equal in shape.")

    print("Comparison completed.")
    '''