#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP-I Demonstration, Program #JBC-3
# Author: Nick Foster
# Generated: Fri May 30 17:32:50 2014
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import gmrr_rn13
import sip
import sys
import time

class CLABS_3(gr.top_block, Qt.QWidget):

    def __init__(self, txgain=10, rxfreq=75.e6, samp_rate=500e3, rxgain=20, txfreq=75.e6, initial_select=1, baseband_gain=1):
        gr.top_block.__init__(self, "USRP-I Demonstration, Program #JBC-3")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("USRP-I Demonstration, Program #JBC-3")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "CLABS_3")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.txgain = txgain
        self.rxfreq = rxfreq
        self.samp_rate = samp_rate
        self.rxgain = rxgain
        self.txfreq = txfreq
        self.initial_select = initial_select
        self.baseband_gain = baseband_gain

        ##################################################
        # Variables
        ##################################################
        self.selector_chooser = selector_chooser = initial_select
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ""
        self.txgain_slider = txgain_slider = txgain
        self.txfreq_slider = txfreq_slider = txfreq
        self.select = select = selector_chooser
        self.rxgain_slider = rxgain_slider = rxgain
        self.rxfreq_slider = rxfreq_slider = rxfreq
        self.envelope_gain = envelope_gain = 3
        self.baseband_gain_slider = baseband_gain_slider = baseband_gain

        ##################################################
        # Blocks
        ##################################################
        self._txgain_slider_layout = Qt.QVBoxLayout()
        self._txgain_slider_tool_bar = Qt.QToolBar(self)
        self._txgain_slider_layout.addWidget(self._txgain_slider_tool_bar)
        self._txgain_slider_tool_bar.addWidget(Qt.QLabel("Predriver out gain (dB)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._txgain_slider_counter = qwt_counter_pyslot()
        self._txgain_slider_counter.setRange(0, 45, 1)
        self._txgain_slider_counter.setNumButtons(2)
        self._txgain_slider_counter.setValue(self.txgain_slider)
        self._txgain_slider_tool_bar.addWidget(self._txgain_slider_counter)
        self._txgain_slider_counter.valueChanged.connect(self.set_txgain_slider)
        self._txgain_slider_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._txgain_slider_slider.setRange(0, 45, 1)
        self._txgain_slider_slider.setValue(self.txgain_slider)
        self._txgain_slider_slider.setMinimumWidth(200)
        self._txgain_slider_slider.valueChanged.connect(self.set_txgain_slider)
        self._txgain_slider_layout.addWidget(self._txgain_slider_slider)
        self.top_grid_layout.addLayout(self._txgain_slider_layout, 1,0)
        self._txfreq_slider_tool_bar = Qt.QToolBar(self)
        self._txfreq_slider_tool_bar.addWidget(Qt.QLabel("Predriver output freq"+": "))
        self._txfreq_slider_line_edit = Qt.QLineEdit(str(self.txfreq_slider))
        self._txfreq_slider_tool_bar.addWidget(self._txfreq_slider_line_edit)
        self._txfreq_slider_line_edit.returnPressed.connect(
        	lambda: self.set_txfreq_slider(eng_notation.str_to_num(self._txfreq_slider_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._txfreq_slider_tool_bar, 9,0)
        self._rxgain_slider_layout = Qt.QVBoxLayout()
        self._rxgain_slider_tool_bar = Qt.QToolBar(self)
        self._rxgain_slider_layout.addWidget(self._rxgain_slider_tool_bar)
        self._rxgain_slider_tool_bar.addWidget(Qt.QLabel("RF in gain (dB)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._rxgain_slider_counter = qwt_counter_pyslot()
        self._rxgain_slider_counter.setRange(0, 45, 1)
        self._rxgain_slider_counter.setNumButtons(2)
        self._rxgain_slider_counter.setValue(self.rxgain_slider)
        self._rxgain_slider_tool_bar.addWidget(self._rxgain_slider_counter)
        self._rxgain_slider_counter.valueChanged.connect(self.set_rxgain_slider)
        self._rxgain_slider_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._rxgain_slider_slider.setRange(0, 45, 1)
        self._rxgain_slider_slider.setValue(self.rxgain_slider)
        self._rxgain_slider_slider.setMinimumWidth(100)
        self._rxgain_slider_slider.valueChanged.connect(self.set_rxgain_slider)
        self._rxgain_slider_layout.addWidget(self._rxgain_slider_slider)
        self.top_grid_layout.addLayout(self._rxgain_slider_layout, 0,0)
        self._rxfreq_slider_tool_bar = Qt.QToolBar(self)
        self._rxfreq_slider_tool_bar.addWidget(Qt.QLabel("RF input freq"+": "))
        self._rxfreq_slider_line_edit = Qt.QLineEdit(str(self.rxfreq_slider))
        self._rxfreq_slider_tool_bar.addWidget(self._rxfreq_slider_line_edit)
        self._rxfreq_slider_line_edit.returnPressed.connect(
        	lambda: self.set_rxfreq_slider(eng_notation.str_to_num(self._rxfreq_slider_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._rxfreq_slider_tool_bar, 8,0)
        self._envelope_gain_layout = Qt.QVBoxLayout()
        self._envelope_gain_tool_bar = Qt.QToolBar(self)
        self._envelope_gain_layout.addWidget(self._envelope_gain_tool_bar)
        self._envelope_gain_tool_bar.addWidget(Qt.QLabel("Final gain (linear)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._envelope_gain_counter = qwt_counter_pyslot()
        self._envelope_gain_counter.setRange(0, 20, 0.1)
        self._envelope_gain_counter.setNumButtons(2)
        self._envelope_gain_counter.setValue(self.envelope_gain)
        self._envelope_gain_tool_bar.addWidget(self._envelope_gain_counter)
        self._envelope_gain_counter.valueChanged.connect(self.set_envelope_gain)
        self._envelope_gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._envelope_gain_slider.setRange(0, 20, 0.1)
        self._envelope_gain_slider.setValue(self.envelope_gain)
        self._envelope_gain_slider.setMinimumWidth(200)
        self._envelope_gain_slider.valueChanged.connect(self.set_envelope_gain)
        self._envelope_gain_layout.addWidget(self._envelope_gain_slider)
        self.top_grid_layout.addLayout(self._envelope_gain_layout, 4,0)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("<b>RF input spectrum</b>"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self.variable_qtgui_label_0))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 6,0)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec("A:0", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(rxfreq_slider, 0)
        self.uhd_usrp_source_0.set_gain(rxgain_slider, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_sink_0_0.set_subdev_spec("A:0 B:A", 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(txfreq_slider, 0)
        self.uhd_usrp_sink_0_0.set_gain(txgain_slider, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_center_freq(0, 1)
        self.uhd_usrp_sink_0_0.set_gain(0, 1)
        self.uhd_usrp_sink_0_0.set_antenna("TXA", 1)
        self._selector_chooser_options = (0, 1, )
        self._selector_chooser_labels = ("10-tone Waveform", "RF Input", )
        self._selector_chooser_tool_bar = Qt.QToolBar(self)
        self._selector_chooser_tool_bar.addWidget(Qt.QLabel("Input source"+": "))
        self._selector_chooser_combo_box = Qt.QComboBox()
        self._selector_chooser_tool_bar.addWidget(self._selector_chooser_combo_box)
        for label in self._selector_chooser_labels: self._selector_chooser_combo_box.addItem(label)
        self._selector_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._selector_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._selector_chooser_options.index(i)))
        self._selector_chooser_callback(self.selector_chooser)
        self._selector_chooser_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_selector_chooser(self._selector_chooser_options[i]))
        self.top_layout.addWidget(self._selector_chooser_tool_bar)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rxfreq_slider, #fc
        	samp_rate, #bw
        	"RF input spectrum", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 7,0)
        self.gmrr_rn13_gmrr_waveform_source_0 = gmrr_rn13.gmrr_waveform_source("/home/nick/Desktop/DL10.TXT")
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vcc((select, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((not select, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((baseband_gain, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((envelope_gain, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self._baseband_gain_slider_layout = Qt.QVBoxLayout()
        self._baseband_gain_slider_tool_bar = Qt.QToolBar(self)
        self._baseband_gain_slider_layout.addWidget(self._baseband_gain_slider_tool_bar)
        self._baseband_gain_slider_tool_bar.addWidget(Qt.QLabel("Baseband gain (linear)"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._baseband_gain_slider_counter = qwt_counter_pyslot()
        self._baseband_gain_slider_counter.setRange(0, 10, 0.01)
        self._baseband_gain_slider_counter.setNumButtons(2)
        self._baseband_gain_slider_counter.setValue(self.baseband_gain_slider)
        self._baseband_gain_slider_tool_bar.addWidget(self._baseband_gain_slider_counter)
        self._baseband_gain_slider_counter.valueChanged.connect(self.set_baseband_gain_slider)
        self._baseband_gain_slider_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._baseband_gain_slider_slider.setRange(0, 10, 0.01)
        self._baseband_gain_slider_slider.setValue(self.baseband_gain_slider)
        self._baseband_gain_slider_slider.setMinimumWidth(200)
        self._baseband_gain_slider_slider.valueChanged.connect(self.set_baseband_gain_slider)
        self._baseband_gain_slider_layout.addWidget(self._baseband_gain_slider_slider)
        self.top_grid_layout.addLayout(self._baseband_gain_slider_layout, 5,0)
        self.analog_rail_ff_0 = analog.rail_ff(0, 1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.gmrr_rn13_gmrr_waveform_source_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_null_sink_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "CLABS_3")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.set_txgain_slider(self.txgain)

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq
        self.set_rxfreq_slider(self.rxfreq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxfreq_slider, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.set_rxgain_slider(self.rxgain)

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.set_txfreq_slider(self.txfreq)

    def get_initial_select(self):
        return self.initial_select

    def set_initial_select(self, initial_select):
        self.initial_select = initial_select
        self.set_selector_chooser(self.initial_select)

    def get_baseband_gain(self):
        return self.baseband_gain

    def set_baseband_gain(self, baseband_gain):
        self.baseband_gain = baseband_gain
        self.set_baseband_gain_slider(self.baseband_gain)
        self.blocks_multiply_const_vxx_0_0.set_k((self.baseband_gain, ))

    def get_selector_chooser(self):
        return self.selector_chooser

    def set_selector_chooser(self, selector_chooser):
        self.selector_chooser = selector_chooser
        self.set_select(self.selector_chooser)
        self._selector_chooser_callback(self.selector_chooser)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", repr(self.variable_qtgui_label_0)))

    def get_txgain_slider(self):
        return self.txgain_slider

    def set_txgain_slider(self, txgain_slider):
        self.txgain_slider = txgain_slider
        self.uhd_usrp_sink_0_0.set_gain(self.txgain_slider, 0)
        Qt.QMetaObject.invokeMethod(self._txgain_slider_counter, "setValue", Qt.Q_ARG("double", self.txgain_slider))
        Qt.QMetaObject.invokeMethod(self._txgain_slider_slider, "setValue", Qt.Q_ARG("double", self.txgain_slider))

    def get_txfreq_slider(self):
        return self.txfreq_slider

    def set_txfreq_slider(self, txfreq_slider):
        self.txfreq_slider = txfreq_slider
        self.uhd_usrp_sink_0_0.set_center_freq(self.txfreq_slider, 0)
        Qt.QMetaObject.invokeMethod(self._txfreq_slider_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.txfreq_slider)))

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        self.blocks_multiply_const_vxx_1.set_k((not self.select, ))
        self.blocks_multiply_const_vxx_1_0.set_k((self.select, ))

    def get_rxgain_slider(self):
        return self.rxgain_slider

    def set_rxgain_slider(self, rxgain_slider):
        self.rxgain_slider = rxgain_slider
        Qt.QMetaObject.invokeMethod(self._rxgain_slider_counter, "setValue", Qt.Q_ARG("double", self.rxgain_slider))
        Qt.QMetaObject.invokeMethod(self._rxgain_slider_slider, "setValue", Qt.Q_ARG("double", self.rxgain_slider))
        self.uhd_usrp_source_0.set_gain(self.rxgain_slider, 0)

    def get_rxfreq_slider(self):
        return self.rxfreq_slider

    def set_rxfreq_slider(self, rxfreq_slider):
        self.rxfreq_slider = rxfreq_slider
        Qt.QMetaObject.invokeMethod(self._rxfreq_slider_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rxfreq_slider)))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxfreq_slider, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.rxfreq_slider, 0)

    def get_envelope_gain(self):
        return self.envelope_gain

    def set_envelope_gain(self, envelope_gain):
        self.envelope_gain = envelope_gain
        self.blocks_multiply_const_vxx_0.set_k((self.envelope_gain, ))
        Qt.QMetaObject.invokeMethod(self._envelope_gain_counter, "setValue", Qt.Q_ARG("double", self.envelope_gain))
        Qt.QMetaObject.invokeMethod(self._envelope_gain_slider, "setValue", Qt.Q_ARG("double", self.envelope_gain))

    def get_baseband_gain_slider(self):
        return self.baseband_gain_slider

    def set_baseband_gain_slider(self, baseband_gain_slider):
        self.baseband_gain_slider = baseband_gain_slider
        Qt.QMetaObject.invokeMethod(self._baseband_gain_slider_counter, "setValue", Qt.Q_ARG("double", self.baseband_gain_slider))
        Qt.QMetaObject.invokeMethod(self._baseband_gain_slider_slider, "setValue", Qt.Q_ARG("double", self.baseband_gain_slider))

import socket
import threading
import select
import Queue
class clabs_tcp_ctrl(threading.Thread):
    def __init__(self, tb, port):
        threading.Thread.__init__(self)
        self._tb = tb
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('0.0.0.0', port))
        self._sock.listen(1)
        self._sock.setblocking(0)
        self.setDaemon(True)
        self._running=True

    def stop(self):
        self._running=False

    def wait(self):
        while(self._running):
            1

    def run(self):
        ins = [self._sock]
        outs = []
        msgqs = {}
        while self._running:
            readable, writeable, bad = select.select(ins, outs, ins)
            for s in readable:
                if s is self._sock:
                    conn, addr = s.accept()
                    print "New connection"
                    conn.setblocking(0)
                    ins.append(conn)
                    msgqs[conn] = ""
                else:
                    d = s.recv(1024)
                    if d:
                        print "New message from %s: %s" % (s.getpeername(), d)
                        msgqs[s] += d
                    else:
                        print "Connection closed"
                        ins.remove(s)
                        s.close()
                        del msgqs[s]
            #parse data
            for k, v in msgqs.iteritems():
                if len(v) > 0:
                    if v[-1] == "\n":
                        print "Message: %s" % v

                        #do something.
                        if(v[0:2] == 'IF'): #set RF input freq
                            f = float(v[3:].strip())*1e6
                            print "Setting input frequency to %f" % f
                            self._tb.set_rxfreq(f)

                        elif(v[0:2] == 'OF'): #set predriver output freq
                            f = float(v[3:].strip())*1e6
                            print "Setting predriver frequency to %f" % f
                            self._tb.set_txfreq(f)

                        elif(v[0:2] == 'TW'): #select internal test waveform (bool)
                            tw = int(v[3:].strip())
                            if(tw):
                                print "Selecting internal test waveform"
                            else:
                                print "Selecting RF input"
                            self._tb.set_select(not tw)
                            self._tb.set_selector_chooser(not tw)

                        elif(v[0:2] == 'BG'): #set baseband gain
                            bg = float(v[3:].strip())
                            print "Setting baseband gain to %f" % bg
                            self._tb.set_baseband_gain(bg)
                            Qt.QMetaObject.invokeMethod(self._tb._baseband_gain_slider_slider, "setValue", Qt.Q_ARG("double", bg))

                        elif(v[0:2] == 'FG'): #set final gain
                            fg = float(v[3:].strip())
                            print "Setting final gain to %f" % fg
                            self._tb.set_envelope_gain(fg)
                            Qt.QMetaObject.invokeMethod(self._tb._envelope_gain_slider, "setValue", Qt.Q_ARG("double", fg))

                        elif(v[0:2] == 'RG'): #set RF gain
                            rg = float(v[3:].strip())
                            print "Setting RF input gain to %f" % rg
                            self._tb.set_rxgain(rg)
                            Qt.QMetaObject.invokeMethod(self._tb._rxgain_slider_slider, "setValue", Qt.Q_ARG("double", rg))

                        elif(v[0:2] == 'PG'): #set predriver gain
                            pg = float(v[3:].strip())
                            print "Setting predriver output gain to %f" % pg
                            self._tb.set_txgain(rg)
                            Qt.QMetaObject.invokeMethod(self._tb._txgain_slider_slider, "setValue", Qt.Q_ARG("double", pg))

                        msgqs[k] = ""

        for s in ins:
            s.close()
        self._sock.close()


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--txgain", dest="txgain", type="eng_float", default=eng_notation.num_to_str(10),
        help="Set txgain [default=%default]")
    parser.add_option("", "--rxfreq", dest="rxfreq", type="eng_float", default=eng_notation.num_to_str(75.e6),
        help="Set rxfreq [default=%default]")
    parser.add_option("", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(500e3),
        help="Set samp_rate [default=%default]")
    parser.add_option("", "--rxgain", dest="rxgain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set rxgain [default=%default]")
    parser.add_option("", "--txfreq", dest="txfreq", type="eng_float", default=eng_notation.num_to_str(75.e6),
        help="Set txfreq [default=%default]")
    parser.add_option("", "--initial-select", dest="initial_select", type="intx", default=1,
        help="Set Initial selection [default=%default]")
    parser.add_option("", "--baseband-gain", dest="baseband_gain", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set baseband_gain [default=%default]")
    parser.add_option("", "--port", type="intx", default=52001, help="Set TCP port to listen on [default=%default]")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CLABS_3(txgain=options.txgain, rxfreq=options.rxfreq, samp_rate=options.samp_rate, rxgain=options.rxgain, txfreq=options.txfreq, initial_select=options.initial_select, baseband_gain=options.baseband_gain)
    tcp_server = clabs_tcp_ctrl(tb, options.port)
    tcp_server.start()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
        tcp_server.stop()
        tcp_server.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    time.sleep(1)
    tb = None #to clean up Qt widgets
