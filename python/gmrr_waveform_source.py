#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class gmrr_waveform_source(gr.sync_block):
    """
    docstring for block gmrr_waveform_source
    """
    def __init__(self, filename):
        gr.sync_block.__init__(self,
            name="gmrr_waveform_source",
            in_sig=None,
            out_sig=[numpy.complex64])
        f = open(filename, 'r')
        f.readline()
        f.readline()
        self._waveform = []
        for line in f:
            [i, q, samp] = line.split()
            i = float(i.strip(',\t '))
            q = float(q.strip(',\t '))
            samp = int(samp.strip(',\t '))
            self._waveform.append(numpy.complex64(i+1j*q))
        self._offset = 0
        print "Samples: %i" % len(self._waveform)

    def work(self, input_items, output_items):
        out = output_items[0]
        oidx=0
        while oidx < len(out):
            out[oidx] = self._waveform[self._offset]
            self._offset = (self._offset+1) % len(self._waveform)
            oidx += 1
        return len(out)

