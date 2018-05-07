'''
Created on June 04, 2017
@author: v-lianji
'''

import tensorflow as tf
import math
from time import clock
import numpy as np
import sys
import os
import pickle
import sys
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from datetime import datetime

###Preprocessing the data from "txt" to "pkl"
def load_data_from_file_batching(file,batch_size):
    ref_date=datetime.strptime('1995-01-01','%Y-%m-%d')
    labels = []
    features = []
    cnt = 0
    required_col_num=80
    label_col_num=78
    label_col='FPS'
    string_col_num=[2,7,9,10,12,13,18,23,24,28,34,36,40,41,42,43,48,50,51,54,56,59,60,61,63,64,65,66,68,69,70,72,73,76,77]
    date_col_num=[17,55,57,58]
    date_col_format={17:'%b %Y',55:'%b-%d-%Y',57:'%b-%d-%Y',58:'%b-%d-%Y'}
    with open(file, 'r',encoding='utf-8') as rd:
        # rd.readline()
        while True:
            line = rd.readline()
            if not line:
                break
            cnt += 1
            if '#' in line:
                punc_idx = line.index('#')
            elif '\t\n' in line:
                punc_idx = line.index('\t\n')
            elif '\n' in line:
                punc_idx = line.index('\n')
            else:
                punc_idx = len(line)
            line=line[:punc_idx]
            # label = int(line[0:1])
            # feature_line = line[2:punc_idx]
            words = line.split('\t')
            if cnt == 1:
                if len(words) == required_col_num and words[label_col_num]==label_col:
                    continue
                else:
                    break
            cur_feature_list = []
            if len(words)!= required_col_num: continue
            for i,word in enumerate(words):
                if not word:
                    cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    continue
                if len(word) <= 0:
                    cur_feature_list.append([(i - 1) if i > label_col_num else i, float(0.0)])
                    continue
                if i==label_col_num:
                    label=float(word)
                elif i in string_col_num:
                    num=(hash(word) + 2.0 ** 31) / 2 ** 32
                    cur_feature_list.append([(i-1) if i>label_col_num else i, float(num)])
                elif i in date_col_num:
                ####handle date format
                    datetime_object = datetime.strptime(word, date_col_format.get(i))
                    feature_date = (datetime_object - ref_date).days
                    cur_feature_list.append([(i-1) if i>label_col_num else i, float(feature_date)])
                    # cur_feature_list.append([(i-1) if i>label_col_num else i, word])
                ####handle date format
                else:
                    cur_feature_list.append([(i-1) if i>label_col_num else i, float(word)])
            print(cur_feature_list)
            features.append(cur_feature_list)
            labels.append(label)
            if cnt == batch_size:
                yield labels, features
                labels = []
                features = []
                cnt = 0
    if cnt > 0:
        yield labels, features
# def load_data_from_file_batching(file, batch_size):
#     ref_date=datetime.strptime('1995-01-01','%Y-%m-%d')
#     labels = []
#     features = []
#     cnt = 0
#     with open(file, 'r') as rd:
#         while True:
#             line = rd.readline()
#             if not line:
#                 break
#             cnt += 1
#             if '#' in line:
#                 punc_idx = line.index('#')
#             elif '\n' in line:
#                 punc_idx = line.index('\n')
#             else:
#                 punc_idx = len(line)
#             label = int(line[0:1])
#             feature_line = line[2:punc_idx]
#             words = feature_line.split('\t')
#             cur_feature_list = []
#             for word in words:
#                 if not word:
#                     continue
#                 tokens = word.split(':')
#                 # if tokens[0]=='4532':
#                 #    print('line ', cnt, ':    ',word, '    line:', line)
#                 if len(tokens[1]) <= 0:
#                     tokens[1] = '0'
#                 if tokens[0] != '3':
#                     cur_feature_list.append([int(tokens[0]) - 1, float(tokens[1])])
#                 else:
#                 ####handle date format
#                     datetime_object = datetime.strptime(tokens[1], '%Y-%m-%d')
#                     feature_date = (datetime_object - ref_date).days
#                     cur_feature_list.append([int(tokens[0]) - 1, float(feature_date)])
#                 ####handle date format
#             features.append(cur_feature_list)
#             labels.append(label)
#             if cnt == batch_size:
#                 yield labels, features
#                 labels = []
#                 features = []
#                 cnt = 0
#     if cnt > 0:
#         yield labels, features

###interpret the train and test data
def prepare_data_4_sp(labels, features, dim):
    instance_cnt = len(labels)

    indices = []
    values = []
    values_2 = []
    shape = [instance_cnt, dim]
    feature_indices = []

    for i in range(instance_cnt):
        m = len(features[i])
        for j in range(m):
            indices.append([i, features[i][j][0]])
            values.append(features[i][j][1])
            values_2.append(features[i][j][1] * features[i][j][1])
            feature_indices.append(features[i][j][0])

    res = {}

    res['indices'] = np.asarray(indices, dtype=np.int64)
    res['values'] = np.asarray(values, dtype=np.float32)
    res['values2'] = np.asarray(values_2, dtype=np.float32)
    res['shape'] = np.asarray(shape, dtype=np.int64)
    res['labels'] = np.asarray([[label] for label in labels], dtype=np.float32)
    res['feature_indices'] = np.asarray(feature_indices, dtype=np.int64)

    return res

###Load the "pkl" file to get all data
def load_data_cache(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

###function to call the preprocessing process
def pre_build_data_cache(infile, outfile, feature_cnt, batch_size):
    wt = open(outfile, 'wb')
    for labels, features in load_data_from_file_batching(infile, batch_size):
        input_in_sp = prepare_data_4_sp(labels, features, feature_cnt)
        pickle.dump(input_in_sp, wt)
    wt.close()

###call "build_model", load all the data and train the machine
def single_run(feature_cnt, field_cnt,  params):

    print (params)

    pre_build_data_cache_if_need(params['train_file'], feature_cnt, params['batch_size'])
    pre_build_data_cache_if_need(params['test_file'], feature_cnt, params['batch_size'])

    params['train_file'] = params['train_file'].replace('.csv','.pkl').replace('.txt','.pkl')
    params['test_file'] = params['test_file'].replace('.csv','.pkl').replace('.txt','.pkl')

    print('start single_run')

    tf.reset_default_graph()

    n_epoch = params['n_epoch']
    batch_size = params['batch_size']

    _indices = tf.placeholder(tf.int64, shape=[None, 2], name='raw_indices')
    _values = tf.placeholder(tf.float32, shape=[None], name='raw_values')
    _values2 = tf.placeholder(tf.float32, shape=[None], name='raw_values_square')
    _shape = tf.placeholder(tf.int64, shape=[2], name='raw_shape')

    _y = tf.placeholder(tf.float32, shape=[None,1], name='Y')
    _ind = tf.placeholder(tf.int64, shape=[None])

    # train_step, loss, error, preds, merged_summary, tmp = build_model(_indices, _values, _values2, _shape, _y, _ind,
    #                                                              feature_cnt, field_cnt, params)
    train_step, loss, error, preds, tmp = build_model(_indices, _values, _values2, _shape, _y, _ind,
                                                                 feature_cnt, field_cnt, params)

    # auc = tf.metrics.auc(_y, preds)


    saver = tf.train.Saver()
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    log_writer = tf.summary.FileWriter(params['log_path'], graph=sess.graph)

    glo_ite = 0

    saver.restore(sess, 'models/[3200, 1600, 1600]0.001-72905')

    for eopch in range(n_epoch):
        if eopch < 72905: continue
        iteration = -1
        start = clock()

        time_load_data, time_sess = 0, 0
        time_cp02 = clock()

        train_loss_per_epoch = 0

        for training_input_in_sp in load_data_cache(params['train_file']):
            time_cp01 = clock()
            time_load_data += time_cp01 - time_cp02
            iteration += 1
            glo_ite += 1
            # _,  cur_loss, summary, _tmp = sess.run([train_step,  loss, merged_summary, tmp], feed_dict={
            #     _indices: training_input_in_sp['indices'], _values: training_input_in_sp['values'],
            #     _shape: training_input_in_sp['shape'], _y: training_input_in_sp['labels'],
            #     _values2: training_input_in_sp['values2'], _ind: training_input_in_sp['feature_indices']
            # })
            _,  cur_loss, _tmp = sess.run([train_step,  loss, tmp], feed_dict={
                _indices: training_input_in_sp['indices'], _values: training_input_in_sp['values'],
                _shape: training_input_in_sp['shape'], _y: training_input_in_sp['labels'],
                _values2: training_input_in_sp['values2'], _ind: training_input_in_sp['feature_indices']
            })

            time_cp02 = clock()

            time_sess += time_cp02 - time_cp01
            # print('Train Value Length',len(training_input_in_sp['values']))
            print('Loss',cur_loss)
            # print('Div Error',_div_error)
            train_loss_per_epoch += cur_loss
            # print(_tmp)

            # log_writer.add_summary(summary, glo_ite)
        end = clock()
        #print('time for eopch ', eopch, ' ', "{0:.4f}min".format((end - start) / 60.0), ' time_load_data:', "{0:.4f}".format(time_load_data), ' time_sess:',
        #      "{0:.4f}".format(time_sess), ' train_loss: ', train_loss_per_epoch, ' train_error: ', train_error_per_epoch)
        if eopch % 5 == 0:
            model_path = params['model_path'] + "/" + str(params['layer_sizes']).replace(':', '_') + str(
                params['reg_w_linear']).replace(':', '_')
            os.makedirs(model_path, exist_ok=True)
            saver.save(sess, model_path, global_step=eopch)
            auc=predict_test_file(preds, sess, params['test_file'], feature_cnt, _indices, _values, _shape, _y,
                              _values2, _ind, eopch, batch_size, 'test', model_path, params['output_predictions'])
            print('auc is ', auc, ', at epoch  ', eopch, ', time is {0:.4f} min'.format((end - start) / 60.0)
                  , ', train_loss is {0:.2f}'.format(train_loss_per_epoch))


    log_writer.close()

###Predict the result of test data and compare the results between predicted FPS and the train data FPS
def predict_test_file(preds, sess, test_file, feature_cnt, _indices, _values, _shape, _y, _values2, _ind, epoch,
                      batch_size, tag, path, output_prediction = True):
    if output_prediction:
        wt = open(path + '/deepFM_pred_' + tag + str(epoch) + '.txt', 'w')

    gt_scores = []
    pred_scores = []

    for test_input_in_sp in load_data_cache(test_file):
        predictions = sess.run(preds, feed_dict={
            _indices: test_input_in_sp['indices'], _values: test_input_in_sp['values'],
            _shape: test_input_in_sp['shape'], _y: test_input_in_sp['labels'], _values2: test_input_in_sp['values2'],
            _ind: test_input_in_sp['feature_indices']
        })#.reshape(-1).tolist()
        # print('Prediction:',predictions)
        print('Value Length:',len(test_input_in_sp['values']))
        print('Y:', test_input_in_sp['labels'].reshape(-1).tolist())
        predictions=predictions.reshape(-1).tolist()
        print('Prediction:',predictions)
        if output_prediction:
            for (gt, preded) in zip(test_input_in_sp['labels'].reshape(-1).tolist(), predictions):
                wt.write('{0:d},{1:f}\n'.format(int(gt), preded))
                gt_scores.append(gt)
                #pred_scores.append(1.0 if preded >= 0.5 else 0.0)
                pred_scores.append(preded)
        else:
            gt_scores.extend(test_input_in_sp['labels'].reshape(-1).tolist())
            pred_scores.extend(predictions)
    fpr, tpr, thresholds = metrics.roc_curve(np.asarray(gt_scores).astype(np.int), np.asarray(pred_scores).astype(np.int),pos_label=5)
    auc =metrics.auc(fpr, tpr)
    # auc = roc_auc_score(np.asarray(gt_scores), np.asarray(pred_scores))
    print('auc is ', auc, ', at epoch  ', epoch)
    if output_prediction:
        wt.close()
    return auc


###Python function to build a FPS Estimator based on DeepFM model
def build_model(_indices, _values, _values2, _shape, _y, _ind, feature_cnt, field_cnt, params):
    eta = tf.constant(params['eta'])
    _x = tf.SparseTensor(_indices, _values, _shape)  # m * feature_cnt sparse tensor
    _xx = tf.SparseTensor(_indices, _values2, _shape)

    model_params = []
    tmp = []

    init_value = params['init_value']
    dim = params['dim']
    layer_sizes = params['layer_sizes']

    w_linear = tf.Variable(tf.truncated_normal([feature_cnt, 1], stddev=init_value, mean=0), name='w_linear',
                           dtype=tf.float32)
        # w_linear = tf.Variable(tf.truncated_normal([feature_cnt, params['n_classes']], stddev=init_value, mean=0),  #tf.random_uniform([feature_cnt, 1], minval=-0.05, maxval=0.05),
        #                     name='w_linear', dtype=tf.float32)
    bias = tf.Variable(tf.truncated_normal([1], stddev=init_value, mean=0), name='bias')
        # bias = tf.Variable(tf.truncated_normal([1,params['n_classes']], stddev=init_value, mean=0), name='bias')
    tmp.append({'Bias':tf.shape(bias)})
    model_params.append(bias)
    model_params.append(w_linear)
    preds=bias
    # logits = bias
    # linear part
    preds += tf.sparse_tensor_dense_matmul(_x, w_linear, name='contr_from_linear')
    tmp.append({'Logits After contr from linear':tf.shape(preds)})
    w_fm = tf.Variable(tf.truncated_normal([feature_cnt, dim], stddev=init_value / math.sqrt(float(dim)), mean=0),
                           name='w_fm', dtype=tf.float32)
    model_params.append(w_fm)
    # fm order 2 interactions
    if params['is_use_fm_part']:
        preds = preds + 0.5 * tf.reduce_sum(
            tf.pow(tf.sparse_tensor_dense_matmul(_x, w_fm), 2) - tf.sparse_tensor_dense_matmul(_xx, tf.pow(w_fm, 2)), 1,
            keep_dims=True)
        tmp.append({'Logits After FM Part': tf.shape(preds)})
    # deep neural network
    if params['is_use_dnn_part']:
        w_fm_nn_input = tf.reshape(tf.gather(w_fm, _ind) * tf.expand_dims(_values, 1), [-1, field_cnt * dim])
        w_nn_input=tf.Variable(tf.truncated_normal([feature_cnt, feature_cnt* dim], stddev=init_value, mean=0), name='w_linear',
                dtype=tf.float32)
    # w_fm_nn_input=tf.sparse_tensor_dense_matmul(_x, w_nn_input, name='w_nn_input')
        print(w_fm_nn_input.shape)
        model_params.append(w_nn_input)
    # tmp.append(tf.shape(tf.expand_dims(_values, 1)))
    # tmp.append(tf.shape(w_fm_nn_input))
    # tmp.append(tf.shape(tf.gather(w_fm, _ind) * tf.expand_dims(_values, 1)))
    # tmp.append(tf.shape(tf.gather(w_fm, _ind)))


    #w_nn_layers = []
        hidden_nn_layers = []
        hidden_nn_layers.append(w_fm_nn_input)
        last_layer_size = field_cnt * dim
        layer_idx = 0

        w_nn_params = []
        b_nn_params = []

        for layer_size in layer_sizes:
            cur_w_nn_layer = tf.Variable(
                tf.truncated_normal([last_layer_size, layer_size], stddev=init_value / math.sqrt(float(10)), mean=0),
                name='w_nn_layer' + str(layer_idx), dtype=tf.float32)

            cur_b_nn_layer = tf.Variable(tf.truncated_normal([layer_size], stddev=init_value, mean=0), name='b_nn_layer' + str(layer_idx)) #tf.get_variable('b_nn_layer' + str(layer_idx), [layer_size], initializer=tf.constant_initializer(0.0))

            cur_hidden_nn_layer = tf.nn.xw_plus_b(hidden_nn_layers[layer_idx], cur_w_nn_layer, cur_b_nn_layer)

            if params['activations'][layer_idx]=='tanh':
                cur_hidden_nn_layer = tf.nn.tanh(cur_hidden_nn_layer)
            elif params['activations'][layer_idx]=='sigmoid':
                cur_hidden_nn_layer = tf.nn.sigmoid(cur_hidden_nn_layer)
            elif params['activations'][layer_idx]=='relu':
                cur_hidden_nn_layer = tf.nn.relu(cur_hidden_nn_layer)

            #cur_hidden_nn_layer = tf.matmul(hidden_nn_layers[layer_idx], cur_w_nn_layer)
            #w_nn_layers.append(cur_w_nn_layer)

            hidden_nn_layers.append(cur_hidden_nn_layer)

            layer_idx += 1
            last_layer_size = layer_size

            model_params.append(cur_w_nn_layer)
            model_params.append(cur_b_nn_layer)
            w_nn_params.append(cur_w_nn_layer)
            b_nn_params.append(cur_b_nn_layer)
        hidden_nn_layers[-1]=tf.nn.dropout(hidden_nn_layers[-1],params['drop_out_rate'])
    # cur_hidden_nn_layer=tf.nn.dropout(cur_hidden_nn_layer,params['drop_out_rate'])
        # w_nn_output = tf.Variable(tf.truncated_normal([last_layer_size, params['n_classes']], stddev=init_value, mean=0), name='w_nn_output',
        #                           dtype=tf.float32)
    # w_nn_output = tf.Variable(tf.truncated_normal([last_layer_size, 1], stddev=init_value, mean=0),
    #                           name='w_nn_output',
    #                           dtype=tf.float32)
    # w_nn_output = tf.Variable(
    #     tf.truncated_normal([last_layer_size, 1], stddev=init_value / math.sqrt(float(10)), mean=0),
    #     name='w_nn_output', dtype=tf.float32)
        w_nn_output = tf.Variable(
            tf.truncated_normal([last_layer_size, 1], stddev=init_value / math.sqrt(float(10)), mean=0),
            name='w_nn_output', dtype=tf.float32)
        # b_nn_layer = tf.Variable(tf.truncated_normal([1], stddev=init_value, mean=0),
        #                              name='b_nn_output')  # tf.get_variable('b_nn_layer' + str(layer_idx), [layer_size], initializer=tf.constant_initializer(0.0))
        b_nn_layer = tf.Variable(tf.truncated_normal([1], stddev=init_value, mean=0),
                                     name='b_nn_output')
        # nn_output = tf.matmul(hidden_nn_layers[-1], w_nn_output)
        nn_output=tf.nn.xw_plus_b(hidden_nn_layers[-1], w_nn_output, b_nn_layer)
        model_params.append(w_nn_output)
        w_nn_params.append(w_nn_output)
        model_params.append(b_nn_layer)
        b_nn_params.append(b_nn_layer)
        preds+=nn_output

        ###
    logits = tf.sigmoid(preds)
    w_nn_softmax = tf.Variable(
        tf.truncated_normal([1, 1], stddev=0.5, mean=0),
        name='w_nn_softmax', dtype=tf.float32)
    b_nn_softmax = tf.Variable(tf.truncated_normal([1], stddev=100, mean=0),
                               name='b_nn_softmax')  # tf.get_variable('b_nn_layer' + str(layer_idx), [layer_size], initializer=tf.constant_initializer(0.0))
    # nn_output = tf.matmul(hidden_nn_layers[-1], w_nn_output)
    nn_softmax = tf.nn.xw_plus_b(logits, w_nn_softmax, b_nn_softmax)
    model_params.append(w_nn_softmax)
    model_params.append(b_nn_softmax)
    ###
    preds = nn_softmax
    # logits=nn_output
    # preds=nn_output
    # tmp.append({'Logits After NN Part': tf.shape(logits)})
    # if params['loss'] == 'cross_entropy_loss': # 'loss': 'log_loss'
    #     # preds=logits
    #     error = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=tf.reshape(logits,[-1])
    #                                                                    , labels=tf.reshape(_y,[-1])))
    # elif params['loss'] == 'square_loss':
        # preds=logits

        #error = tf.reduce_mean(tf.squared_difference(preds, _y))
    error = tf.reduce_mean(tf.reduce_sum(tf.square(tf.subtract(_y, preds))
                                         #,                                            reduction_indices=[1]
                                          ))
    # divide_per_epoch=tf.constant(10,shape=[1],dtype=tf.float32)
    # max_error=tf.constant(10 ** 10,shape=[1],dtype=tf.float32)
    # error=tf.reshape(error,[1])
    # div_error=tf.div(error,divide_per_epoch)
    # div_error=tf.greater(error,max_error)
    # error=tf.minimum(error,10**10)
    # while tf.greater(error,max_error) is not None:
    #     error=tf.div(error,divide_per_epoch)
        # print('ssssd')
    # elif params['loss'] == 'log_loss':
    #     # preds=logits
    #     #preds = tf.sigmoid(logits)
    #     error = tf.reduce_mean(tf.losses.log_loss(predictions=preds,labels=_y))

    # else:
    #     preds=tf.argmax(input=logits,axis=1,name='predictions')
    #     onehot_labels = tf.one_hot(indices=tf.cast(_y, tf.int64), depth=params['n_classes'])
    #     onehot_labels = tf.reshape(onehot_labels, (tf.shape(_y)[0], params['n_classes']))
    #     error=tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels,logits=logits)
    # tmp.append({'Logits After Calc Loss': tf.shape(logits)})

    lambda_w_linear = tf.constant(params['reg_w_linear'], name='lambda_w_linear')
    lambda_w_fm = tf.constant(params['reg_w_fm'], name='lambda_w_fm')
    lambda_w_nn = tf.constant(params['reg_w_nn'], name='lambda_nn_fm')
    lambda_w_l1 = tf.constant(params['reg_w_l1'], name='lambda_w_l1')
    #
    # l2_norm = tf.multiply(lambda_w_linear, tf.pow(bias, 2)) + tf.reduce_sum(
    #     tf.add(tf.multiply(lambda_w_linear, tf.pow(w_linear, 2)),
    #            tf.multiply(lambda_w_fm, tf.pow(w_fm, 2)))) + tf.reduce_sum(
    #     tf.multiply(lambda_w_nn, tf.pow(w_nn_output, 2)))

    # l2_norm = tf.multiply(lambda_w_linear, tf.pow(bias, 2)) \
    #           + tf.multiply(lambda_w_linear, tf.reduce_sum(tf.pow(w_linear, 2)))

    l2_norm = tf.multiply(lambda_w_linear, tf.reduce_sum(tf.pow(w_linear, 2)))
    l2_norm += tf.multiply(lambda_w_l1, tf.reduce_sum(tf.abs(w_linear)))
    #
    if params['is_use_fm_part'] or params['is_use_dnn_part']:
        l2_norm += tf.multiply(lambda_w_fm, tf.reduce_sum(tf.pow(w_fm, 2)))

    if params['is_use_dnn_part']:
        for i in range(len(w_nn_params)):
            l2_norm += tf.multiply(lambda_w_nn, tf.reduce_sum(tf.pow(w_nn_params[i], 2)))

        for i in range(len(b_nn_params)):
            l2_norm += tf.multiply(lambda_w_nn, tf.reduce_sum(tf.pow(b_nn_params[i], 2)))
    l2_norm+=tf.multiply(lambda_w_nn,tf.reduce_sum(tf.pow(w_nn_softmax,2)))
    l2_norm+=tf.multiply(lambda_w_nn,tf.reduce_sum(tf.pow(b_nn_softmax,2)))
    #
    tmp.append(tf.shape(tf.pow(w_linear, 2)))
    tmp.append(tf.shape(tf.pow(w_fm, 2)))


    # loss=error
    loss = tf.add(error, l2_norm)
    # if params['optimizer']=='adadelta':
    # train_step = tf.train.AdadeltaOptimizer(eta).minimize(loss,var_list=model_params)
    # elif params['optimizer']=='sgd':
    # train_step = tf.train.GradientDescentOptimizer(params['learning_rate']).minimize(loss,var_list=model_params)
    # elif params['optimizer']=='adam':
    train_step = tf.train.AdamOptimizer(params['learning_rate']).minimize(loss,var_list=model_params)
    # train_step = tf.train.AdamOptimizer(params['learning_rate']).minimize(loss)

    # elif params['optimizer']=='ftrl':
    #     train_step = tf.train.FtrlOptimizer(params['learning_rate']).minimize(loss,var_list=model_params)
    # else:
    #     train_step = tf.train.GradientDescentOptimizer(params['learning_rate']).minimize(loss,var_list=model_params)

    # tf.summary.scalar('square_error', error)
    # tf.summary.scalar('loss', loss)
    # tf.summary.histogram('linear_weights_hist', w_linear)

    # if params['is_use_fm_part']:
    #     tf.summary.histogram('fm_weights_hist', w_fm)
    # if params['is_use_dnn_part']:
    # for idx in range(len(w_nn_params))  :
    #     tf.summary.histogram('nn_layer'+str(idx)+'_weights', w_nn_params[idx])

    # merged_summary = tf.summary.merge_all()

    # return train_step, loss, error, preds, merged_summary, tmp
    return train_step, loss, error, preds, tmp

###Check if the pkl file is existed, generate it if no
def pre_build_data_cache_if_need(infile, feature_cnt, batch_size):
    outfile = infile.replace('.csv','.pkl').replace('.txt','.pkl')
    if not os.path.isfile(outfile):
        print('pre_build_data_cache for ', infile)
        pre_build_data_cache(infile, outfile, feature_cnt, batch_size)
        print('pre_build_data_cache finished.' )


###The actual program to run the FPS estimator and the main flow of this program
###Read or pre-processing the data
###Build a DeepFM model based on the setting
###Train the DeepFM
###Test the DeepFM and compare the results
def run():
    # train_file = r'\\mlsdata\e$\Users\v-lianji\DeepRecsys\DeepFM\part01.svmlight_balanced.csv'
    # test_file = r'\\mlsdata\e$\Users\v-lianji\DeepRecsys\DeepFM\part02.svmlight.csv'

    print ('begin running')

    field_cnt = 79 #83
    feature_cnt = 79 #5000
    # field_cnt = 39 #83
    # feature_cnt = 39 #5000


    params = {
        'reg_w_linear': 0.001, 'reg_w_fm':0.001, 'reg_w_nn': 0.001,  #0.001
        'reg_w_l1': 0.001,
        'init_value': 20,
        'layer_sizes': [3200, 1600, 1600],
        'activations':['relu','relu', 'relu'],
        'eta': 0.3,
        'n_epoch': 10000000,  # 500
        'batch_size': 1,
        'dim': 20,
        'model_path': 'models',
        'log_path': 'logs/' + datetime.utcnow().strftime('%Y-%m-%d_%H_%M_%S'),
        'train_file':  'data/train.txt',  #'data/part01.svmlight_balanced.csv',
        'test_file':    'data/test.txt',#'data/part02.svmlight.csv',
        # 'train_file': 'data/tryData-train.txt',
        # 'test_file': 'data/tryData-test.txt',
        'output_predictions':True,
        'is_use_fm_part':True,
        'is_use_dnn_part':True,
        'learning_rate':0.01, # [0.001, 0.01]
        'loss': 'cross_entropy_loss', # [cross_entropy_loss, square_loss, log_loss]
        'optimizer':'adam', # [adam, ftrl, sgd]
        'drop_out_rate': 0.8#0.8,
        #'n_classes':6
    }


    single_run(feature_cnt, field_cnt, params)


if __name__ == '__main__':
    run()