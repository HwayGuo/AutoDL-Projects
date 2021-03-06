###############################################################
# NAS-Bench-201, ICLR 2020 (https://arxiv.org/abs/2001.00326) #
###############################################################
# Copyright (c) Xuanyi Dong [GitHub D-X-Y], 2020.06           #
###############################################################
# Usage: python exps/NAS-Bench-201/test-nas-api.py
###############################################################
import os, sys, time, torch, argparse
import numpy as np
from typing import List, Text, Dict, Any
from shutil import copyfile
from collections import defaultdict
from copy    import deepcopy
from pathlib import Path
import matplotlib
import seaborn as sns
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

lib_dir = (Path(__file__).parent / '..' / '..' / 'lib').resolve()
if str(lib_dir) not in sys.path: sys.path.insert(0, str(lib_dir))
from config_utils import dict2config, load_config
from nas_201_api import NASBench201API, NASBench301API
from log_utils import time_string
from models import get_cell_based_tiny_net


def test_api(api, is_301=True):
  print('{:} start testing the api : {:}'.format(time_string(), api))
  api.clear_params(12)
  api.reload(index=12)
  
  # Query the informations of 1113-th architecture
  info_strs = api.query_info_str_by_arch(1113)
  print(info_strs)
  info = api.query_by_index(113)
  print('{:}\n'.format(info))
  info = api.query_by_index(113, 'cifar100')
  print('{:}\n'.format(info))

  info = api.query_meta_info_by_index(115, '90' if is_301 else '200')
  print('{:}\n'.format(info))

  for dataset in ['cifar10', 'cifar100', 'ImageNet16-120']:
    for xset in ['train', 'test', 'valid']:
      best_index, highest_accuracy = api.find_best(dataset, xset)
    print('')
  params = api.get_net_param(12, 'cifar10', None)

  # Obtain the config and create the network
  config = api.get_net_config(12, 'cifar10')
  print('{:}\n'.format(config))
  network = get_cell_based_tiny_net(config)
  network.load_state_dict(next(iter(params.values())))

  # Obtain the cost information
  info = api.get_cost_info(12, 'cifar10')
  print('{:}\n'.format(info))
  info = api.get_latency(12, 'cifar10')
  print('{:}\n'.format(info))

  # Count the number of architectures
  info = api.statistics('cifar100', '12')
  print('{:}\n'.format(info))

  # Show the information of the 123-th architecture
  api.show(123)

  # Obtain both cost and performance information
  info = api.get_more_info(1234, 'cifar10')
  print('{:}\n'.format(info))
  print('{:} finish testing the api : {:}'.format(time_string(), api))


def test_issue_81_82(api):
  results = api.query_by_index(0, 'cifar10-valid', hp='12')
  results = api.query_by_index(0, 'cifar10-valid', hp='200')
  print(list(results.keys()))
  print(results[888].get_eval('valid'))
  print(results[888].get_eval('x-valid'))
  result_dict = api.get_more_info(index=0, dataset='cifar10-valid', iepoch=11, hp='200', is_random=False)


if __name__ == '__main__':

  api201 = NASBench201API(os.path.join(os.environ['TORCH_HOME'], 'NAS-Bench-201-v1_0-e61699.pth'), verbose=True)
  test_issue_81_82(api201)
  # test_api(api201, False)
  print ('Test {:} done'.format(api201))

  api201 = NASBench201API(None, verbose=True)
  test_issue_81_82(api201)
  test_api(api201, False)
  print ('Test {:} done'.format(api201))

  # api301 = NASBench301API(None, verbose=True)
  # test_api(api301, True)
