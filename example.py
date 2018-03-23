'''
import tensorflow as tf
a = tf.constant([1.0, 2.0], name = "a")
b = tf.constant([2.0, 3.0], name = "b")
result = tf.add(a, b, name = "add")
print result
'''
'''
import tensorflow as tf

init_op = tf.initialize_all_variables()
sess.run(init_op)

w1 = tf.Variable(tf.random_normal ([2, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal ([3, 1], stddev=1, seed=1))

x = tf.constant([[0.7, 0.9]])

a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

sess = tf.Session()

sess.run(w1.initializer)
sess.run(w2.initializer)

print(sess.run(y))
sess.close()
'''

'''
import tensorflow as tf

g1 = tf.Graph()
with g1.as_default():
    v = tf.get_variable(
            "v", shape=[1], initializer=tf.zeros_initializer
            )

g2 = tf.Graph()
with g2.as_default():
    v = tf.get_variable(
            "v", shape=[1], initializer=tf.ones_initializer
            )

with tf.Session(graph=g1) as sess:
    tf.global_variables_initializer
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))

with tf.Session(graph=g2) as sess:
    tf.global_variables_initializer
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))
'''


from __future__ import absolute_import
from __future__ import diviion
from __future__ import print_function

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

if __name__ == "__main__":
    tf.app.run()
