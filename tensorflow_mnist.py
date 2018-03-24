from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

INPUT_NODE = 784
OUTPUT_NODE = 10

LAYER1_NODE = 500
BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.1
LEARNING_RAE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

init = tf.initialize_all_variables()

def inference(input_tensor, avg_class, weights1, biases1,
              weights2, biases2):
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)

        return tf.matmul(layer1, weights2) + biases2
    else:
        layer1 = tf.nn.relu(
                tf.matmul(input_tensor, avg_class.average(weights1)) + 
                avg_class.average(biases1)
                )
        return (tf.matmul(layer1, avg_class.average(weights2)) + 
               avg_class.average(biases2))

def train(mnist):
    x = tf.placeholder(tf.float32, [None, INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name = 'y-input')

    weights1 = tf.Variable(
            tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1)
            )
    biases1 = tf.Variable(
            tf.constant(0.1, shape=[LAYER1_NODE])
            )
    weights2 = tf.Variable(
            tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1)
            )
    biases2 = tf.Variable(
            tf.constant(0.1, shape=[OUTPUT_NODE])
            )

    y = inference(x, None, weights1, biases1, weights2, biases2)

    global_step = tf.Variable(0, trainable = False)

    variable_averages = tf.train.ExponentialMovingAverage(
            MOVING_AVERAGE_DECAY, global_step
            )

    variables_averages_op = variable_averages.apply(
            tf.trainable_variables()
            )

    average_y = inference(
            x, variable_averages, weights1, biases1, weights2, biases2
            )

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels = tf.argmax(y_, 1), logits = y
            )

    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)

    regularization = regularizer(weights1) + regularizer(weights2)

    loss = cross_entropy_mean + regularization

    learning_rate = tf.train.exponential_decay(
            LEARNING_RATE_BASE,
            global_step,
            mnist.train.num_examples / BATCH_SIZE,
            LEARNING_RAE_DECAY
            )

    train_step = tf.train.GradientDescentOptimizer(learning_rate) \
               .minimize(loss, global_step = global_step)

    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name = 'train')

    correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # tf.initialize_all_variables().run()
        validate_feed = {x: mnist.validation.images,
                         y_: mnist.validation.labels}

        test_feed = {x: mnist.test.images, y_: mnist.test.labels}

        for i in range(TRAINING_STEPS):
            if i % 1000 == 0:
                validate_acc = sess.run(accuracy, feed_dict = validate_feed)
                print("After %d training step(s), validation accuracy "
                      "using average model is %g " % (i, validate_acc))

            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            sess.run(train_op, feed_dict = {x: xs, y_: ys})

        test_acc = sess.run(accuracy, feed_dict = test_feed)
        print("After %d training step(s), test accuracy using average "
                  "model is %g" % (TRAINING_STEPS, test_acc))

def main(argv = None):
    mnist = input_data.read_data_sets(train_dir= 'MNIST_DATA', one_hot=True)
    train(mnist)

if __name__ == '__main__':
    tf.app.run()

# print "Training data size: ", mnist.train.num_examples

# print "Validating data size: ", mnist.validation.num_examples
# 
# print "Testing data size: ", mnist.test.num_examples
# 
# print "Example training data: ", mnist.train.images[0]
# 
# print "Example training data label: ", mnist.train.labels[0]
