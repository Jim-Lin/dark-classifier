# dark-classifier(editing...)

## how to retrain
### docker image requisites
* bamos/openface
* gcr.io/tensorflow/tensorflow:latest-devel

### Step 1: collect face data
* /face/training-images/<xxx>/...
* /face/training-images/<yyy>/...
* /face/training-images/<zzz>/...
* ...

### (option) Step 2: face detection and alignment
`docker run -v /face:/face --rm bamos/openface /root/openface/util/align-dlib.py /face/training-images align outerEyesAndNose /face/aligned-images/ --size 96`

### (option) Step 3: check every face image count and convert png to jpeg
* [WARNING: Folder has less than 20 images, which may cause issues.](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/image_retraining/retrain.py#L157)

`python /face/util/png_to_jpeg.py --dir_from /face/aligned-images --dir_to /face/aligned-images-jpeg`

### Step 4: retrain model
* [How to Retrain Inception's Final Layer for New Categories](https://www.tensorflow.org/tutorials/image_retraining)

`docker run -v /face:/face --rm gcr.io/tensorflow/tensorflow:latest-devel python /tensorflow/tensorflow/examples/image_retraining/retrain.py --image_dir /face/<aligned-images-jpeg or training-images> --output_graph /face/output_graph.pb --output_labels /face/output_labels.txt --how_many_training_steps 2000 --model_dir /face/inception --bottleneck_dir /face/bottleneck`

and you will get the retrain model (output_graph.pb and output_labels.txt) to able to do DARK Facial Recognition

## how to classify
* [use the retrained model in a Python program](https://github.com/eldor4do/TensorFlow-Examples/blob/master/retraining-example.py)

`python label_image.py --image <face>.jpg --model /face/output_graph.pb --labels /face/output_labels.txt`
