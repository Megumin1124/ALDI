import json
import random
import cv2
import numpy as np
import os
# sim10k中车辆稀疏，因此可能会对重叠目标检测效果差。因此加入此代码，从而让其检测重叠目标效果加强
def random_translate_bbox(bbox, width, height):
    """
    平移标注框，返回新的标注框
    bbox: [xmin, ymin, w, h]
    width: 图像的宽度
    height: 图像的高度
    """
    xmin, ymin, box_width, box_height = bbox
    xmax = xmin + box_width
    ymax = ymin + box_height


    # 平移的最大量
    # 平移的最大量，限定为一位小数
    max_translate_x = round(box_width * random.uniform(0.3, 0.8), 1)
    max_translate_y = round(box_height * random.uniform(0.3, 0.8), 1)


    # 随机生成平移量
    translate_x = round(random.uniform(0, max_translate_x),1)
    translate_y = round(random.uniform(0, max_translate_y),1)

    # 平移标注框
    new_bbox = [xmin + translate_x, ymin + translate_y, xmax + translate_x, ymax + translate_y]

    # 保证新的标注框不超出图像边界
    # bbox: [xmin, ymin, w, h]

    new_bbox[0] = max(0,min(new_bbox[0],width))
    new_bbox[1] = max(0,min(new_bbox[1],height))

    #print("bbox",new_bbox)
    translate_x = new_bbox[0] - bbox[0]
    translate_y = new_bbox[1] - bbox[1]
    return new_bbox, translate_x, translate_y

def augment_image(image, bbox, translate_x, translate_y):
    """
    将前景从原图中提取并平移
    """
    xmin, ymin, box_width, box_height = bbox
    xmax = xmin + box_width
    ymax = ymin + box_height
    # 提取前景部分
    foreground = image[int(ymin):int(ymax), int(xmin):int(xmax)]

    return foreground, int(xmin + translate_x), int(ymin + translate_y)

def augment_annotations(json_file, image_folder, output_folder):
    # 读取原始 JSON 文件
    with open(json_file, 'r') as f:
        data = json.load(f)
    i = 0
    augmented_annotations = []
    for image_info in data['images']:
        i = i+1
        print(i)
        image_id = image_info['id']
        image_filename = image_info['file_name']
        image_width = image_info['width']
        image_height = image_info['height']
        
    
        # 读取图像
        image_path = os.path.join(image_folder, image_filename)
        image = cv2.imread(image_path)
        #print(image_path)
        # 获取该图片的所有标注
        image_annotations = [ann for ann in data['annotations'] if ann['image_id'] == image_id]

        # 为每个标注框生成一个平移后的新标注框和图像
        for annotation in image_annotations:
            bbox = annotation['bbox']
            new_bbox, translate_x, translate_y = random_translate_bbox(bbox, image_width, image_height)
            #print(bbox)
            #print(translate_x)
            # 创建平移后的图像
            translated_foreground, new_xmin, new_ymin = augment_image(image, bbox, translate_x, translate_y)
            bbox_width = translated_foreground.shape[1]
            bbox_height = translated_foreground.shape[0]
            new_image = image.copy()
            new_xmax = new_xmin + bbox_width
            new_ymax = new_ymin + bbox_height
            if new_xmax > image_width:
                new_xmax = image_width

            if new_ymax > image_height:
                new_ymax = image_height
            # 将平移后的前景图像合并回原图
            
            correct_foreground = translated_foreground[0:new_ymax - new_ymin,0:new_xmax - new_xmin]
            
            #print(correct_foreground.shape,int(new_ymin),int(new_ymin + bbox_height),int(new_xmin),int(new_xmin + bbox_width))
            #print(translated_foreground.shape)
            new_image[int(new_ymin):int(new_ymax), int(new_xmin):int(new_xmax)] = correct_foreground
            
            # 保存新图像
            new_image_filename = f"{image_filename}"
            new_image_path = os.path.join(output_folder, new_image_filename)
            cv2.imwrite(new_image_path, new_image)
            #print(new_image_path)
            # 创建新的标注框
            new_annotation = annotation.copy()
            #print(new_bbox)
            new_bbox = [new_xmin, new_ymin, new_xmax - new_xmin, new_ymax - new_ymin]
            new_annotation['bbox'] = new_bbox
            
            augmented_annotations.append(new_annotation)
            break
    # 更新 JSON 文件，包含原始标注和新增的平移标注框
    data['annotations'].extend(augmented_annotations)

    # 保存更新后的 JSON 文件
    output_json_file_folder = '/workspace/aldi/datasets/sim10k_dense/' 
    output_json_file = os.path.join(output_json_file_folder, 'coco_car_annotations.json')
    with open(output_json_file, 'w') as f:
        json.dump(data, f, indent=4)

"""# 示例使用
json_file = '/workspace/aldi/datasets/sim10k/coco_car_annotations.json'  # 原始 JSON 标注文件路径
image_folder ='/workspace/aldi/datasets/sim10k/images' # 图像文件夹路径
output_folder = '/workspace/aldi/datasets/sim10k_dense/images'  # 输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

augment_annotations(json_file, image_folder, output_folder)
"""

# 读取注释 JSON 文件
with open('/workspace/aldi/datasets/sim10k_dense/coco_car_annotations.json', 'r') as f:
    data = json.load(f)

# 获取所有的注释 ID
ann_ids = [ann['id'] for ann in data['annotations']]

# 检查是否有重复的 ID
if len(ann_ids) != len(set(ann_ids)):
    print("There are duplicate annotation IDs!")

    # 修复重复 ID（可以重新生成 ID 或通过其他方法）
    unique_ann_ids = set()
    for ann in data['annotations']:
        original_id = ann['id']
        # 生成新的唯一 ID（这里可以根据需求重新定义生成方式）
        while ann['id'] in unique_ann_ids:
            ann['id'] += 1  # 简单的增加 ID
        unique_ann_ids.add(ann['id'])

    # 保存修复后的 JSON 文件
    with open('/workspace/aldi/datasets/sim10k_dense/coco_car_annotations.json', 'w') as f:
        json.dump(data, f)
else:
    print("All annotation IDs are unique.")
