import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/../utils')

import numpy as np
import matplotlib.pyplot as plt
from caffe2.python import core, model_helper, workspace, brew
from caffe2.proto import caffe2_pb2

import mobile_exporter
from data_utils import load_data

# core.GlobalInit(['caffe2', '--caffe2_log_level=10'])
#device_opts = core.DeviceOption(caffe2_pb2.CUDA, 0)

#frames, labels = load_data()
#labels = np.int32(labels)

arg_scope = {'order': 'NCHW'}
model = model_helper.ModelHelper(name='train_model')

#model.RunAllOnGPU()
#model.net.RunAllOnGPU()


brew.conv(model, 'data', 'conv1', dim_in=3, dim_out=20, kernel=5)
brew.max_pool(model, 'conv1', 'pool1', kernel=2)
brew.conv(model, 'pool1', 'conv2', dim_in=20, dim_out=30, kernel=5)
brew.max_pool(model, 'conv2', 'pool2', kernel=2)
brew.conv(model, 'pool2', 'conv3', dim_in=30, dim_out=40, kernel=5)
brew.max_pool(model, 'conv3', 'pool3', kernel=2)
brew.conv(model, 'pool3', 'conv4', dim_in=40, dim_out=50, kernel=5)
brew.max_pool(model, 'conv4', 'pool4', kernel=2)
brew.fc(model, 'pool4', 'fc1', dim_in=50 * 4 * 4, dim_out=300)
brew.relu(model, 'fc1', 'fc1')
brew.fc(model, 'fc1', 'fc2', dim_in=300, dim_out=300)
brew.relu(model, 'fc2', 'fc2')
brew.fc(model, 'fc2', 'pred', dim_in=300, dim_out=9)
softmax = brew.softmax(model, 'pred', 'softmax')
    
    
#def AddAccuracy(model, softmax, label):
#    accuracy = brew.accuracy(model, [softmax, label], 'accuracy')
#    return accuracy
#
#def AddTrainingOperators(model, softmax, label):
#    xent = model.LabelCrossEntropy([softmax, label], 'xent')
#    # compute the expected loss
#    loss = model.AveragedLoss(xent, 'loss')
#    # track the accuracy of the model
#    AddAccuracy(model, softmax, label)
#    # use the average loss we just computed to add gradient operators to the model
#    model.AddGradientOperators([loss])
#    # do a simple stochastic gradient descent
#    ITER = brew.iter(model, 'iter')
#    # set the learning rate schedule
#    LR = model.LearningRate(
#        ITER, 'LR', base_lr=-0.1, policy='step', stepsize=1, gamma=0.999 )
#    # ONE is a constant value that is used in the gradient update. We only need
#    # to create it once, so it is explicitly placed in param_init_net.
#    ONE = model.param_init_net.ConstantFill([], 'ONE', shape=[1], value=1.0)
#    # Now, for each parameter, we do the gradient updates.
#    for param in model.params:
#        # Note how we get the gradient of each parameter - ModelHelper keeps
#        # track of that.
#        param_grad = model.param_to_grad[param]
#        # The update is a simple weighted sum: param = param + param_grad * LR
#        model.WeightedSum([param, ONE, param_grad, LR], param)
#        
#def AddBookkeepingOperators(model):
#    '''This adds a few bookkeeping operators that we can inspect later.
#    
#    These operators do not affect the training procedure: they only collect
#    statistics and prints them to file or to logs.
#    '''    
#    # Print basically prints out the content of the blob. to_file=1 routes the
#    # printed output to a file. The file is going to be stored under
#    #     root_folder/[blob name]
#    model.Print('accuracy', [], to_file=1)
#    model.Print('loss', [], to_file=1)
#    # Summarizes the parameters. Different from Print, Summarize gives some
#    # statistics of the parameter, such as mean, std, min and max.
#    for param in model.params:
#        model.Summarize(param, [], to_file=1)
#        model.Summarize(model.param_to_grad[param], [], to_file=1)
#    # Now, if we really want to be verbose, we can summarize EVERY blob
#    # that the model produces; it is probably not a good idea, because that
#    # is going to take time - summarization do not come for free. For this
#    # demo, we will only show how to summarize the parameters and their
#    # gradients.   
#    
#
#    
##workspace.FeedBlob('data', frames, device_opts)
##workspace.FeedBlob('label', labels, device_opts)
#
##label = core.BlobReference('label')
##
##AddTrainingOperators(model, softmax, label)
##AddBookkeepingOperators(model)
#    


workspace.RunNetOnce(model.param_init_net)
# creating the network
#workspace.CreateNet(model.net, overwrite=True)
    
    
#total_iters = 1
#accuracy = np.zeros(total_iters)
#loss = np.zeros(total_iters)
#for i in range(total_iters):
#    workspace.RunNet(model.net)
#    accuracy[i] = workspace.FetchBlob('accuracy')
#    loss[i] = workspace.FetchBlob('loss')
#    print('epoch: {:4d} acc: {:6.4f} loss: {:6.4f}'.format(i, accuracy[i], loss[i]))
#plt.plot(loss, 'b')
#plt.plot(accuracy, 'r')
#plt.legend(('Loss', 'Accuracy'), loc='upper right')
#plt.show()
    


## Create our mobile exportable networks
#workspace.RunNetOnce(model.param_init_net)
init_net, predict_net = mobile_exporter.Export(workspace, model.net, model.params)
with open('init_net.pb', 'wb') as f:
    f.write(init_net.SerializeToString())
with open('predict_net.pb', 'wb') as f:
    f.write(predict_net.SerializeToString())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    
#    
#    
#    
#    
#    
## Populate the workspace with data
#np_data = frames
#print('Generated Random Data')
#workspace.FeedBlob('data', np_data)
#print('Feeded Random Data to Blob')
#
#workspace.CreateNet(model.net)
#workspace.RunNet(model.net)
#ref_out = workspace.FetchBlob('softmax')
#
## Clear the workspace
#workspace.ResetWorkspace()
#
## Populate the workspace with data
#workspace.RunNetOnce(init_net)
## Fake 'data' is populated by init_net, we have to replace it
#workspace.FeedBlob('data', np_data)
#
## Overwrite the old net
#workspace.CreateNet(predict_net, True)
#workspace.RunNet(predict_net.name)
#manual_run_out = workspace.FetchBlob('softmax')
#np.testing.assert_allclose(
#    ref_out, manual_run_out, atol=1e-10, rtol=1e-10
#)
#
## Clear the workspace
#workspace.ResetWorkspace()
#
## Predictor interface test (simulates writing to disk)
#predictor = workspace.Predictor(
#    init_net.SerializeToString(), predict_net.SerializeToString()
#)
#
## Output is a vector of outputs but we only care about the first and only result
#predictor_out = predictor.run([np_data])
#assert len(predictor_out) == 1
#predictor_out = predictor_out[0]
#
#np.testing.assert_allclose(
#    ref_out, predictor_out, atol=1e-10, rtol=1e-10
#)