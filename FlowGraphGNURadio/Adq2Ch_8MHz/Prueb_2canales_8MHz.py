#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Prueba 2 canales
# Author: Isaac Tupac
# GNU Radio version: 3.8.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from datetime import datetime
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import Generator_ROJ
import gpsdo  # embedded python module
import numpy as np; import gr_digital_rf

from gnuradio import qtgui

class Prueb_2canales_8MHz(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Prueba 2 canales")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Prueba 2 canales")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "Prueb_2canales_8MHz")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.freq_centr = freq_centr = 8e6
        self.freq_almac = freq_almac = 100000
        self.filter_taps = filter_taps = (1,)*int(100)
        self.decimation = decimation = 100
        self.Longitud = Longitud = gpsdo.Longitud
        self.Long_ind = Long_ind = gpsdo.Long_ind
        self.Latitud = Latitud = gpsdo.Latitud
        self.Lat_ind = Lat_ind = gpsdo.Lat_ind

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_subdev_spec("A:B A:A", 0)
        self.uhd_usrp_source_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_0.set_center_freq(freq_centr, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_source_0.set_center_freq(freq_centr, 1)
        self.uhd_usrp_source_0.set_gain(0, 1)
        self.uhd_usrp_source_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 1)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.gr_digital_rf_digital_rf_channel_sink_0_0 = gr_digital_rf.digital_rf_channel_sink(
            channel_dir='/home/soporte/Isaac/AdquIonoSDR/DataAdquirida/2Canales/Canal1',
            dtype=np.complex64,
            subdir_cadence_secs=3600,
            file_cadence_millisecs=1000,
            sample_rate_numerator=freq_almac,
            sample_rate_denominator=1,
            start=None,
            ignore_tags=False,
            is_complex=True,
            num_subchannels=1,
            uuid_str=None,
            center_frequencies=(
                None
            ),
            metadata={"samp_rate":samp_rate,"bandwidth":samp_rate,"decimation":decimation,"storFreq":freq_almac,"filterTaps":filter_taps,"centerFreq":freq_centr,"Latitud":Latitud,"Lat_ind":Lat_ind,"Longitud":Longitud,"Long_ind":Long_ind},
            is_continuous=True,
            compression_level=0,
            checksum=False,
            marching_periods=True,
            stop_on_skipped=False,
            stop_on_time_tag=False,
            debug=False,
            min_chunksize=None,
        )
        self.gr_digital_rf_digital_rf_channel_sink_0 = gr_digital_rf.digital_rf_channel_sink(
            channel_dir='/home/soporte/Isaac/AdquIonoSDR/DataAdquirida/2Canales/Canal0',
            dtype=np.complex64,
            subdir_cadence_secs=3600,
            file_cadence_millisecs=1000,
            sample_rate_numerator=freq_almac,
            sample_rate_denominator=1,
            start=None,
            ignore_tags=False,
            is_complex=True,
            num_subchannels=1,
            uuid_str=None,
            center_frequencies=(
                None
            ),
            metadata={"samp_rate":samp_rate,"bandwidth":samp_rate,"decimation":decimation,"storFreq":freq_almac,"filterTaps":filter_taps,"centerFreq":freq_centr,"Latitud":Latitud,"Lat_ind":Lat_ind,"Longitud":Longitud,"Long_ind":Long_ind},
            is_continuous=True,
            compression_level=0,
            checksum=False,
            marching_periods=True,
            stop_on_skipped=False,
            stop_on_time_tag=False,
            debug=False,
            min_chunksize=None,
        )
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccc(decimation, filter_taps)
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccc(decimation, filter_taps)
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fft_filter_xxx_0_0 = filter.fft_filter_ccc(1, (1,1,1,1,1,1), 2)
        self.fft_filter_xxx_0_0.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (1,1,1,1,1,1), 2)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle_0_0_0_2_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_0_2_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, freq_almac,True)
        self.blocks_throttle_0_0_0_2_0 = blocks.throttle(gr.sizeof_gr_complex*1, freq_almac,True)
        self.blocks_throttle_0_0_0_2 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_xx_0_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.Generator_ROJ_Generator_ROJ_0 = Generator_ROJ.Generator_ROJ(samp_rate, 'Seno', 500e-3, '/home/soporte/Isaac/ProgrDemo/all_freq_list_10ms.txt', freq_centr, 0, 20)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Generator_ROJ_Generator_ROJ_0, 0), (self.blocks_throttle_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_throttle_0_0_0, 0), (self.blocks_multiply_xx_0_0_0_0, 1))
        self.connect((self.blocks_throttle_0_0_0_2, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0_2_0, 0), (self.gr_digital_rf_digital_rf_channel_sink_0, 0))
        self.connect((self.blocks_throttle_0_0_0_2_0_0, 0), (self.gr_digital_rf_digital_rf_channel_sink_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0_2_1, 0), (self.blocks_multiply_xx_0_0_0_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_throttle_0_0_0_2_0, 0))
        self.connect((self.fft_filter_xxx_0_0, 0), (self.blocks_throttle_0_0_0_2_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.fft_filter_xxx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_throttle_0_0_0_2, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_throttle_0_0_0_2_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Prueb_2canales_8MHz")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_2.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_2_1.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 1)

    def get_freq_centr(self):
        return self.freq_centr

    def set_freq_centr(self, freq_centr):
        self.freq_centr = freq_centr
        self.uhd_usrp_source_0.set_center_freq(self.freq_centr, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq_centr, 1)

    def get_freq_almac(self):
        return self.freq_almac

    def set_freq_almac(self, freq_almac):
        self.freq_almac = freq_almac
        self.blocks_throttle_0_0_0_2_0.set_sample_rate(self.freq_almac)
        self.blocks_throttle_0_0_0_2_0_0.set_sample_rate(self.freq_almac)

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.fir_filter_xxx_0_0.set_taps(self.filter_taps)
        self.fir_filter_xxx_0_0_0.set_taps(self.filter_taps)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_Longitud(self):
        return self.Longitud

    def set_Longitud(self, Longitud):
        self.Longitud = Longitud

    def get_Long_ind(self):
        return self.Long_ind

    def set_Long_ind(self, Long_ind):
        self.Long_ind = Long_ind

    def get_Latitud(self):
        return self.Latitud

    def set_Latitud(self, Latitud):
        self.Latitud = Latitud

    def get_Lat_ind(self):
        return self.Lat_ind

    def set_Lat_ind(self, Lat_ind):
        self.Lat_ind = Lat_ind

def snipfcn_snippet_0(self):
    nmea=self.uhd_usrp_source_0.get_mboard_sensor("gps_gpgga").to_pp_string() #Adquiere la hora gps local
    print('El valor del  nmea completo es:',nmea)
    valor_posic=nmea[18:26]
    valor_posic=float(valor_posic)
    #print("El tipo de valor_posic es:",type(valor_int))
    print('El valor UTC de:l inicio del programa es:',valor_posic)
    valor_latitud=nmea[28:37]
    print('El valor de la latitud es:',valor_latitud)
    latitud_indica=nmea[38]
    print('El valor del indicador de la latitud es:',latitud_indica)
    valor_longitud=nmea[40:50]
    print('El valor de la longitud es:',valor_longitud)
    longitud_indica=nmea[51]
    print('El valor del indicador de la longitud es:',longitud_indica)
    f=open("/home/soporte/Isaac/AdquisIonosOblic/gpsdo.txt","w")
    f.writelines([valor_latitud+"\n",latitud_indica+"\n",valor_longitud+"\n",longitud_indica+"\n"])

def snipfcn_snippet_2_0_1_0_0_0(self):
    gps_time=uhd.time_spec_t(self.uhd_usrp_source_0.get_mboard_sensor("gps_time").to_int()+1.0) #Adquiere la hora gps local
    print('El valor de  gps_time es:',gps_time)
    self.uhd_usrp_source_0.set_time_next_pps(gps_time); # setea el tiempo gps en el siguiente PPS

    Full_second=gps_time.get_full_secs() #Adquiere el epoch en seg.

    UTC_time= datetime.utcfromtimestamp(Full_second) # Adquiere el tiempo en formato de UTC

    year=int(UTC_time.strftime("%Y"))
    print('El valor de  year es:',year)
    month=int(UTC_time.strftime("%m"))
    print('El valor de  month es:',month)
    day=int(UTC_time.strftime("%d"))
    print('El valor de  day es:',day)
    hour=int(UTC_time.strftime("%H"))
    print('El valor de  hour es:',hour)
    minute=int(UTC_time.strftime("%M"))
    print('El valor de  minute es:',minute)
    second=int(UTC_time.strftime("%S"))
    print('El valor de  second es:',second)

    if(hour>=5):
     dayN=day
     monthF=month

    if (hour==0):
     hour=24
     dayN=(day-1)
     monthF=month
    elif (hour==1):
     hour=25
     dayN=(day-1)
     monthF=month
    elif (hour==2):
     hour=26
     dayN=(day-1)
     monthF=month
    elif (hour==3):
     hour=27
     dayN=(day-1)
     monthF=month
    elif (hour==4):
     hour=28
     dayN=(day-1)
     monthF=month

    if (((month==2) or (month==4) or (month==6) or (month==8) or (month==9) or (month==11) or (month==1)) and (dayN==0)):
     dayN=31
     monthF=month-1
    elif (((month==3) or (month==5) or (month==7) or (month==10) or (month==12)) and (dayN==0)):
     if(month==3):
      dayN=28
      monthF=month-1
      if(year%4==0): #bisiesto
       dayN=29
       monthF=month-1
     else:
      dayN=30
      monthF=month-1

    print('El valor de  dayN es:',dayN)
    print('El valor de monthF es:',monthF)
    print('El valor de  hour -5 es:',hour-5)
    #date_time = datetime(year, monthF, dayN, (hour-5), (minute+1), 4) # Se resta 5h para ponerlo en hora local (gps), se suma 1seg porque el crontab fue corrido un seg antes
    date_time = datetime(year, monthF, dayN, (hour-5), (minute+1), 5)

    unix_time=time.mktime(date_time.timetuple())# epoch time en el cual comenzara la adquisicion por USRP
    print('El valor de unix_times es:',unix_time)
    # Poner 4s+960ms o 4s+1.0s
    #self.uhd_usrp_source_0.set_start_time(uhd.time_spec_t(unix_time,1.120))
    #self.uhd_usrp_source_0.set_start_time(uhd.time_spec_t(unix_time,0.960))
    self.uhd_usrp_source_0.set_start_time(uhd.time_spec_t(unix_time)) #Para 4seg y 5 seg


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)
    snipfcn_snippet_2_0_1_0_0_0(tb)




def main(top_block_cls=Prueb_2canales_8MHz, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
