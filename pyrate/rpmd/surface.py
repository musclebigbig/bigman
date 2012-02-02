#!/usr/bin/env python
# encoding: utf-8

################################################################################
#
#   PyRate - Python tools for computing chemical reaction rates
#
#   Copyright (c) 2012 by Joshua W. Allen (jwallen@mit.edu)
#                         Yury V. Suleimanov (ysuleyma@mit.edu)
#                         William H. Green (whgreen@mit.edu)
#
#   Permission is hereby granted, free of charge, to any person obtaining a 
#   copy of this software and associated documentation files (the "Software"), 
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the 
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#   DEALINGS IN THE SOFTWARE. 
#
################################################################################

"""
This module contains a representation of a dividing surface
"""

import math
import numpy
from ._surface import *

################################################################################

class TransitionState:
    """
    A representation of a transition state geometry with supplemental
    information used to enumerate a dividing surface. The attributes are:
    
    ======================= ====================================================
    Attribute               Description
    ======================= ====================================================
    `geometry`              An array of the coordinates of each atom in each transition state in atomic units
    `formingBonds`          A list of indices for each bond that is forming in the reaction for each transition state
    `breakingBonds`         A list of indices for each bond that is forming in the reaction for each transition state
    ----------------------- ----------------------------------------------------
    `formingBondLengths`    A list of the bond lengths for each bond that is forming in each transition state
    `breakingBondLengths`   A list of the bond lengths for each bond that is breaking in each transition state
    ======================= ====================================================
    
    The `formingBondLengths` and `breakingBondLengths` arrays are automatically
    computed from the given transition state geometries.
    """

    def __init__(self, geometry, formingBonds, breakingBonds):
        
        self.geometry = geometry
        Nts = self.geometry.shape[2]
        
        self.formingBonds = numpy.array(formingBonds, numpy.int)
        self.breakingBonds = numpy.array(breakingBonds, numpy.int)
        self.formingBondLengths = numpy.empty((Nts, self.formingBonds.shape[0]))
        self.breakingBondLengths = numpy.empty((Nts, self.breakingBonds.shape[0]))
        
        for n in range(Nts):
            for m in range(self.formingBonds.shape[0]):
                atom1 = self.formingBonds[n,m,0] - 1
                atom2 = self.formingBonds[n,m,1] - 1
                Rx = self.geometry[0,atom1,n] - self.geometry[0,atom2,n]
                Ry = self.geometry[1,atom1,n] - self.geometry[1,atom2,n]
                Rz = self.geometry[2,atom1,n] - self.geometry[2,atom2,n]
                R = math.sqrt(Rx * Rx + Ry * Ry + Rz * Rz)
                self.formingBondLengths[n,m] = R
            
            for m in range(self.breakingBonds.shape[0]):
                atom1 = self.breakingBonds[n,m,0] - 1
                atom2 = self.breakingBonds[n,m,1] - 1
                Rx = self.geometry[0,atom1,n] - self.geometry[0,atom2,n]
                Ry = self.geometry[1,atom1,n] - self.geometry[1,atom2,n]
                Rz = self.geometry[2,atom1,n] - self.geometry[2,atom2,n]
                R = math.sqrt(Rx * Rx + Ry * Ry + Rz * Rz)
                self.breakingBondLengths[n,m] = R

    def value(self, position):
        """
        Return the value of the dividing surface function at the given
        `position`.
        """
        s1 = transition_state_value(position, 
                                    self.formingBonds, 
                                    self.formingBondLengths,
                                    self.breakingBonds,
                                    self.breakingBondLengths)
        return s1
    
    def gradient(self, position):
        """
        Return the gradient of the dividing surface function at the given
        `position`.
        """
        ds1 = transition_state_gradient(position, 
                                        self.formingBonds, 
                                        self.formingBondLengths,
                                        self.breakingBonds,
                                        self.breakingBondLengths)
        return ds1
    
    def hessian(self, position):
        """
        Return the Hessian of the dividing surface function at the given
        `position`.
        """
        d2s1 = transition_state_hessian(position, 
                                        self.formingBonds, 
                                        self.formingBondLengths,
                                        self.breakingBonds,
                                        self.breakingBondLengths)
        return d2s1
