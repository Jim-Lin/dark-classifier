#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import argparse

def create_graph(model):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(args):
    answer = None

    if not tf.gfile.Exists(args.image):
        tf.logging.fatal('File does not exist %s', args.image)
        return answer

    image_data = tf.gfile.FastGFile(args.image, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph(args.model)

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-3:][::-1]  # Getting top 3 predictions
        f = open(args.labels, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k[0]]
        return answer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image',
        type=str,
        help='imagePath',
        required=True
    )
    parser.add_argument(
        '--model',
        type=str,
        help='modelFullPath',
        required=True
    )
    parser.add_argument(
        '--labels',
        type=str,
        help='labelsFullPath',
        required=True
    )

    args = parser.parse_args()
    run_inference_on_image(args)
