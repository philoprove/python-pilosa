# Copyright 2017 Pilosa Corp.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
#

import unittest

from pilosa.exceptions import PilosaError
from pilosa.imports import csv_bit_reader, batch_bits

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


class ImportsTestCase(unittest.TestCase):

    def test_csvbititerator(self):
        reader = csv_bit_reader(StringIO(u"""
            1,10,683793200
            5,20,683793300
            3,41,683793385        
            10,10485760,683793385        
        """))
        slice_bit_groups = list(batch_bits(reader, 2))
        self.assertEqual(3, len(slice_bit_groups))

        slice1, batch1 = slice_bit_groups[0]
        self.assertEqual(slice1, 0)
        self.assertEqual(2, len(list(batch1)))

        slice2, batch2 = slice_bit_groups[1]
        self.assertEqual(slice2, 0)
        self.assertEqual(1, len(list(batch2)))

        slice3, batch3 = slice_bit_groups[2]
        self.assertEqual(slice3, 10)
        self.assertEqual(1, len(list(batch3)))

    def test_invalid_input(self):
        invalid_inputs = [
            # less than 2 columns
            u"155",
            # invalid row ID
            u"a5,155",
            # invalid column ID
            u"155,a5",
            # invalid timestamp
            u"155,255,a5",
        ]

        for text in invalid_inputs:
            reader = csv_bit_reader(StringIO(text))
            self.assertRaises(PilosaError, list, reader)

