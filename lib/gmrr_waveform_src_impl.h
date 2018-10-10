/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_GMRR_RN13_GMRR_WAVEFORM_SRC_IMPL_H
#define INCLUDED_GMRR_RN13_GMRR_WAVEFORM_SRC_IMPL_H

#include <gmrr_rn13/gmrr_waveform_src.h>
#include <mutex>
#include <string>

namespace gr {
  namespace gmrr_rn13 {

    class gmrr_waveform_src_impl : public gmrr_waveform_src
    {
     private:
        std::vector<gr_complex> d_vec;
        size_t d_offset;
	std::mutex d_lock;
	void read_file(std::string filename);

     public:
      gmrr_waveform_src_impl(std::string filename);
      ~gmrr_waveform_src_impl();

      void set_filename(std::string filename);

      // Where all the action really happens
      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace gmrr_rn13
} // namespace gr

#endif /* INCLUDED_GMRR_RN13_GMRR_WAVEFORM_SRC_IMPL_H */

