# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

include(GrPython)

#find GRCC
find_program(GRCC
             NAMES grcc
             PATHS /usr/local/bin /usr/bin
            )

set(GMRR_RN13 ${CMAKE_CURRENT_BINARY_DIR}/rn13.py)
set(GMRR_RN13_GRC ${CMAKE_CURRENT_SOURCE_DIR}/rn13.grc)

add_custom_target(gmrr_rn13 ALL DEPENDS ${GMRR_RN13})

#use GRCC to make executable
add_custom_command(OUTPUT ${GMRR_RN13}
                   COMMAND ${GRCC} ${GMRR_RN13_GRC} -d ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_GRC}
                  )


GR_PYTHON_INSTALL(
    PROGRAMS ${GMRR_RN13}
    DESTINATION bin
)
