#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:59:37 2018

@author: maximoskaliakatsos-papakostas

Functions included:
- write_stream_to_midi

"""

import music21 as m21
import copy

def blend_single_feature(f1, f2, feature_index):
    ''' puts feature with index feature_index from f1 array and puts it in f2 '''
    f = copy.deepcopy(f2)
    f[ feature_index ] = f1[ feature_index ]
    return f
# end get_minimum_pitch