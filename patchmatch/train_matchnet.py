# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 11:28:35 2018
@author: galad-loth
"""

import mxnet as mx
import logging
import sys
from metric_net import match_net
from data import get_UBC_patch_dataiter

logging.basicConfig(level=logging.INFO)

root_logger = logging.getLogger()
stdout_handler = logging.StreamHandler(sys.stdout)
root_logger.addHandler(stdout_handler)
root_logger.setLevel(logging.INFO)

def train_match_net():
    
    datadir="D:\\_Datasets\\UBCPatch"
    dataset="liberty"
    gt_file="m50_100000_100000_0.txt"
    batch_size=50
    train_iter,val_iter=get_UBC_patch_dataiter(datadir, dataset,gt_file, 
                                          batch_size,"siam",True, 0.05)
    model_prefix="checkpoint\\matchnet"
    checkpoint = mx.callback.do_checkpoint(model_prefix) 
    eval_metric=mx.metric.Accuracy()
    
    train_net=match_net(512,256)
    train_mod = mx.mod.Module(train_net,context=mx.gpu(),
                              data_names=['data1','data2'],label_names=["loss_label"])
    
    train_mod.bind(data_shapes=train_iter.provide_data,
                   label_shapes=train_iter.provide_label)
    #    train_mod.init_params()
    train_mod.fit(train_data=train_iter,
                eval_data=val_iter,
                initializer =mx.initializer.Xavier(),
                optimizer='sgd',
                optimizer_params={'learning_rate':0.01,
                                  "momentum":0.9,
                                  "wd":0.005,
                                  "lr_scheduler":mx.lr_scheduler.FactorScheduler(8000,0.9)},
                eval_metric=eval_metric,
                epoch_end_callback=checkpoint,
                num_epoch=10)
    
    
if __name__=="__main__":
    train_match_net()
