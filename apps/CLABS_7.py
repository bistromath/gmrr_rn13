#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: USRP-I Demonstration, Program #JBC-3
# Author: Nick Foster
# Generated: Fri May 30 17:32:50 2014
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot, QThread
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
from CLABS_7_init import CLABS_7_init
import socket
import threading
import select
import Queue
import struct
import cmath
import numpy
from os.path import expanduser
from time import strftime

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
                         "SR": (self._set_test_bandwidth, float), "TF": (self._set_offset_freq, float),
                         "ML": (self._set_mod_level, float), "CL": (self._set_carrier_level, float),
                         "MF": (self._set_mod_freq, float), "MT": (self._set_mod_type, int),
                         "MW": (self._set_mod_waveform, int), "DG": (self._set_driver_gain, float),
                         "RG": (self._set_rf_gain, float), "FG": (self._set_final_gain, float),
                         "PG": (self._set_predriver_gain, float), "IG": (self._set_input_gain, float),
                         "SQ": (self._set_squelch, float), "TO": (self._set_test_output, int),
                         "PD": (self._set_predistorter, str), "DP": (self._set_predriver_delay, float),
                         "DF": (self._set_final_delay, float), "DD": (self._set_drive_delay, float)}

    def parse(self, cmd, arg):
        if not (cmd in self._cmdlist):
            return 1
        try:
            if self._cmdlist[cmd][1] is float:
                unitarg = float(arg)
            elif self._cmdlist[cmd][1] is int:
                unitarg = int(arg)
            elif self._cmdlist[cmd][1] is str:
                unitarg = str(arg).strip()
            else:
                return 1
            retval = self._cmdlist[cmd][0](unitarg)
            return retval
        except Exception as e:
            print e
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
        print "Setting downloadable waveform sample rate to %fsps" % arg
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
        Qt.QMetaObject.invokeMethod(self._tb._baseband_gain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_rf_gain(self, arg):
        print "Setting RF input gain to %f" % arg
        self._tb.set_rxgain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._rxgain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_final_gain(self, arg):
        print "Setting final gain to %f" % arg
        self._tb.set_envelope_gain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._envelope_gain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_predriver_gain(self, arg):
        print "Setting predriver output gain to %f" % arg
        self._tb.set_txgain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._txgain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_input_gain(self, arg):
        print "Setting digital input gain to %f" % arg
        self._tb.set_digital_input_gain(arg)
        Qt.QMetaObject.invokeMethod(self._tb._digital_input_gain_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_squelch(self, arg):
        print "Setting squelch level to %f" % arg
        self._tb.set_squelch(arg)
        Qt.QMetaObject.invokeMethod(self._tb._squelch_slider, "setValue", Qt.Q_ARG("double", arg))
        return 0

    def _set_predistorter(self, arg):
        print "Setting predistortion file to " + arg
        self._tb.set_predistorter(arg)
        return 0

    def _set_predriver_delay(self, arg):
        print "Setting predriver delay to %f samples" % arg
        self._tb.set_predriver_delay(arg)
        return 0

    def _set_drive_delay(self, arg):
        print "Setting drive delay to %f samples" % arg
        self._tb.set_drive_delay(arg)
        return 0

    def _set_final_delay(self, arg):
        print "Setting final delay to %f samples" % arg
        self._tb.set_final_delay(arg)
        return 0

    def _set_test_output(self, arg):
        if arg==1:
            print "Setting output mode to TEST OUTPUT"
        else:
            print "Setting output mode to NORMAL"
        self._tb.set_env_phase_out(arg)
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
    parser.add_option("", "--predriver-delay", dest="predriver_delay", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set predriver delay [default=%default]")
    parser.add_option("", "--final-delay", dest="final_delay", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set final delay [default=%default]")
    parser.add_option("", "--drive-delay", dest="drive_delay", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set drive delay [default=%default]")
    parser.add_option("", "--port", type="intx", default=52001, help="Set TCP port to listen on [default=%default]")
    parser.add_option("", "--filename", type="string", default=expanduser("~") + "/rn13_files/" + "DLWF.txt", help="Set test waveform file source")
    parser.add_option("", "--predistorter", type="string", default=expanduser("~") + "/rn13_files/" + "Predistort.txt", help="Set predistortion table filename")
    parser.add_option("", "--preset", type="string", default=expanduser("~") + "/rn13_files/" + "CLABS_presets.txt", help="Load a presets file on startup (specify filename)")
    (options, args) = parser.parse_args()
    Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = CLABS_7_init(initial_txgain=options.txgain, rxfreq=options.rxfreq, samp_rate=options.samp_rate, initial_rxgain=options.rxgain, txfreq=options.txfreq, initial_baseband_gain=options.baseband_gain, filename=options.filename)
    cal_running = threading.Lock()

    class cal_thread(QThread):
        def __init__(self, tb):
            self.tb = tb
            super(cal_thread, self).__init__()

        def run(self):
            tb = self.tb
            print "Beginning calibration..."
            #create a cal output file with a timestamped name in ~/rn13_files/
            #or just grab the filename from the dialog
    #        filename = tb._calibrate_output_line_edit.text()
            filename = expanduser("~") + "/rn13_files/" + "calibration_%s" % strftime("%Y-%m-%d_%H:%M:%S")

            #switch to internal siggen
            tb.set_select(1)

            #enable output
            tb.set_off_switch(0)

            #set mod waveform to constant
            tb.set_mod_wave_chooser(0)

            #set mod type to CW
            tb.set_mod_type_chooser(0)

            #set modulation frequency to 5kHz
            tb.set_tone_freq(5e3)
            tb.set_mod_freq(0)

            #set predistorter to Linear
    #        tb.set_predistorter

            #set delays to zero: predriver, final, drive
            tb.set_predriver_delay(0)
            tb.set_final_delay(0)
            tb.set_drive_delay(0)

            #retrieve num avgs, num samples/avg, min ampl, max ampl, ampl steps
            navgs = int(tb._calibrate_N_line_edit.text())
            nperavg = int(tb._calibrate_K_line_edit.text())
            min_ampl = float(tb._calibrate_min_ampl_line_edit.text())
            max_ampl = float(tb._calibrate_max_ampl_line_edit.text())
            nsteps = int(tb._calibrate_num_steps_line_edit.text())
            fudge_factor = float(tb._calibrate_fudge_factor_line_edit.text())
            pause_between_steps = tb._cal_pause_checkbox_check_box.checkState()

            #write header to cal output file:
            #date, time, USRP name, TX/RX freqs, CORDIC settings, RF in gain, predriver gain,
            #final gain, driver gain, digital input gain,
            of = open(filename, 'w')
            of.write("#CLABS-7 calibration output file\n")
            of.write("#Date: %s\n" % strftime("%Y-%m-%d %H:%M:%S"))
            of.write("#Settings:\n")

            uhd_id = dict(tb.uhd_usrp_sink_0_0.get_usrp_info())
            of.write("#\tUSRP serial: %s\n" % uhd_id["mboard_serial"])
            of.write("#\tRF DB serial: %s\n" % uhd_id["tx_serial"])

            of.write("#\tTX RF frequency: %s\n" % tb.uhd_usrp_sink_0_0.get_center_freq())
            of.write("#\tRX RF frequency: %s\n" % tb.uhd_usrp_source_0.get_center_freq())

            of.write("#\tRX gain: %i\n" % tb.uhd_usrp_source_0.get_gain())
            of.write("#\tTX gain: %i\n" % tb.uhd_usrp_sink_0_0.get_gain())
            of.write("#\tDigital input gain: %i\n" % tb.get_digital_input_gain())

            of.write("#\tMinimum amplitude: %f, maximum amplitude: %f, steps: %i\n" % (min_ampl, max_ampl, nsteps))
            of.write("#\tNumber of averages: %i\n" % navgs)
            of.write("#\tNumber of samples per average: %i\n" % nperavg)

            of.write("#\tPredistorter filename: %s\n" % tb.get_predistorter())
            of.write("#\tFudge factor: %f\n" % fudge_factor)

            of.write("#LEVEL\tAMPLITUDE\tPHASE\n")

            #step through cal steps while recording
            for ampl in numpy.linspace(min_ampl,max_ampl,nsteps):
                print "Level: %f" % ampl
                tb.set_carrier_level(ampl)
                if(pause_between_steps):
                    wait = raw_input("Press enter to continue...")
                time.sleep(0.2)
                for i in range(navgs):
                    for j in range(nperavg):
                        avg = numpy.mean(tb.calibrate_average_probe.level())
                    print "I: %.2f Q: %.2f" % (avg.real, avg.imag)
                    print "Magnitude: %f (%f with f.f.)" % (abs(avg), abs(avg)*fudge_factor)
                    print "Phase: %f" % cmath.phase(avg)
                    of.write("%f\t%f\t%f\n" % (ampl, abs(avg)*fudge_factor, cmath.phase(avg)))

            #disable output
            tb.set_off_switch(1)
            #switch to external mode
            tb.set_select(0)

            #write cal data to file
            print "Wrote calibration output to %s" % filename

            #close cal file
            of.close()

    t = cal_thread(tb)
    def run_calibration():
        with cal_running:
            t.start()

    #hook up "start calibration" button
    _calibrate_start_push_button = Qt.QPushButton("Start")
    _calibrate_start_push_button.pressed.connect(run_calibration)
    tb.tab_grid_widget_grid_layout_5.addWidget(_calibrate_start_push_button,  1,1)
    tb._cal_pause_checkbox_check_box = Qt.QCheckBox("Pause between steps")
    tb.tab_grid_widget_grid_layout_5.addWidget(tb._cal_pause_checkbox_check_box,  1,2)

    tb.start()
    tb.show()
    tb._predistorter_line_edit.setText(options.predistorter)
    tb.set_predistorter(options.predistorter)
    tcp_server = clabs_tcp_ctrl(tb, options.port)
    tcp_server._set_predriver_delay(options.predriver_delay)
    tcp_server._set_drive_delay(options.drive_delay)
    tcp_server._set_final_delay(options.final_delay)
    tb.uhd_usrp_source_0.set_auto_dc_offset(False, 0)
    print "Rx freq: %fHz" % tb.uhd_usrp_source_0.get_center_freq()
    print "Tx freq: %fHz" % tb.uhd_usrp_sink_0_0.get_center_freq()

    #read presets file, if applicable
    if options.preset is not None:
        try:
            f = open(options.preset, 'r')
        except IOError as e:
            print e
            sys.exit(0)

        for line in f:
            if line[0:2].isalpha():
                cmd = line[0:2]
                arg = line[3:]

                retstr = "%s " % line[0:2]
                retstr += str(tcp_server.parse(cmd, arg))
                print retstr

        f.close()

    tcp_server.start()
    def quitting():
        tb.stop()
        tb.wait()
        tcp_server.stop()
        tcp_server.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    time.sleep(1)
    tb = None #to clean up Qt widgets
