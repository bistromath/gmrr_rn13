/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "stream_sel_impl.h"

namespace gr {
  namespace gmrr_rn13 {

    stream_sel::sptr
    stream_sel::make(size_t sizeof_stream_item, size_t ninputs, size_t sel, bool block)
    {
      return gnuradio::get_initial_sptr
        (new stream_sel_impl(sizeof_stream_item, ninputs, sel, block));
    }

    /*
     * The private constructor
     */
    stream_sel_impl::stream_sel_impl(size_t sizeof_stream_item, size_t ninputs, size_t sel, bool block)
      : gr::block("stream_sel",
              gr::io_signature::make(ninputs, ninputs, sizeof_stream_item),
              gr::io_signature::make(1, 1, sizeof_stream_item))
    {
        d_block = block;
        d_size = sizeof_stream_item;
        d_ninputs = ninputs;
        d_sel = sel;
    }

    /*
     * Our virtual destructor.
     */
    stream_sel_impl::~stream_sel_impl()
    {
    }

    void stream_sel_impl::set_sel(size_t which) {
      boost::lock_guard<boost::mutex> guard(d_mtx);
      if(which >= d_ninputs) {
	std::cerr << "stream_sel: can't set value outside ninputs" << std::endl;
        return;
      }
      d_sel = which;
    }

    int
    stream_sel_impl::general_work(int noutput_items,
	gr_vector_int &ninput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      boost::lock_guard<boost::mutex> guard(d_mtx);
      const void *in = (const void *) input_items[d_sel];
      void *out = (void *) output_items[0];
      size_t nitems = std::min(ninput_items[d_sel], noutput_items);

      memcpy(out, in, nitems*d_size);

      if(d_block == false) {
        consume_each(nitems);
      } else {  
        consume(d_sel, nitems);
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace gmrr_rn13 */
} /* namespace gr */

