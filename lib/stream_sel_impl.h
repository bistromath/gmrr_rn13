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

#ifndef INCLUDED_GMRR_RN13_STREAM_SEL_IMPL_H
#define INCLUDED_GMRR_RN13_STREAM_SEL_IMPL_H

#include <gmrr_rn13/stream_sel.h>
#include <boost/thread.hpp>

namespace gr {
  namespace gmrr_rn13 {

    class stream_sel_impl : public stream_sel
    {
     private:
        size_t d_ninputs;
        size_t d_sel;
        bool d_block;
        size_t d_size;
        boost::mutex d_mtx;

     public:
      stream_sel_impl(size_t sizeof_stream_item, size_t ninputs, size_t sel, bool block);
      ~stream_sel_impl();

      // Where all the action really happens
      int general_work(int noutput_items,
         gr_vector_int &ninput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
      void set_sel(size_t which);
    };

  } // namespace gmrr_rn13
} // namespace gr

#endif /* INCLUDED_GMRR_RN13_STREAM_SEL_IMPL_H */

