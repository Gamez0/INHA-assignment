import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("./mnist/data/", one_hot=True)
#making nueral model
#to use cnn make it in 2d
X = tf.placeholder(tf.float32, [None, 28, 28, 1])
Y = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)
# each var and layer are set
# W1 [3 3 1 32] -> [3 3]: size of kernell, 1: inputed X , 32: number of filter
# L1 Conv shape=(?, 28, 28, 32)
#    Pool     ->(?, 14, 14, 32)
W1 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
#using tf.nn.conv2d we can make a conv that move one point
#padding='SAME' is moving one more at the edge in kernell sliding
L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
L1 = tf.nn.relu(L1)
#Pooling can also use tf.nn.max_pool to set easily
L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
L1 = tf.nn.dropout(L1, keep_prob)

#L2 Conv shape is=(?, 14, 14, 64)
#   Pool is     ->(?, 7, 7, 64)
#W2's [3, 3, 32, 64] 32 is the size of filter that is printed int w1 in L1
W2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
L2 = tf.nn.relu(L2)
L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
L2 = tf.nn.dropout(L2, keep_prob)

#input 7x7x64 -> output 256
#For full connection we bring the Pool size(?,7,7,64)from just before tom make dimension
#Reshapeing -> (?,256) 
W3 = tf.Variable(tf.random_normal([7 * 7 * 64, 256], stddev=0.01))
L3 = tf.reshape(L2, [-1, 7 * 7 * 64])
L3 = tf.matmul(L3, W3)
L3 = tf.nn.relu(L3)
L3 = tf.nn.dropout(L3, keep_prob)

#get the final ouput from L3, get 256 as input date make 10 printout in 0~9label
W4 = tf.Variable(tf.random_normal([256, 10], stddev=0.01))
model = tf.matmul(L3, W4)

# change the func to RMSPropOptimizer and check the result
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
#optimizer = tf. train.RMSPropOptimizer(0.001,0.9).minimize(cost)
#########
# training
######
init = tf.global_variables_initializer() # init = op that initialize global var
sess = tf.Session() # a class for running tensorflow opertation
sess.run(init) #run session

batch_size = 100 # number of picture worked in one time
total_batch = int(mnist.train.num_examples / batch_size) # all example / batch size

for epoch in range(15): # after using one batch it means one epoch has past
    total_cost = 0

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        # reshape to [28 28 1] to use in cnnm model
        batch_xs = batch_xs.reshape(-1, 28, 28, 1) # reshapeing the tensor

        _, cost_val = sess.run([optimizer, cost],
                               feed_dict={X: batch_xs, # feed values to the tensorflow
                                          Y: batch_ys,
                                          keep_prob: 0.7}) # give keep_prob to feed_dict
        total_cost += cost_val

    print('Epoch:', '%04d' % (epoch + 1),
          'Avg. cost =', '{:.3f}'.format(total_cost / total_batch)) #one epoch done

print('Finish!')

#########
# Check result
######
is_correct = tf.equal(tf.argmax(model, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('Accuracy:', sess.run(accuracy,
                        feed_dict={X: mnist.test.images.reshape(-1, 28, 28, 1),
                                   Y: mnist.test.labels,
                                   keep_prob: 1}))

#########
# Check result (matplot)
######
labels = sess.run(model,
                  feed_dict={X: mnist.test.images.reshape(-1, 28, 28, 1),
                             Y: mnist.test.labels,
                             keep_prob: 1})

fig = plt.figure()
for i in range(10):
    subplot = fig.add_subplot(2, 5, i + 1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.set_title('%d' % np.argmax(labels[i]))
    subplot.imshow(mnist.test.images[i].reshape((28, 28)),
                   cmap=plt.cm.gray_r)

plt.show()