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
    def __init__(self, samp_rate, mode, mod_type, carrier_freq, mod_freq, mod_level, carrier_level):
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

        self._samp_rate = samp_rate
        self._mode = ['CW', 'PM', 'AM'][mode]
        self._mod_type = [analog.GR_CONST_WAVE, analog.GR_COS_WAVE, analog.GR_TRI_WAVE, analog.GR_SQR_WAVE][mod_type]
        self._freq = carrier_freq
        self._mod_freq = mod_freq
        self._carrier_ampl = carrier_level
        self._mod_ampl = mod_level

        self.update()

    def update(self):
        #figure out all required settings here
        #we do this in a single monolithic function because
        #several settings depend on other settings, and that
        #means we have to keep state.
        if self._mode == 'CW':
            self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
            self._sig_src_1.set_frequency(self._freq)
            self._sig_src_1.set_amplitude(1)
            self._sig_src_1.set_offset(0)
            self._sig_src_2.set_frequency(self._mod_freq)
            self._sig_src_2.set_waveform(analog.GR_COS_WAVE)
            self._sig_src_2.set_amplitude(self._mod_ampl)
            self._sig_src_2.set_offset(self._carrier_ampl)
            self._mod_selector.set_input_index(0)

        elif self._mode == 'PM':
            self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
            self._sig_src_1.set_frequency(self._freq)
            self._sig_src_1.set_amplitude(1)
            self._sig_src_1.set_offset(self._carrier_ampl)
            self._sig_src_2.set_waveform(self._mod_type)
            self._sig_src_2.set_frequency(self._mod_freq)
            if self._mod_type in [analog.GR_TRI_WAVE, analog.GR_SQR_WAVE]:
                self._sig_src_2.set_amplitude(self._mod_ampl*2)
                self._sig_src_2.set_offset(-self._mod_ampl+self._carrier_ampl)
            else:
                self._sig_src_2.set_amplitude(self._mod_ampl)
                self._sig_src_2.set_offset(self._carrier_ampl)
            self._mod_selector.set_input_index(1)
            self._pm.set_sensitivity(self._mod_ampl)

        elif self._mode == 'AM':
            self._sig_src_1.set_waveform(analog.GR_COS_WAVE)
            self._sig_src_1.set_frequency(self._freq)
            self._sig_src_1.set_amplitude(1)
            self._sig_src_1.set_offset(0)
            self._sig_src_2.set_waveform(self._mod_type)
            self._sig_src_2.set_frequency(self._mod_freq)
            if self._mod_type in [analog.GR_TRI_WAVE, analog.GR_SQR_WAVE]:
                self._sig_src_2.set_amplitude(self._mod_ampl*2)
                self._sig_src_2.set_offset(-self._mod_ampl+self._carrier_ampl)
            else:
                self._sig_src_2.set_amplitude(self._mod_ampl)
                self._sig_src_2.set_offset(self._carrier_ampl)
            self._mod_selector.set_input_index(2)

        else:
            print "Invalid mode %s" % self._mode


    def set_freq(self, freq):
        self._freq = freq
        self.update()

    def set_mod_freq(self, freq):
        self._mod_freq = freq
        self.update()

    def set_mod_level(self, mod_level):
        self._mod_ampl = mod_level
        self.update()

    def set_carrier_level(self, carrier_level):
        self._carrier_ampl = carrier_level
        self.update()

    #0 for CW, 1 for PM, 2 for AM
    def set_mode(self, mode):
        self._mode = ['CW', 'PM', 'AM'][mode]
        self.update()

    #0 for constant, 1 for sine, 2 for triangle, 3 for square
    def set_mod(self, mod):
        self._mod_type = [analog.GR_CONST_WAVE, analog.GR_COS_WAVE, analog.GR_TRI_WAVE, analog.GR_SQR_WAVE][mod]
        self.update()

    def set_samp_rate(self, rate):
        self._sig_src_1.set_sampling_freq(rate)
        self._sig_src_2.set_sampling_freq(rate)
        self.update()




