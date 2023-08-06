#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from .clustermap import heatmap,ClusterMapPlotter,composite
from .annotations import *
from .dotHeatmap import *
from .colors import *
from .tools import *
# from .example import *

#__all__=['*']
__version__='1.3.8'

_ROOT = os.path.abspath(os.path.dirname(__file__))
