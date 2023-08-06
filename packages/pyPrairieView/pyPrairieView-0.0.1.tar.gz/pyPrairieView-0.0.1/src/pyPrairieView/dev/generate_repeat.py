#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 16:08:39 2022

@author: doug
"""

def generate_repeat(waveform, repeat_number=None, interstimulus_interval=None):
    if repeat_number is None:
        return protocol
    else:
        for repeat_amount in repeat_number:
            waveform[repeat_amount] = 