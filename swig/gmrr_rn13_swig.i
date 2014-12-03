/* -*- c++ -*- */

#define GMRR_RN13_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "gmrr_rn13_swig_doc.i"

%{
#include "gmrr_rn13/gmrr_waveform_src.h"
#include "gmrr_rn13/predistorter.h"
%}


%include "gmrr_rn13/gmrr_waveform_src.h"
GR_SWIG_BLOCK_MAGIC2(gmrr_rn13, gmrr_waveform_src);
%include "gmrr_rn13/predistorter.h"
GR_SWIG_BLOCK_MAGIC2(gmrr_rn13, predistorter);
