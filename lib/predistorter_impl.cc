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
#include "predistorter_impl.h"
#include <string>
#include <cstdlib>
#include <fstream>

namespace gr {
  namespace gmrr_rn13 {

    predistorter::sptr
    predistorter::make(std::string filename)
    {
      return gnuradio::get_initial_sptr
        (new predistorter_impl(filename));
    }

    /*
     * The private constructor
     */
    predistorter_impl::predistorter_impl(std::string filename)
      : gr::sync_block("predistorter",
              gr::io_signature::make(1, 10, sizeof(float)),
              gr::io_signature::make(1, 10, sizeof(float)))
    {
        load(filename);
    }

    /*
     * Our virtual destructor.
     */
    predistorter_impl::~predistorter_impl()
    {
    }

    /* Yes, the GMRR predistortion tables include extra columns for plotting and indexing, but
     * we'll just read them in anyway.
     */
    void predistorter_impl::load(std::string filename)
    {
        std::ifstream f;
        f.open(filename.c_str(), std::ios::in);
        int tablesize;


        if(!f.is_open()) {
            std::cout << "Could not open file: " << filename << std::endl;
            return;
        }

        d_table.clear();
        std::string line;
        std::getline(f, d_title);
        while(std::getline(f, line)) {
            if(line[0] != '/') {
                std::stringstream linestream(line);
                std::string cell;
                std::vector<float> table_entry;
                while(std::getline(linestream, cell, ',')) {
                    table_entry.push_back(std::strtod(cell.c_str(), NULL));
                }
                if(table_entry.size() > 1) {
                    d_table.push_back(table_entry);
                } else {
                    if(table_entry[0] > 0) {
                        tablesize = table_entry[0];
                    }
                }
            }
        }

        std::cout << "Predistorter: read " << d_table.size() << " entries from predistortion file." << std::endl;
        if(d_table.size() != tablesize) throw std::runtime_error("Table size does not match number of entries.");
    }

    static float interpolate(std::vector<std::vector<float> > &table, int index, float value)
    {
        /* perform linear interpolation on value,
         * using table[...][-1] as the input column
         * and table[...][index] as the output column */
        //clip to table values
        if(value < table.front().back()) value = table.front().back();
        if(value > table.back().back())  value = table.back().back();

        /* take care of the edge cases */
        if(value == table.front().back()) return table.front()[index];
        if(value == table.back().back()) return table.back()[index];

        int i=table.size()-1;
        while(table[i].back() > value ) i--;

        float d_t = value - table[i].back();
        float d_i = table[i+1].back() - table[i].back();
        float d_o = table[i+1][index] - table[i][index];
        float retval = table[i][index] + d_t * d_o / d_i;

        return retval;
    }

    std::string predistorter_impl::get_title(void)
    {
        return d_title;
    }

    int
    predistorter_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        int ninputs = input_items.size();

        for(int i=0; i<ninputs; i++) {
            const float *in = (const float *) input_items[i];
            float *out = (float *) output_items[i];

            for(int j=0; j<noutput_items; j++) {
                out[j] = interpolate(d_table, i, in[j]);
            }
        }


        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace gmrr_rn13 */
} /* namespace gr */

