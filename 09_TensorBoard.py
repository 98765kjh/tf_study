# Can't get tensorboard graph...
# I don't know why :(

import tensorflow as tf
import numpy as np

xy = np.loadtxt('09_train.txt', unpack=True)
x_data = np.transpose(xy[0:-1])
y_data = np.reshape(xy[-1], (4,1))


X = tf.placeholder(tf.float32, name="X-input")
Y = tf.placeholder(tf.float32, name="Y-input")


W1 = tf.Variable(tf.random_uniform([2, 5], -1.0, 1.0), name="Weight1")
W2 = tf.Variable(tf.random_uniform([5, 3], -1.0, 1.0), name="Weight2")
W3 = tf.Variable(tf.random_uniform([3, 1], -1.0, 1.0), name="Weight3")


b1 = tf.Variable(tf.zeros([5]), name="Bias1")
b2 = tf.Variable(tf.zeros([3]), name="Bias2")
b3 = tf.Variable(tf.zeros([1]), name="Bias3")

with tf.name_scope("layer2") as scope:
    L2 = tf.sigmoid(tf.matmul(X, W1)+b1)

with tf.name_scope("layer3") as scope:
    L3 = tf.sigmoid(tf.matmul(L2, W2)+b2)

with tf.name_scope("layer4") as scope:
    hypothesis = tf.sigmoid(tf.matmul(L3, W3)+b3)


with tf.name_scope("cost") as scope:
    cost = tf.reduce_mean(-Y*tf.log(hypothesis)-(1-Y)*tf.log(1-hypothesis))
    cost_sum = tf.summary.scalar("cost", cost)

with tf.name_scope("train") as scope:
    optimizer = tf.train.GradientDescentOptimizer(0.3).minimize(cost)

with tf.name_scope("accuracy") as scope:
    answer = tf.equal(tf.floor(hypothesis + 0.5), Y)
    accuracy = tf.reduce_mean(tf.cast(answer, "float"))
    accuracy_sum = tf.summary.scalar("accuracy", accuracy)

w1_hist = tf.summary.histogram("Weight1", W1)
w2_hist = tf.summary.histogram("Weight2", W2)
w3_hist = tf.summary.histogram("Weight3", W3)

b1_hist = tf.summary.histogram("Bias1", b1)
b2_hist = tf.summary.histogram("Bias2", b2)
b3_hist = tf.summary.histogram("Bias3", b3)

y_hist = tf.summary.histogram("y", Y)


init = tf.global_variables_initializer()

with tf.Session() as session:
    session.run(init)
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("./log/xor_logs", session.graph)

    for step in xrange(20001):
        session.run(optimizer, feed_dict={X:x_data, Y:y_data})
        if step%2000==0:
            summary = session.run(merged, feed_dict={X:x_data, Y:y_data})
            writer.add_summary(summary, step)
