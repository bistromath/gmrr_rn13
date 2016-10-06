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


#ifndef INCLUDED_GMRR_RN13_STREAM_SEL_H
#define INCLUDED_GMRR_RN13_STREAM_SEL_H

#include <gmrr_rn13/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace gmrr_rn13 {

    /*!
     * \brief <+description of block+>
     * \ingroup gmrr_rn13
     *
     */
    class GMRR_RN13_API stream_sel : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<stream_sel> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of gmrr_rn13::stream_sel.
       *
       * To avoid accidental use of raw pointers, gmrr_rn13::stream_sel's
       * constructor is in a private implementation
       * class. gmrr_rn13::stream_sel::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t sizeof_stream_item, size_t ninputs, size_t sel, bool block=true);
      virtual void set_sel(size_t which) = 0;
    };

  } // namespace gmrr_rn13
} // namespace gr

#endif /* INCLUDED_GMRR_RN13_STREAM_SEL_H */

