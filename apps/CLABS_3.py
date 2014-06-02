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
                        if v[0:2] == 'IF': #set RF input freq
                            f = float(v[3:].strip())*1e6
                            print "Setting input frequency to %f" % f
                            self._tb.set_rxfreq(f)

                        elif v[0:2] == 'OF': #set predriver output freq
                            f = float(v[3:].strip())*1e6
                            print "Setting predriver frequency to %f" % f
                            self._tb.set_txfreq(f)

                        elif v[0:2] == 'TW': #select internal test waveform:
                            tw = int(v[3:].strip()) #0 for off, 1 for 10-tone, 2 for config. generator
                            if tw==0:
                                print "Selecting RF input"
                            elif tw==1:
                                print "Selecting IQ file source"
                            elif tw==2:
                                print "Selecting configurable waveform source"
                            self._tb.set_select(tw)
                            self._tb.set_selector_chooser(tw)

                        elif v[0:2] == 'BW': #set IQ waveform bandwidth
                            bw = float(v[3:].strip())
                            print "Setting test waveform bandwidth to %f" % bw
                            self._tb.set_mod_bw_slider(bw)
                            Qt.QMetaObject.invokeMethod(self._tb._mod_bw_slider_slider, "setValue", Qt.Q_ARG("double", bw))

                        elif v[0:2] == 'TF': #set waveform generator frequency
                            tf = float(v[3:].strip())
                            print "Setting test waveform freq to %f" % tf
                            self._tb.set_tone_freq(tf)
#                            Qt.QMetaObject.invokeMethod(self._tb._mod_freq_slider, "setValue", Qt.Q_ARG("double", bw))

                        elif v[0:2] == 'TA': #set waveform generator amplitude
                            ta = float(v[3:].strip())
                            print "Setting test waveform ampl to %f" % ta
                            self._tb.test_src.set_ampl(ta)

                        elif v[0:2] == 'MI':
                            mi = float(v[3:].strip())
                            print "Setting test waveform mod index to %f" % mi
                            self._tb.set_mod_index(mi)
                            Qt.QMetaObject.invokeMethod(self._tb._mod_index_slider, "setValue", Qt.Q_ARG("double", mi))

                        elif v[0:2] == 'MF':
                            mf = float(v[3:].strip())
                            print "Setting test waveform mod freq to %f" % mf
                            self._tb.set_mod_freq(mf)
                            Qt.QMetaObject.invokeMethod(self._tb._mod_freq_slider, "setValue", Qt.Q_ARG("double", mf))

                        elif v[0:2] == 'MT':
                            mt = min(2, int(v[3:].strip()))
                            print "Setting modulation type to %s" % (("CW", "Phase mod", "Amplitude mod")[mt])
                            self._tb.set_mod_type_chooser(mt)

                        elif v[0:2] == 'MW':
                            mw = min(2, int(v[3:].strip()))
                            print "Setting modulation waveform to %s" % (("Constant", "Cosine", "Triangle", "Square")[mw])
                            self._tb.set_mod_wave_chooser(mw)

                        elif v[0:2] == 'BG': #set baseband gain
                            bg = float(v[3:].strip())
                            print "Setting baseband gain to %f" % bg
                            self._tb.set_baseband_gain(bg)
                            Qt.QMetaObject.invokeMethod(self._tb._baseband_gain_slider_slider, "setValue", Qt.Q_ARG("double", bg))

                        elif v[0:2] == 'FG': #set final gain
                            fg = float(v[3:].strip())
                            print "Setting final gain to %f" % fg
                            self._tb.set_envelope_gain(fg)
                            Qt.QMetaObject.invokeMethod(self._tb._envelope_gain_slider, "setValue", Qt.Q_ARG("double", fg))

                        elif v[0:2] == 'RG': #set RF gain
                            rg = float(v[3:].strip())
                            print "Setting RF input gain to %f" % rg
                            self._tb.set_rxgain(rg)
                            Qt.QMetaObject.invokeMethod(self._tb._rxgain_slider_slider, "setValue", Qt.Q_ARG("double", rg))

                        elif v[0:2] == 'PG': #set predriver gain
                            pg = float(v[3:].strip())
                            print "Setting predriver output gain to %f" % pg
                            self._tb.set_txgain(rg)
                            Qt.QMetaObject.invokeMethod(self._tb._txgain_slider_slider, "setValue", Qt.Q_ARG("double", pg))

                        msgqs[k] = ""

        for s in ins:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        self._sock.shutdown(socket.SHUT_RDWR)
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
    parser.add_option("", "--baseband-gain", dest="baseband_gain", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set baseband_gain [default=%default]")
    parser.add_option("", "--port", type="intx", default=52001, help="Set TCP port to listen on [default=%default]")
    parser.add_option("", "--filename", type="string", default="/home/nick/Desktop/DL10.txt", help="Set test waveform file source")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CLABS_3_init(txgain=options.txgain, rxfreq=options.rxfreq, samp_rate=options.samp_rate, rxgain=options.rxgain, txfreq=options.txfreq, baseband_gain=options.baseband_gain)
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