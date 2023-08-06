#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 12:06:01 2022

@author: doug
"""

def generate_epoch(epoch_type):
    # necessary inputs
        # type
        # first level (holding)
        # delta level
        # final level
        # first duration (ms)
        # delta duration (ms)
        # interstimulus interval (ms)
        # train rate (Hz)
        # pulse width (ms)
    
    match epoch_type:
        case "step":
            # specify baseline voltage 
            # 
        case "ramp":
            # ramp at specified level
        case "pulse train":
            
        case "biphasic train":
            
        case "triangle train":
            
        case "cosine train":