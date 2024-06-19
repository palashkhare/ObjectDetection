# Description
### Object detetction using YOLO V8.
This repository tryies to utilize capabilities of YOLO v8 and try to understand the process of -
* Using Yolo V8
* Training Yolo models

# Concepts

### Image Classification
The neural network that's created and trained for image classification determines a class of object on the image and returns its name and the probability of this prediction.

For example, on the left image, it returned that this is a "cat" and that the confidence level of this prediction is 92% (0.92).

### Object Detection
The neural network for object detection, in addition to the object type and probability, returns the coordinates of the object on the image: x, y, width and height, as shown on the second image. Object detection neural networks can also detect several objects in the image and their bounding boxes.

### Image Segmenation
Finally, in addition to object types and bounding boxes, the neural network trained for image segmentation detects the shapes of the objects, as shown on the right image.


# YOLO V8
### Types of modes offered in YOLO V8

Larger the moder more accurate the object detection

|Classification	| Detection	| Segmentation	| Kind|
|--|--|--|--|
|yolov8n-cls.pt	| yolov8n.pt	| yolov8n-seg.pt	| Nano  |
|yolov8s-cls.pt	| yolov8s.pt	| yolov8s-seg.pt	| Small |
|yolov8m-cls.pt	| yolov8m.pt	| yolov8m-seg.pt	| Medium|
|yolov8l-cls.pt	| yolov8l.pt	| yolov8l-seg.pt	| Large |
|yolov8x-cls.pt	| yolov8x.pt	| yolov8x-seg.pt	| Huge  |

### Important Methods
* train({path to dataset descriptor file}) – used to train the model on the images dataset.
* predict({image}) – used to make a prediction for a specified image, for example to detect bounding boxes of all objects that the model can find in the image.
* export({format}) – used to export the model from the default PyTorch format to a specified format.

### Default Training Dataset
YOLO v8 is trained on a huge COCO image dataset of 80 different types.

### Annotation Requirements
* Decide on and encode classes of objects you want to teach your model to detect. 
  *  For example, if you want to detect only cats and dogs, then you can state that "0" is cat and "1" is dog.
* Create a folder for your dataset and two subfolders in it: "images" and "labels".
* Add the images to the "images" subfolder. The more images you collect, the better for training.
* For each image, create an annotation text file in the "labels" subfolder. Annotation text files should have the same names as image files and the ".txt" extensions. In the annotation files you should add records about each object that exist on the appropriate image in the following format:
```
{object_class_id} {x_center} {y_center} {width} {height}
```

> You should also normalize the coordinates to fit in a range from 0 to 1. To calculate them, you need to use the following formulas:

```
x_center = (box_x_left+box_x_width/2)/image_width
y_center = (box_y_top+box_height/2)/image_height
width = box_width/image_width
height = box_height/image_height
```
> If one image has more than one objects annotated then two rows of annotation in the sam file need to be provided
```txt
1 0.589869281 0.490361446 0.326797386 0.527710843
0 0.323529412 0.585542169 0.189542484 0.351807229
```

* Finally, you need to create a dataset descriptor YAML-file that points to the created datasets and describes the object classes in them. This is a sample of this file for the data created above:
```yaml
train: ../train/images
val: ../val/images

nc: 2
names: ['cat','dog']
```
* **First two Lines** specify the path to images
* **nc** defines **N**umber of **C**lasses in the training
* **names** define the name of classes for training

Indexes of these items are numbers that you used when annotating the images, and these indexes will be returned by the model when it detects objects using the predict method. So, if you used "0" for cats, then it should be the first item in the names array.

> This YAML file should be passed to the train method of the model to start the training process.


## Reference
* https://www.freecodecamp.org/news/how-to-detect-objects-in-images-using-yolov8/
* https://cocodataset.org/#home
* https://universe.roboflow.com/roboflow-100/road-signs-6ih4y
* https://docs.ultralytics.com/modes/export/#usage-examples