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
from CLABS_3_init import CLABS_3_init
import socket
import threading
import select
import Queue
import struct

class clabs_tcp_ctrl(threading.Thread):
    def __init__(self, tb, port):
        threading.Thread.__init__(self)
        self._tb = tb
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('0.0.0.0', port))
        self._sock.listen(1)
        self._sock.setblocking(0)
        NOLINGER = struct.pack('ii', 1, 0)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, NOLINGER)
        self.setDaemon(True)
        self._running=True

        self._cmdlist = {"IF": (self._set_input_freq, float), "OF": (self._set_output_freq, float),
                         "ON": (self._set_power, int), "IS": (self._set_input_source, int),
                         "BW": (self._set_test_bandwidth, float), "TF": (self._set_offset_freq, float),
                         "ML": (self._set_mod_level, float), "CL": (self._set_carrier_level, float),
                         "MF": (self._set_mod_freq, float), "MT": (self._set_mod_type, int),
                         "MW": (self._set_mod_waveform, int), "DG": (self._set_driver_gain, float),
                         "RG": (self._set_rf_gain, float), "FG": (self._set_final_gain, float),
                         "PG": (self._set_predriver_gain, float), "IG": (self._set_input_gain, float)}

    def parse(self, cmd, arg):
        if not (cmd in self._cmdlist):
            return 1
        try:
            if self._cmdlist[cmd][1] is float:
                unitarg = float(arg)
            elif self._cmdlist[cmd][1] is int:
                unitarg = int(arg)
            else:
                return 1
            retval = self._cmdlist[cmd][0](unitarg)
            return retval
        except:
            return 2

    def _set_input_freq(self, arg):
        print "Setting input freq to %fMHz" % arg
        self._tb.set_rxfreq(arg*1e6)
        return 0

    def _set_output_freq(self, arg):
        print "Setting output freq to %fMHz" % arg
        self._tb.set_txfreq(arg*1e6)
        return 0

    def _set_power(self, arg):
        if arg not in range(2):
            return 2
        print "Setting output %s" % (("ON", "OFF")[int(arg==0)])
        self._tb.set_off_switch(int(arg==0))
#        self._tb.set_off_switch_chooser(int(arg==0))
        return 0

    def _set_input_source(self, arg):
        if arg not in range(2):
            return 2
        print "Setting input source: %s" % (("EXTERNAL", "INTERNAL")[arg])
        self._tb.set_select(arg)
        self._tb.set_selector_chooser(arg)
        return 0

    def _set_test_bandwidth(self, arg):
        print "Setting downloadable waveform bandwidth to %fHz" % arg
        self._tb.set_mod_bw_slider(arg)
        Qt.QMetaObject.invokeMethod(self._tb._mod_bw_slider_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_offset_freq(self, arg):
        print "Setting test waveform freq offset to %fHz" % arg
        self._tb.set_tone_freq(arg)
        return 0

    def _set_mod_level(self, arg):
        print "Setting test waveform modulation level to %f" % arg
        self._tb.set_mod_level(arg)
        Qt.QMetaObject.invokeMethod(self._tb._mod_level_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_carrier_level(self, arg):
        print "Setting test waveform carrier level to %f" % arg
        self._tb.set_carrier_level(arg)
        Qt.QMetaObject.invokeMethod(self._tb._carrier_level_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_mod_freq(self, arg):
        print "Setting test waveform mod freq to %fHz" % arg
        self._tb.set_mod_freq(arg)
        Qt.QMetaObject.invokeMethod(self._tb._mod_freq_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_mod_type(self, arg):
        if arg not in range(4):
            return 2
        print "Setting modulation type to %s" % (("CW", "Phase mod", "Amplitude mod", "Downloadable tone")[arg])
        self._tb.set_mod_type_chooser(arg)
        return 0

    def _set_mod_waveform(self, arg):
        if arg not in range(4):
            return 2
        print "Setting modulation waveform to %s" % (("Constant", "Cosine", "Triangle", "Square")[arg])
        self._tb.set_mod_wave_chooser(arg)
        return 0

    def _set_driver_gain(self, arg):
        print "Setting driver gain to %f" % arg
        self._tb.set_baseband_gain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._baseband_gain_slider_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_rf_gain(self, arg):
        print "Setting RF input gain to %f" % arg
        self._tb.set_rxgain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._rxgain_slider_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_final_gain(self, arg):
        print "Setting final gain to %f" % arg
        self._tb.set_envelope_gain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._envelope_gain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_predriver_gain(self, arg):
        print "Setting predriver output gain to %f" % arg
        self._tb.set_txgain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._txgain_slider_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_input_gain(self, arg):
        print "Setting digital input gain to %f" % arg
        self._tb.set_digital_input_gain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._digital_input_gain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

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
                    outs.append(conn)
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
                        cmd = v[0:2]
                        arg = v[3:]

                        retstr = "%s " % v[0:2]
                        print "Message: %s" % v

                        retstr += str(self.parse(cmd, arg))

                        #now post replies to each listener
                        retstr += '\n'
                        for s in outs:
                            try:
                                s.send(retstr)
                            except:
                                pass

                        msgqs[k] = ""

        for s in ins:
            try:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except:
                pass
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()
        except:
            pass


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
    parser.add_option("", "--baseband-gain", dest="baseband_gain", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set baseband_gain [default=%default]")
    parser.add_option("", "--port", type="intx", default=52001, help="Set TCP port to listen on [default=%default]")
    parser.add_option("", "--filename", type="string", default="/home/nick/Desktop/DL10.txt", help="Set test waveform file source")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CLABS_3_init(initial_txgain=options.txgain, rxfreq=options.rxfreq, samp_rate=options.samp_rate, initial_rxgain=options.rxgain, txfreq=options.txfreq, initial_baseband_gain=options.baseband_gain)
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
