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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include "gmrr_waveform_src_impl.h"

namespace gr {
  namespace gmrr_rn13 {

    gmrr_waveform_src::sptr
    gmrr_waveform_src::make(std::string filename)
    {
      return gnuradio::get_initial_sptr
        (new gmrr_waveform_src_impl(filename));
    }

    void 
    gmrr_waveform_src_impl::read_file(std::string filename) {
        //open file
        std::ifstream file(filename.c_str());
        assert(file.is_open());
	std::lock_guard<std::mutex> lock(d_lock);
	d_vec.clear();

        //read file, parse to d_vec
        std::string line;
        std::getline(file, line);
        std::getline(file, line);

        while(std::getline(file, line)) {
            std::istringstream ss(line);
            std::string s;
            std::getline(ss, s, ',');
            float i=atof(s.c_str());
            std::getline(ss, s, ',');
            float q=atof(s.c_str());
            d_vec.push_back(gr_complex(i,q));
        }
        std::cout << "Waveform has " << d_vec.size() << " entries." << std::endl;
    }

    /*
     * The private constructor
     */
    gmrr_waveform_src_impl::gmrr_waveform_src_impl(std::string filename)
      : gr::sync_block("gmrr_waveform_src",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_offset(0)
    {
        read_file(filename);
    }

    /*
     * Our virtual destructor.
     */
    gmrr_waveform_src_impl::~gmrr_waveform_src_impl()
    {
    }

    void
    gmrr_waveform_src_impl::set_filename(std::string filename)
    {
	read_file(filename);
    }

    int
    gmrr_waveform_src_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        gr_complex *out = (gr_complex *) output_items[0];

        size_t oidx = 0;
	std::lock_guard<std::mutex> lock(d_lock);
        while(oidx < noutput_items) {
            out[oidx] = d_vec[d_offset];
            d_offset = (d_offset+1)%d_vec.size();
            oidx++;
        }
        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace gmrr_rn13 */
} /* namespace gr */

