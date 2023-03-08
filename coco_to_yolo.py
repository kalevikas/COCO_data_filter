import argparse
import json
import os
import shutil

def convert_bbox(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_coco_to_yolo(ann_file, img_dir, out_dir):
    with open(ann_file) as f:
        anns = json.load(f)
        
    img_id_to_file_name = {}
    for img in anns['images']:
        img_id_to_file_name[img['id']] = img['file_name']

    for cat in anns['categories']:
        cat_id_to_name = {cat['id']: cat['name']}

    for ann in anns['annotations']:
        img_id = ann['image_id']
        cat_id = ann['category_id']
        cat_name = cat_id_to_name[cat_id]
        bbox = convert_bbox((ann['image_width'], ann['image_height']), ann['bbox'])
        img_file_name = img_id_to_file_name[img_id]
        img_file_path = os.path.join(img_dir, img_file_name)
        img_out_dir = os.path.join(out_dir, cat_name)
        os.makedirs(img_out_dir, exist_ok=True)
        txt_out_path = os.path.join(img_out_dir, os.path.splitext(img_file_name)[0] + '.txt')
        with open(txt_out_path, 'a') as f:
            f.write(f"{cat_id} {' '.join([str(i) for i in bbox])}\n")
        shutil.copy(img_file_path, img_out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert COCO annotations to YOLO format')
    parser.add_argument('--dataset_dir', type=str, required=True, help='Path to COCO dataset directory')
    parser.add_argument('--ann_dir', type=str, required=True, help='Path to COCO annotations directory')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to output directory')
    args = parser.parse_args()

    # ann_file = os.path.join(args.ann_dir, 'instances_train2017.json')
    # img_dir = os.path.join(args.dataset_dir, 'train2017')
    # out_dir = os.path.join(args.output_dir, 'train')

    # convert_coco_to_yolo(ann_file, img_dir, out_dir)

    ann_file = os.path.join(args.ann_dir, 'C:\\Users\\vkale\\UK_Currency\\coco_data\\filtered_annotation.json')
    img_dir = os.path.join(args.dataset_dir, 'val2017')
    out_dir = os.path.join(args.output_dir, 'val')

    convert_coco_to_yolo(ann_file, img_dir, out_dir)
