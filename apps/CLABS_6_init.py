#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: USRP DSP Operation, Program #CLABS-6A
# Author: Nick Foster
# Generated: Fri May  1 09:21:16 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
from os.path import expanduser
import gmrr_rn13
import sip
import sys
import threading
import time

from distutils.version import StrictVersion
class CLABS_6_init(gr.top_block, Qt.QWidget):

    def __init__(self, initial_select=0, initial_baseband_gain=1, rxfreq=75.e6, initial_rxgain=20, txfreq=75.e6, initial_txgain=10, sig_samp_rate=100e3, filename=expanduser("~") + "/rn13_files/" + "DLWF.txt", samp_rate=500e3):
        gr.top_block.__init__(self, "USRP DSP Operation, Program #CLABS-6A")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("USRP DSP Operation, Program #CLABS-6A")
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

        self.settings = Qt.QSettings("GNU Radio", "CLABS_6_init")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.initial_select = initial_select
        self.initial_baseband_gain = initial_baseband_gain
        self.rxfreq = rxfreq
        self.initial_rxgain = initial_rxgain
        self.txfreq = txfreq
        self.initial_txgain = initial_txgain
        self.sig_samp_rate = sig_samp_rate
        self.filename = filename
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.selector_chooser = selector_chooser = initial_select
        self.initial_predistorter = initial_predistorter = expanduser("~") + "/rn13_files/" + "Predistort.txt"
        self.vpredistorter_title = vpredistorter_title = "Wat"
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ""
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.txgain = txgain = initial_txgain
        self.txfreq_slider = txfreq_slider = txfreq
        self.tone_freq = tone_freq = 0
        self.squelch = squelch = -60
        self.select = select = selector_chooser
        self.rxgain = rxgain = initial_rxgain
        self.rxfreq_slider = rxfreq_slider = rxfreq
        self.predriver_delay = predriver_delay = 0
        self.predistorter = predistorter = initial_predistorter
        self.off_switch = off_switch = 1
        self.mod_wave_chooser = mod_wave_chooser = 0
        self.mod_type_chooser = mod_type_chooser = 0
        self.mod_level = mod_level = 1
        self.mod_freq = mod_freq = 0
        self.mod_bw_slider = mod_bw_slider = 1e6
        self.final_delay = final_delay = 0
        self.envelope_gain = envelope_gain = 1
        self.drive_delay = drive_delay = 0
        self.digital_input_gain = digital_input_gain = 1
        self.carrier_level = carrier_level = 1
        self.baseband_gain = baseband_gain = initial_baseband_gain

        ##################################################
        # Blocks
        ##################################################
        self.tab_grid_widget = Qt.QTabWidget()
        self.tab_grid_widget_widget_0 = Qt.QWidget()
        self.tab_grid_widget_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_grid_widget_widget_0)
        self.tab_grid_widget_grid_layout_0 = Qt.QGridLayout()
        self.tab_grid_widget_layout_0.addLayout(self.tab_grid_widget_grid_layout_0)
        self.tab_grid_widget.addTab(self.tab_grid_widget_widget_0, "RF controls")
        self.tab_grid_widget_widget_1 = Qt.QWidget()
        self.tab_grid_widget_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_grid_widget_widget_1)
        self.tab_grid_widget_grid_layout_1 = Qt.QGridLayout()
        self.tab_grid_widget_layout_1.addLayout(self.tab_grid_widget_grid_layout_1)
        self.tab_grid_widget.addTab(self.tab_grid_widget_widget_1, "Test modulator controls")
        self.tab_grid_widget_widget_2 = Qt.QWidget()
        self.tab_grid_widget_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_grid_widget_widget_2)
        self.tab_grid_widget_grid_layout_2 = Qt.QGridLayout()
        self.tab_grid_widget_layout_2.addLayout(self.tab_grid_widget_grid_layout_2)
        self.tab_grid_widget.addTab(self.tab_grid_widget_widget_2, "Envelope/phase detection")
        self.tab_grid_widget_widget_3 = Qt.QWidget()
        self.tab_grid_widget_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_grid_widget_widget_3)
        self.tab_grid_widget_grid_layout_3 = Qt.QGridLayout()
        self.tab_grid_widget_layout_3.addLayout(self.tab_grid_widget_grid_layout_3)
        self.tab_grid_widget.addTab(self.tab_grid_widget_widget_3, "Predistortion")
        self.tab_grid_widget_widget_4 = Qt.QWidget()
        self.tab_grid_widget_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_grid_widget_widget_4)
        self.tab_grid_widget_grid_layout_4 = Qt.QGridLayout()
        self.tab_grid_widget_layout_4.addLayout(self.tab_grid_widget_grid_layout_4)
        self.tab_grid_widget.addTab(self.tab_grid_widget_widget_4, "Delays")
        self.top_grid_layout.addWidget(self.tab_grid_widget, 3,0)
        self._predistorter_tool_bar = Qt.QToolBar(self)
        self._predistorter_tool_bar.addWidget(Qt.QLabel("Predistorter filename"+": "))
        self._predistorter_line_edit = Qt.QLineEdit(str(self.predistorter))
        self._predistorter_tool_bar.addWidget(self._predistorter_line_edit)
        self._predistorter_line_edit.returnPressed.connect(
        	lambda: self.set_predistorter(str(str(self._predistorter_line_edit.text().toAscii()))))
        self.tab_grid_widget_grid_layout_3.addWidget(self._predistorter_tool_bar,  0,0)
        self._txgain_range = Range(0, 45, 1, initial_txgain, 200)
        self._txgain_win = RangeWidget(self._txgain_range, self.set_txgain, "Predriver out gain (dB)", "counter_slider")
        self.tab_grid_widget_grid_layout_0.addWidget(self._txgain_win,  3,0)
        self._txfreq_slider_tool_bar = Qt.QToolBar(self)
        self._txfreq_slider_tool_bar.addWidget(Qt.QLabel("Predriver output freq"+": "))
        self._txfreq_slider_line_edit = Qt.QLineEdit(str(self.txfreq_slider))
        self._txfreq_slider_tool_bar.addWidget(self._txfreq_slider_line_edit)
        self._txfreq_slider_line_edit.returnPressed.connect(
        	lambda: self.set_txfreq_slider(eng_notation.str_to_num(str(self._txfreq_slider_line_edit.text().toAscii()))))
        self.tab_grid_widget_grid_layout_0.addWidget(self._txfreq_slider_tool_bar,  1,0)
        self._tone_freq_range = Range(-samp_rate/2, samp_rate/2, 100, 0, 200)
        self._tone_freq_win = RangeWidget(self._tone_freq_range, self.set_tone_freq, "Offset frequency", "counter_slider")
        self.tab_grid_widget_grid_layout_1.addWidget(self._tone_freq_win,  4,0)
        self._squelch_range = Range(-90, 0, 1, -60, 200)
        self._squelch_win = RangeWidget(self._squelch_range, self.set_squelch, "Squelch value (dBfs)", "counter_slider")
        self.tab_grid_widget_grid_layout_2.addWidget(self._squelch_win,  1,0)
        self._rxgain_range = Range(0, 45, 1, initial_rxgain, 100)
        self._rxgain_win = RangeWidget(self._rxgain_range, self.set_rxgain, "RF in gain (dB)", "counter_slider")
        self.tab_grid_widget_grid_layout_0.addWidget(self._rxgain_win,  2,0)
        self._rxfreq_slider_tool_bar = Qt.QToolBar(self)
        self._rxfreq_slider_tool_bar.addWidget(Qt.QLabel("RF input freq"+": "))
        self._rxfreq_slider_line_edit = Qt.QLineEdit(str(self.rxfreq_slider))
        self._rxfreq_slider_tool_bar.addWidget(self._rxfreq_slider_line_edit)
        self._rxfreq_slider_line_edit.returnPressed.connect(
        	lambda: self.set_rxfreq_slider(eng_notation.str_to_num(str(self._rxfreq_slider_line_edit.text().toAscii()))))
        self.tab_grid_widget_grid_layout_0.addWidget(self._rxfreq_slider_tool_bar,  0,0)
        self._predriver_delay_range = Range(0, 100, 0.01, 0, 200)
        self._predriver_delay_win = RangeWidget(self._predriver_delay_range, self.set_predriver_delay, "Predriver delay", "counter_slider")
        self.tab_grid_widget_grid_layout_4.addWidget(self._predriver_delay_win,  1,0)
        self._off_switch_options = (0, 1, )
        self._off_switch_labels = ("On", "Off", )
        self._off_switch_tool_bar = Qt.QToolBar(self)
        self._off_switch_tool_bar.addWidget(Qt.QLabel("Output"+": "))
        self._off_switch_combo_box = Qt.QComboBox()
        self._off_switch_tool_bar.addWidget(self._off_switch_combo_box)
        for label in self._off_switch_labels: self._off_switch_combo_box.addItem(label)
        self._off_switch_callback = lambda i: Qt.QMetaObject.invokeMethod(self._off_switch_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._off_switch_options.index(i)))
        self._off_switch_callback(self.off_switch)
        self._off_switch_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_off_switch(self._off_switch_options[i]))
        self.top_grid_layout.addWidget(self._off_switch_tool_bar, 2,0)
        self._mod_wave_chooser_options = (0, 1, 2, 3, )
        self._mod_wave_chooser_labels = ("Constant", "Sine wave", "Triangle wave", "Square wave", )
        self._mod_wave_chooser_tool_bar = Qt.QToolBar(self)
        self._mod_wave_chooser_tool_bar.addWidget(Qt.QLabel("Modulation waveform"+": "))
        self._mod_wave_chooser_combo_box = Qt.QComboBox()
        self._mod_wave_chooser_tool_bar.addWidget(self._mod_wave_chooser_combo_box)
        for label in self._mod_wave_chooser_labels: self._mod_wave_chooser_combo_box.addItem(label)
        self._mod_wave_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mod_wave_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._mod_wave_chooser_options.index(i)))
        self._mod_wave_chooser_callback(self.mod_wave_chooser)
        self._mod_wave_chooser_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_mod_wave_chooser(self._mod_wave_chooser_options[i]))
        self.tab_grid_widget_grid_layout_1.addWidget(self._mod_wave_chooser_tool_bar,  2,0)
        self._mod_type_chooser_options = (0, 1, 2, 3, )
        self._mod_type_chooser_labels = ("CW", "Phase mod", "Amplitude mod", "Downloadable waveform", )
        self._mod_type_chooser_tool_bar = Qt.QToolBar(self)
        self._mod_type_chooser_tool_bar.addWidget(Qt.QLabel("Modulation type"+": "))
        self._mod_type_chooser_combo_box = Qt.QComboBox()
        self._mod_type_chooser_tool_bar.addWidget(self._mod_type_chooser_combo_box)
        for label in self._mod_type_chooser_labels: self._mod_type_chooser_combo_box.addItem(label)
        self._mod_type_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mod_type_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._mod_type_chooser_options.index(i)))
        self._mod_type_chooser_callback(self.mod_type_chooser)
        self._mod_type_chooser_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_mod_type_chooser(self._mod_type_chooser_options[i]))
        self.tab_grid_widget_grid_layout_1.addWidget(self._mod_type_chooser_tool_bar,  1,0)
        self._mod_level_range = Range(0, 1, 0.01, 1, 200)
        self._mod_level_win = RangeWidget(self._mod_level_range, self.set_mod_level, "Modulation level", "counter_slider")
        self.tab_grid_widget_grid_layout_1.addWidget(self._mod_level_win,  6,0)
        self._mod_freq_range = Range(-50000, 50000, 100, 0, 200)
        self._mod_freq_win = RangeWidget(self._mod_freq_range, self.set_mod_freq, "Modulation frequency", "counter_slider")
        self.tab_grid_widget_grid_layout_1.addWidget(self._mod_freq_win,  3,0)
        self._mod_bw_slider_range = Range(1000, samp_rate*50, 100, 1e6, 200)
        self._mod_bw_slider_win = RangeWidget(self._mod_bw_slider_range, self.set_mod_bw_slider, "Downloadable modulation sample rate", "counter_slider")
        self.tab_grid_widget_grid_layout_1.addWidget(self._mod_bw_slider_win,  8,0)
        self.gmrr_rn13_predistorter_0 = gmrr_rn13.predistorter(predistorter)
        self._final_delay_range = Range(0, 100, 0.01, 0, 200)
        self._final_delay_win = RangeWidget(self._final_delay_range, self.set_final_delay, "Final delay", "counter_slider")
        self.tab_grid_widget_grid_layout_4.addWidget(self._final_delay_win,  2,0)
        self._envelope_gain_range = Range(0, 20, 0.1, 1, 200)
        self._envelope_gain_win = RangeWidget(self._envelope_gain_range, self.set_envelope_gain, "Final gain (linear)", "counter_slider")
        self.tab_grid_widget_grid_layout_0.addWidget(self._envelope_gain_win,  4,0)
        self._drive_delay_range = Range(0, 100, 0.01, 0, 200)
        self._drive_delay_win = RangeWidget(self._drive_delay_range, self.set_drive_delay, "Drive delay", "counter_slider")
        self.tab_grid_widget_grid_layout_4.addWidget(self._drive_delay_win,  3,0)
        self._carrier_level_range = Range(0, 1, 0.01, 1, 200)
        self._carrier_level_win = RangeWidget(self._carrier_level_range, self.set_carrier_level, "Carrier level", "counter_slider")
        self.tab_grid_widget_grid_layout_1.addWidget(self._carrier_level_win,  7,0)
        self._baseband_gain_range = Range(0, 10, 0.01, initial_baseband_gain, 200)
        self._baseband_gain_win = RangeWidget(self._baseband_gain_range, self.set_baseband_gain, "Driver gain (linear)", "counter_slider")
        self.tab_grid_widget_grid_layout_0.addWidget(self._baseband_gain_win,  5,0)
        self._vpredistorter_title_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._vpredistorter_title_formatter = None
        else:
          self._vpredistorter_title_formatter = lambda x: x
        
        self._vpredistorter_title_tool_bar.addWidget(Qt.QLabel("Predistorter Title"+": "))
        self._vpredistorter_title_label = Qt.QLabel(str(self._vpredistorter_title_formatter(self.vpredistorter_title)))
        self._vpredistorter_title_tool_bar.addWidget(self._vpredistorter_title_label)
        self.tab_grid_widget_grid_layout_3.addWidget(self._vpredistorter_title_tool_bar,  1,0)
          
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("<b>USRP DSP Operation, Program #CLABS-6A</b><br><b>RF input spectrum</b>"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 0,0)
          
        def _variable_function_probe_0_probe():
            while True:
                val = self._vpredistorter_title_label.setText(str(self.gmrr_rn13_predistorter_0.get_title()))
                try:
                    self.set_variable_function_probe_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()
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
        self.uhd_usrp_source_0.set_gain(rxgain, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_sink_0_0.set_subdev_spec("A:0 B:AB", 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(txfreq_slider, 0)
        self.uhd_usrp_sink_0_0.set_gain(txgain, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_center_freq(0, 1)
        self.uhd_usrp_sink_0_0.set_gain(0, 1)
        self.uhd_usrp_sink_0_0.set_antenna("TXA", 1)
        self.test_src = gmrr_rn13.gmrr_test_src(samp_rate, min(2,mod_type_chooser), mod_wave_chooser, tone_freq, mod_freq, mod_level, carrier_level)
        self._selector_chooser_options = (0, 1, )
        self._selector_chooser_labels = ("External", "Internal", )
        self._selector_chooser_tool_bar = Qt.QToolBar(self)
        self._selector_chooser_tool_bar.addWidget(Qt.QLabel("Input source"+": "))
        self._selector_chooser_combo_box = Qt.QComboBox()
        self._selector_chooser_tool_bar.addWidget(self._selector_chooser_combo_box)
        for label in self._selector_chooser_labels: self._selector_chooser_combo_box.addItem(label)
        self._selector_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._selector_chooser_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._selector_chooser_options.index(i)))
        self._selector_chooser_callback(self.selector_chooser)
        self._selector_chooser_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_selector_chooser(self._selector_chooser_options[i]))
        self.tab_grid_widget_grid_layout_1.addWidget(self._selector_chooser_tool_bar,  0,0)
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
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1,0)
        self.gmrr_rn13_gmrr_waveform_src_0 = gmrr_rn13.gmrr_waveform_src(filename)
        self.fractional_resampler_xx_0 = filter.fractional_resampler_cc(0, float(mod_bw_slider)/samp_rate)
        self.fir_filter_xxx_0_2 = filter.fir_filter_fff(1, ([0]*int(final_delay) +[1-(final_delay%1)]  + [final_delay%1]+ [0]*int(100-final_delay)))
        self.fir_filter_xxx_0_2.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccf(1, ([0]*int(predriver_delay) + [1-(predriver_delay%1)]  + [predriver_delay%1]+[0]*int(100-predriver_delay)))
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(1, ([0]*int(drive_delay) + [1-(drive_delay%1)]  +[drive_delay%1]+ [0]*int(100-drive_delay)))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self._digital_input_gain_range = Range(0, 100, 0.01, 1, 200)
        self._digital_input_gain_win = RangeWidget(self._digital_input_gain_range, self.set_digital_input_gain, "Digital input gain (linear)", "counter_slider")
        self.tab_grid_widget_grid_layout_0.addWidget(self._digital_input_gain_win,  7,0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((baseband_gain, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((envelope_gain, ))
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.blks2_selector_0_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=int(mod_type_chooser==3),
        	output_index=0,
        )
        self.blks2_selector_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=3,
        	num_outputs=1,
        	input_index=2 if off_switch==1 else select,
        	output_index=0,
        )
        self.analog_rail_ff_0 = analog.rail_ff(0, 1)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch, 1, 1, False)
        self.analog_phase_modulator_fc_0 = analog.phase_modulator_fc(1)
        self.analog_const_source_x_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_1, 0), (self.blks2_selector_0_0, 2))    
        self.connect((self.analog_phase_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.analog_rail_ff_0, 0), (self.gmrr_rn13_predistorter_0, 2))    
        self.connect((self.analog_rail_ff_0, 0), (self.gmrr_rn13_predistorter_0, 1))    
        self.connect((self.analog_rail_ff_0, 0), (self.gmrr_rn13_predistorter_0, 0))    
        self.connect((self.analog_rail_ff_0, 0), (self.gmrr_rn13_predistorter_0, 3))    
        self.connect((self.blks2_selector_0_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.blks2_selector_0_0_0, 0), (self.blks2_selector_0_0, 1))    
        self.connect((self.blocks_complex_to_arg_0, 0), (self.analog_phase_modulator_fc_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_rail_ff_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 1))    
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.fir_filter_xxx_0_0_0, 0))    
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.uhd_usrp_sink_0_0, 0))    
        self.connect((self.fir_filter_xxx_0_2, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.fractional_resampler_xx_0, 0), (self.blks2_selector_0_0_0, 1))    
        self.connect((self.gmrr_rn13_gmrr_waveform_src_0, 0), (self.fractional_resampler_xx_0, 0))    
        self.connect((self.gmrr_rn13_predistorter_0, 0), (self.blocks_float_to_complex_1, 0))    
        self.connect((self.gmrr_rn13_predistorter_0, 1), (self.blocks_float_to_complex_1, 1))    
        self.connect((self.gmrr_rn13_predistorter_0, 2), (self.fir_filter_xxx_0_0, 0))    
        self.connect((self.gmrr_rn13_predistorter_0, 3), (self.fir_filter_xxx_0_2, 0))    
        self.connect((self.test_src, 0), (self.blks2_selector_0_0_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_selector_0_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_null_sink_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "CLABS_6_init")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_initial_select(self):
        return self.initial_select

    def set_initial_select(self, initial_select):
        self.initial_select = initial_select
        self.set_selector_chooser(self.initial_select)

    def get_initial_baseband_gain(self):
        return self.initial_baseband_gain

    def set_initial_baseband_gain(self, initial_baseband_gain):
        self.initial_baseband_gain = initial_baseband_gain
        self.set_baseband_gain(self.initial_baseband_gain)

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq
        self.set_rxfreq_slider(self.rxfreq)

    def get_initial_rxgain(self):
        return self.initial_rxgain

    def set_initial_rxgain(self, initial_rxgain):
        self.initial_rxgain = initial_rxgain
        self.set_rxgain(self.initial_rxgain)

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.set_txfreq_slider(self.txfreq)

    def get_initial_txgain(self):
        return self.initial_txgain

    def set_initial_txgain(self, initial_txgain):
        self.initial_txgain = initial_txgain
        self.set_txgain(self.initial_txgain)

    def get_sig_samp_rate(self):
        return self.sig_samp_rate

    def set_sig_samp_rate(self, sig_samp_rate):
        self.sig_samp_rate = sig_samp_rate

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.test_src.set_samp_rate(self.samp_rate)
        self.fractional_resampler_xx_0.set_resamp_ratio(float(self.mod_bw_slider)/self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxfreq_slider, self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_selector_chooser(self):
        return self.selector_chooser

    def set_selector_chooser(self, selector_chooser):
        self.selector_chooser = selector_chooser
        self.set_select(self.selector_chooser)
        self._selector_chooser_callback(self.selector_chooser)

    def get_initial_predistorter(self):
        return self.initial_predistorter

    def set_initial_predistorter(self, initial_predistorter):
        self.initial_predistorter = initial_predistorter
        self.set_predistorter(self.initial_predistorter)

    def get_vpredistorter_title(self):
        return self.vpredistorter_title

    def set_vpredistorter_title(self, vpredistorter_title):
        self.vpredistorter_title = vpredistorter_title
        Qt.QMetaObject.invokeMethod(self._vpredistorter_title_label, "setText", Qt.Q_ARG("QString", str(self.vpredistorter_title)))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", repr(self.variable_qtgui_label_0)))

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.uhd_usrp_sink_0_0.set_gain(self.txgain, 0)

    def get_txfreq_slider(self):
        return self.txfreq_slider

    def set_txfreq_slider(self, txfreq_slider):
        self.txfreq_slider = txfreq_slider
        Qt.QMetaObject.invokeMethod(self._txfreq_slider_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.txfreq_slider)))
        self.uhd_usrp_sink_0_0.set_center_freq(self.txfreq_slider, 0)

    def get_tone_freq(self):
        return self.tone_freq

    def set_tone_freq(self, tone_freq):
        self.tone_freq = tone_freq
        self.test_src.set_freq(self.tone_freq)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch)

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        self.blks2_selector_0_0.set_input_index(int(2 if self.off_switch==1 else self.select))

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain
        self.uhd_usrp_source_0.set_gain(self.rxgain, 0)

    def get_rxfreq_slider(self):
        return self.rxfreq_slider

    def set_rxfreq_slider(self, rxfreq_slider):
        self.rxfreq_slider = rxfreq_slider
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rxfreq_slider, self.samp_rate)
        Qt.QMetaObject.invokeMethod(self._rxfreq_slider_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rxfreq_slider)))
        self.uhd_usrp_source_0.set_center_freq(self.rxfreq_slider, 0)

    def get_predriver_delay(self):
        return self.predriver_delay

    def set_predriver_delay(self, predriver_delay):
        self.predriver_delay = predriver_delay
        self.fir_filter_xxx_0_0_0.set_taps(([0]*int(self.predriver_delay) + [1-(self.predriver_delay%1)]  + [self.predriver_delay%1]+[0]*int(100-self.predriver_delay)))

    def get_predistorter(self):
        return self.predistorter

    def set_predistorter(self, predistorter):
        self.predistorter = predistorter
        Qt.QMetaObject.invokeMethod(self._predistorter_line_edit, "setText", Qt.Q_ARG("QString", str(self.predistorter)))
        self.gmrr_rn13_predistorter_0.load(self.predistorter)

    def get_off_switch(self):
        return self.off_switch

    def set_off_switch(self, off_switch):
        self.off_switch = off_switch
        self._off_switch_callback(self.off_switch)
        self.blks2_selector_0_0.set_input_index(int(2 if self.off_switch==1 else self.select))

    def get_mod_wave_chooser(self):
        return self.mod_wave_chooser

    def set_mod_wave_chooser(self, mod_wave_chooser):
        self.mod_wave_chooser = mod_wave_chooser
        self.test_src.set_mod(self.mod_wave_chooser)
        self._mod_wave_chooser_callback(self.mod_wave_chooser)

    def get_mod_type_chooser(self):
        return self.mod_type_chooser

    def set_mod_type_chooser(self, mod_type_chooser):
        self.mod_type_chooser = mod_type_chooser
        self.test_src.set_mode(min(2,self.mod_type_chooser))
        self.blks2_selector_0_0_0.set_input_index(int(int(self.mod_type_chooser==3)))
        self._mod_type_chooser_callback(self.mod_type_chooser)

    def get_mod_level(self):
        return self.mod_level

    def set_mod_level(self, mod_level):
        self.mod_level = mod_level
        self.test_src.set_mod_level(self.mod_level)

    def get_mod_freq(self):
        return self.mod_freq

    def set_mod_freq(self, mod_freq):
        self.mod_freq = mod_freq
        self.test_src.set_mod_freq(self.mod_freq)

    def get_mod_bw_slider(self):
        return self.mod_bw_slider

    def set_mod_bw_slider(self, mod_bw_slider):
        self.mod_bw_slider = mod_bw_slider
        self.fractional_resampler_xx_0.set_resamp_ratio(float(self.mod_bw_slider)/self.samp_rate)

    def get_final_delay(self):
        return self.final_delay

    def set_final_delay(self, final_delay):
        self.final_delay = final_delay
        self.fir_filter_xxx_0_2.set_taps(([0]*int(self.final_delay) +[1-(self.final_delay%1)]  + [self.final_delay%1]+ [0]*int(100-self.final_delay)))

    def get_envelope_gain(self):
        return self.envelope_gain

    def set_envelope_gain(self, envelope_gain):
        self.envelope_gain = envelope_gain
        self.blocks_multiply_const_vxx_0.set_k((self.envelope_gain, ))

    def get_drive_delay(self):
        return self.drive_delay

    def set_drive_delay(self, drive_delay):
        self.drive_delay = drive_delay
        self.fir_filter_xxx_0_0.set_taps(([0]*int(self.drive_delay) + [1-(self.drive_delay%1)]  +[self.drive_delay%1]+ [0]*int(100-self.drive_delay)))

    def get_digital_input_gain(self):
        return self.digital_input_gain

    def set_digital_input_gain(self, digital_input_gain):
        self.digital_input_gain = digital_input_gain

    def get_carrier_level(self):
        return self.carrier_level

    def set_carrier_level(self, carrier_level):
        self.carrier_level = carrier_level
        self.test_src.set_carrier_level(self.carrier_level)

    def get_baseband_gain(self):
        return self.baseband_gain

    def set_baseband_gain(self, baseband_gain):
        self.baseband_gain = baseband_gain
        self.blocks_multiply_const_vxx_1.set_k((self.baseband_gain, ))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--initial-select", dest="initial_select", type="intx", default=0,
        help="Set Initial selection [default=%default]")
    parser.add_option("", "--initial-baseband-gain", dest="initial_baseband_gain", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set initial_baseband_gain [default=%default]")
    parser.add_option("", "--rxfreq", dest="rxfreq", type="eng_float", default=eng_notation.num_to_str(75.e6),
        help="Set rxfreq [default=%default]")
    parser.add_option("", "--initial-rxgain", dest="initial_rxgain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set initial_rxgain [default=%default]")
    parser.add_option("", "--txfreq", dest="txfreq", type="eng_float", default=eng_notation.num_to_str(75.e6),
        help="Set txfreq [default=%default]")
    parser.add_option("", "--initial-txgain", dest="initial_txgain", type="eng_float", default=eng_notation.num_to_str(10),
        help="Set initial_txgain [default=%default]")
    parser.add_option("", "--sig-samp-rate", dest="sig_samp_rate", type="eng_float", default=eng_notation.num_to_str(100e3),
        help="Set sig_samp_rate [default=%default]")
    parser.add_option("", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(500e3),
        help="Set samp_rate [default=%default]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CLABS_6_init(initial_select=options.initial_select, initial_baseband_gain=options.initial_baseband_gain, rxfreq=options.rxfreq, initial_rxgain=options.initial_rxgain, txfreq=options.txfreq, initial_txgain=options.initial_txgain, sig_samp_rate=options.sig_samp_rate, samp_rate=options.samp_rate)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
