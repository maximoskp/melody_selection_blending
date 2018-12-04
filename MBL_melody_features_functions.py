#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:05:00 2018

@author: maximoskaliakatsos-papakostas

Accepted feature labels:
- 'r_density'
- 'r_inhomogeneity'
- 'pcp_entropy'
- 'small_intervals'

Functions included:
- get_features_of_stream
- compute_feature
- get_accepted_feature_labels
- compute_rhythm_density
- compute_rhythm_inhomogeneity
- compute_pcp_entropy
- compute_small_intervals
- compute_melody_markov_transitions

"""

# import music21 as m21
import numpy as np
import scipy.stats as sc

def get_accepted_feature_labels():
    ''' returns a list of strings that correspond to feature computation functions '''
    return ['r_density', 'r_inhomogeneity', 'pcp_entropy', 'small_intervals']
# end get_accepted_feature_labels

def compute_rhythm_density(s):
    # isolate all note events
    notes = []
    # take flat notes from all parts
    for p in s.parts:
        notes.extend( p.flat.notes )
    # isolate all offsets
    offs = []
    # for all notes in all parts
    for n in notes:
        offs.append( n.offset )
    # keep only unique offsets
    offs_unique = list(set( offs ))
    # suppose that there is a maximum of 4 notes per offset unit (16ths)
    # and compute the maximum expected number of offsets
    expected_offsets = 4.0*max(offs_unique)
    # compute actual offets over expected
    return len(offs_unique)/expected_offsets
# end compute_rhythm_density
def compute_rhythm_inhomogeneity(s):
    # isolate all note events
    notes = []
    # take flat notes from all parts
    for p in s.parts:
        notes.extend( p.flat.notes )
    # isolate all offsets
    offs = []
    # for all notes in all parts
    for n in notes:
        offs.append( n.offset )
    # keep only unique offsets
    offs_unique = np.array( list(set( offs )) )
    # sort offsets to make sure
    sorted_offs = np.sort( offs_unique )
    # get differences in offsets
    diff_offs = np.diff( sorted_offs )
    # return std over mean
    return np.std(diff_offs)/np.mean(diff_offs)
# end compute_rhythm_inhomogeneity
def compute_pcp_entropy(s):
    # isolate all note events
    notes = []
    # take flat notes from all parts
    for p in s.parts:
        notes.extend( p.flat.notes )
    # isolate all midi notes
    midis = []
    # for all notes in all parts
    for n in notes:
        midis.append( n.pitch.midi)
    # compute pcp
    pcp = np.histogram( np.mod(midis, 12), bins=12 )[0]
    # return entropy
    return sc.entropy( pcp )
# end compute_pcp_entropy
def compute_small_intervals(s):
    # stream is considered monophonic
    # isolate all note events
    notes = []
    # take flat notes from all parts
    for p in s.parts:
        notes.extend( p.flat.notes )
    # isolate all midi notes
    midis = []
    # for all notes in all parts
    for n in notes:
        midis.append( n.pitch.midi)
    # small intervals percentage
    d = np.diff( np.array( midis ) )
    dd = d[ d!=0 ]
    return np.sum(np.abs(dd) < 3)/np.size(dd)
# end compute_small_intervals
def compute_melody_markov_transitions(s):
    # stream is considered monophonic
    # initialise 128x128 Markov transition matrix
    m = np.zeros( (128,128) )
    # isolate all note events
    notes = []
    # take flat notes from all parts
    for p in s.parts:
        notes.extend( p.flat.notes )
    # isolate all midi notes
    midis = []
    # for all notes in all parts
    for n in notes:
        midis.append( n.pitch.midi)
    # construct sums
    for i in range(len(midis)-1):
        m[ midis[i], midis[i+1] ] = m[ midis[i], midis[i+1] ] + 1
    # make probabilities
    for i in range(m.shape[0]):
        tmpSum = np.sum(m[i,:])
        if tmpSum > 0:
            m[i,:] = m[i,:]/tmpSum
    return m
# end compute_melody_markov_transitions

def compute_feature(s, label):
    ''' gets a stream s and an accepted label and returns the numeric value
        of the requested feature '''
    # initialise an empty feature value
    f = []
    # first check if given label is accepted
    if label in get_accepted_feature_labels():
        if label is 'r_density':
            f = compute_rhythm_density(s)
        elif label is 'r_inhomogeneity':
            f = compute_rhythm_inhomogeneity(s)
        elif label is 'pcp_entropy':
            f = compute_pcp_entropy(s)
        elif label is 'small_intervals':
            f = compute_small_intervals(s)
        else:
            print('wtf?')
    else:
        print('feature label: ', label, ' not in accepted list')
    return f
    # don't forget to compute and return feature!
# end compute_feature

def get_features_of_stream(s, feature_labels=['r_density', 'r_inhomogeneity', 'pcp_entropy', 'small_intervals']):
    ''' gets a stream s and an array of the desired feature labels and
        returns an np array with the requested feature values'''
    # initialise an empty array of features
    f = []
    # start appending feature values
    for lb in feature_labels:
        f.append( compute_feature(s, lb) )
    # return final np array
    return np.array(f)
# end get_features_of_stream