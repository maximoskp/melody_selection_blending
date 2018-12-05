#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 15:59:37 2018

@author: maximoskaliakatsos-papakostas

Functions included:
- neutral_transposition
- fix_lowest_octave
- get_minimum_midi_pitch

"""

import music21 as m21

def get_minimum_pitch(s):
    ''' scans all notes in all parts of stream s and returns the lowest pitch 
        as a m21 pitch object'''
    # initialise minimum pitch
    m = m21.pitch.Pitch(127)
    # scan all parts
    for p in s.parts:
        # can all notes in part
        for n in p.flat.notes:
            # and compare them with minimum pitch
            if n.pitch < m:
                m = n.pitch
    return m
# end get_minimum_pitch

def neutral_transposition(s):
    ''' gets a stream s and returns a stream in C maj or Amin key '''
    # get tonality
    k = s.analyze('key.krumhanslschmuckler')
    # major and minor class modes
    major_class = {'major', 'mixolydian', 'lydian'}
    # minor_class = {'minor', 'dorian', 'phrygian', 'locrian'}
    # get mode for transposing
    m = k.mode
    # get tonic pitch
    t = k.tonic
    # get transposition interval depending on mode
    if m in major_class:
        i = m21.interval.Interval(t, m21.pitch.Pitch('C'))
    else:
        i = m21.interval.Interval(t, m21.pitch.Pitch('A'))
    # transpose
    s_trans = s.transpose(i)
    return s_trans
# end neutral_transposition

def fix_lowest_octave(s, lowest_pitch=60):
    ''' gest a stream s and returns a stream in the same key but
        with its lowest pitch in a given octave - just above a lowestpitch '''
    # find minimum pitch
    m = get_minimum_pitch(s)
    # check octaves difference from lowest pitch
    d = int( m21.interval.Interval(m, m21.pitch.Pitch(lowest_pitch)).semitones/12 )
    # transpose by so many octaves
    i = m21.interval.Interval( 12*d )
    s_fix = s.transpose(i)
    return s_fix
# end fix_lowest_octave