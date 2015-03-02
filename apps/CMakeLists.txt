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

set(GMRR_RN13_PHASE1 ${CMAKE_CURRENT_BINARY_DIR}/CLABS_1A.py)
set(GMRR_RN13_PHASE1_GRC ${CMAKE_CURRENT_SOURCE_DIR}/CLABS-1A.grc)

set(GMRR_RN13_PHASE3_init ${CMAKE_CURRENT_BINARY_DIR}/CLABS_3_init.py)
set(GMRR_RN13_PHASE3_app ${CMAKE_CURRENT_SOURCE_DIR}/CLABS_3.py)
set(GMRR_RN13_PHASE3_GRC ${CMAKE_CURRENT_SOURCE_DIR}/CLABS-3.grc)
set(GMRR_RN13_PHASE3_DLWF ${CMAKE_CURRENT_SOURCE_DIR}/DLWF.txt)
set(GMRR_RN13_PHASE4_init ${CMAKE_CURRENT_BINARY_DIR}/CLABS_4_init.py)
set(GMRR_RN13_PHASE4_app ${CMAKE_CURRENT_SOURCE_DIR}/CLABS_4.py)
set(GMRR_RN13_PHASE4_GRC ${CMAKE_CURRENT_SOURCE_DIR}/CLABS-4.grc)
set(GMRR_RN13_PHASE5_init ${CMAKE_CURRENT_BINARY_DIR}/CLABS_5_init.py)
set(GMRR_RN13_PHASE5_app ${CMAKE_CURRENT_SOURCE_DIR}/CLABS_5.py)
set(GMRR_RN13_PHASE5_GRC ${CMAKE_CURRENT_SOURCE_DIR}/CLABS-5.grc)
set(GMRR_RN13_PHASE5_EXPD1 ${CMAKE_CURRENT_SOURCE_DIR}/EXPD1.txt)
set(GMRR_RN13_PHASE5_EXPD2 ${CMAKE_CURRENT_SOURCE_DIR}/Predistort.txt)
set(GMRR_RN13_PHASE6_init ${CMAKE_CURRENT_BINARY_DIR}/CLABS_6_init.py)
set(GMRR_RN13_PHASE6_app ${CMAKE_CURRENT_SOURCE_DIR}/CLABS_6.py)
set(GMRR_RN13_PHASE6_GRC ${CMAKE_CURRENT_SOURCE_DIR}/CLABS-6.grc)

set(GMRR_RN13_PRESETS ${CMAKE_CURRENT_SOURCE_DIR}/CLABS_presets.txt)

#use GRCC to make executable
add_custom_command(OUTPUT ${GMRR_RN13_PHASE1}
    COMMAND ${GRCC} ${GMRR_RN13_PHASE1_GRC} -d ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_PHASE1_GRC}
                  )

add_custom_command(OUTPUT ${GMRR_RN13_PHASE3_init}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/stupid_kluge.sh ${PROJECT_SOURCE_DIR}/grc ${GRCC} ${GMRR_RN13_PHASE3_GRC} ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_PHASE3_GRC}
                  )

add_custom_command(OUTPUT ${GMRR_RN13_PHASE4_init}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/stupid_kluge.sh ${PROJECT_SOURCE_DIR}/grc ${GRCC} ${GMRR_RN13_PHASE4_GRC} ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_PHASE4_GRC}
                  )

add_custom_command(OUTPUT ${GMRR_RN13_PHASE5_init}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/stupid_kluge.sh ${PROJECT_SOURCE_DIR}/grc ${GRCC} ${GMRR_RN13_PHASE5_GRC} ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_PHASE5_GRC}
                  )

add_custom_command(OUTPUT ${GMRR_RN13_PHASE6_init}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/stupid_kluge.sh ${PROJECT_SOURCE_DIR}/grc ${GRCC} ${GMRR_RN13_PHASE6_GRC} ${CMAKE_CURRENT_BINARY_DIR}
                   MAIN_DEPENDENCY ${GMRR_RN13_PHASE6_GRC}
                  )

add_custom_target(gmrr_rn13_phase1 ALL DEPENDS ${GMRR_RN13_PHASE1})
add_custom_target(gmrr_rn13_phase3 ALL DEPENDS ${GMRR_RN13_PHASE3_init})
add_custom_target(gmrr_rn13_phase4 ALL DEPENDS ${GMRR_RN13_PHASE4_init})
add_custom_target(gmrr_rn13_phase5 ALL DEPENDS ${GMRR_RN13_PHASE5_init})
add_custom_target(gmrr_rn13_phase6 ALL DEPENDS ${GMRR_RN13_PHASE6_init})

GR_PYTHON_INSTALL(
    PROGRAMS ${GMRR_RN13_PHASE1} ${GMRR_RN13_PHASE3_init} ${GMRR_RN13_PHASE3_app} ${GMRR_RN13_PHASE4_init} ${GMRR_RN13_PHASE4_app} ${GMRR_RN13_PHASE5_init} ${GMRR_RN13_PHASE5_app} ${GMRR_RN13_PHASE6_init} ${GMRR_RN13_PHASE6_app}
    DESTINATION bin
)

install(
    FILES ${GMRR_RN13_PHASE3_DLWF} ${GMRR_RN13_PHASE5_EXPD1} ${GMRR_RN13_PHASE5_EXPD2} ${GMRR_RN13_PRESETS}
    DESTINATION $ENV{HOME}/rn13_files
)
