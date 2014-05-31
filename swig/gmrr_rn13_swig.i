/* -*- c++ -*- */

#define GMRR_RN13_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "gmrr_rn13_swig_doc.i"

%{
#include "skippy/stream_selector.h"
%}


%include "skippy/stream_selector.h"
GR_SWIG_BLOCK_MAGIC2(gmrr_rn13, stream_selector);
