import json

with open(r"C:\Users\vkale\UK_Currency\coco_data\annotations\instances_val2017.json", 'r') as f:
    annotations = json.load(f)

new_annotations = {
    'info': annotations['info'],
    'licenses': annotations['licenses'],
    'categories': [],
    'images': [],
    'annotations': []
}

# Define the 5 classes that you are interested in
classes = ['person', 'car', 'motorcycle', 'airplane', 'bus']

# Create a new category for each class
for i, class_name in enumerate(classes):
    new_annotations['categories'].append({
        'id': i + 1,
        'name': class_name,
        'supercategory': ''
    })

# Filter out the annotations and images that correspond to the 5 classes
for image in annotations['images']:
    new_image = {
        'id': image['id'],
        'file_name': image['file_name'],
        'width': image['width'],
        'height': image['height']
    }
    new_annotations['images'].append(new_image)
    for ann in annotations['annotations']:
        if ann['image_id'] == image['id'] and ann['category_id'] in range(1, len(classes) + 1):
            new_ann = {
                'id': ann['id'],
                'image_id': ann['image_id'],
                'category_id': ann['category_id'],
                'bbox': ann['bbox'],
                'area': ann['area'],
                'iscrowd': ann['iscrowd']
            }
            new_annotations['annotations'].append(new_ann)

# Save the filtered annotations to a new file
with open(r"C:\Users\vkale\UK_Currency\coco_data\annotations\filtered_annotations_val2017.json", 'w') as f:
    json.dump(new_annotations, f)
