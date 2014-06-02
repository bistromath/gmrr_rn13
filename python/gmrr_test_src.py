#!/usr/bin/env python

#GMRR test waveform source hier block
#supports the following waveforms

#CW (vary freq, ampl)
#Rectangular pulse (vary freq, ampl)
#2-tone modulated AM (vary modulation type, index, freq)
#Phase modulation (vary freq, index, modulation type)

import math
import numpy
from gnuradio import gr, blocks, analog, filter
from grc_gnuradio.blks2 import selector
import gmrr_rn13

class gmrr_test_src(gr.hier_block2):
    def __init__(self, samp_rate, mode, mod_type, carrier_freq, mod_freq, mod_index):
        gr.hier_block2.__init__(self,
            "gmrr_test_src",
            gr.io_signature(0, 0, 0),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self._sig_src_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self._sig_src_2 = analog.sig_source_c(samp_rate, analog.GR_CONST_WAVE, 0, 1, 0)
        self._c2r = blocks.complex_to_real()
        self._f2c = blocks.float_to_complex()
        self._pm = analog.phase_modulator_fc(0)
        self._mult = blocks.multiply_cc()
        self._mod_selector = selector(gr.sizeof_gr_complex, 3, 1, 0, 0)

        self.connect(self._sig_src_1, (self._mult,0))
        self.connect(self._sig_src_2, (self._mod_selector,0))
        self.connect(self._sig_src_2, self._c2r)
        self.connect(self._c2r, self._pm, (self._mod_selector,1))
        self.connect(self._c2r, self._f2c, (self._mod_selector,2))
        self.connect(self._mod_selector, (self._mult,1))

        self.connect(self._mult, self)
        self.set_mode(mode)
        self.set_mod(mod_type)
        self.set_freq(carrier_freq)
        self.set_mod_freq(mod_freq)
        self.set_mod_index(mod_index)

    def set_freq(self, freq):
        self._sig_src_1.set_frequency(freq)
    def set_ampl(self, ampl):
        self._sig_src_1.set_amplitude(ampl)
    def set_offset(self, offset):
        self._sig_src_1.set_offset(offset)

    def set_mod_freq(self, freq):
        self._sig_src_2.set_frequency(freq)
    def set_mod_ampl(self, ampl):
        self._sig_src_2.set_amplitude(ampl)
    def set_mod_offset(self, offset):
        self._sig_src_2.set_offset(offset)

    def set_cw_mode(self):
        self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
        self._sig_src_2.set_waveform(analog.GR_CONST_WAVE)
        self.set_mod_ampl(1)
        self._mod_selector.set_input_index(0)
    def set_pm_mode(self):
        self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
        self._mod_selector.set_input_index(1)
    def set_am_mode(self):
        self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
        self._mod_selector.set_input_index(2)

    #0 for CW, 1 for PM, 2 for AM
    def set_mode(self, mode):
        if mode==0:
            self.set_cw_mode()
        elif mode==1:
            self.set_pm_mode()
        elif mode==2:
            self.set_am_mode()

    #0 for constant, 1 for sine, 2 for triangle, 3 for square
    def set_mod(self, mod):
        if mod==0:
            self.set_const_mod()
        elif mod==1:
            self.set_cosine_mod()
        elif mod==2:
            self.set_triangle_mod()
        elif mod==3:
            self.set_square_mod()

    def set_mod_index(self, index):
        self._pm.set_sensitivity(index)
        self._sig_src_2.set_offset(1-index)
        self._sig_src_2.set_amplitude(index)

    def set_const_mod(self):
        self._sig_src_2.set_waveform(analog.GR_CONST_WAVE)
    def set_cosine_mod(self):
        self._sig_src_2.set_waveform(analog.GR_COS_WAVE)
    def set_triangle_mod(self):
        self._sig_src_2.set_waveform(analog.GR_TRI_WAVE)
    def set_square_mod(self):
        self._sig_src_2.set_waveform(analog.GR_SQR_WAVE)

    def set_samp_rate(self, rate):
        self._sig_src_1.set_sampling_freq(rate)
        self._sig_src_2.set_sampling_freq(rate)




