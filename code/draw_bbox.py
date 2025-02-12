import json
import cv2
import os
# 打开并读取 JSON 文件内容
def get_anno(data_file,image_file):
    annotations_1 = []
    score_1 = []
    with open(data_file, 'r') as f:
        annotations = json.load(f)  # 使用 json.load 直接加载文件内容
        
        if data_file != None:
            annotations = annotations["annotations"]
          
            for item in annotations:
                if item["image_id"] + ".jpg" == image_file:
                    annotations_1.append(item["bbox"])
        else:
            for item in annotations:
                if item["image_id"] == image_file:
                    annotations_1.append(item["bbox"])
                    score_1.append(item["score"])
    
    return annotations_1,score_1

def show(image,annotations):
   
    for i in range(len(annotations)):
        x1, y1, x2, y2 = annotations[i]
        top_left = (int(x1), int(y1))
        bottom_right = (int( x2), int(y2))
        # 画一个绿色的矩形框
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 1)  # (0, 255, 0) 绿色，2 是线宽
    image = cv2.resize(image, (int(0.5 * image.shape[1]), int(0.5 * image.shape[0])))

    cv2.imshow("Image with Bounding Box", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    



# 加载图像
image_path = r"F:\dataset\sim10k_aug_img\3399041.jpg"  # 替换为您的图像路径

pred_bbox = [
   #[718,379,718+359,379+277],
   #[1,458,1+584,458+384],
   [71.8, 612.1, 655.8, 996.1]
]
image = cv2.imread(image_path)
show(image,pred_bbox)

