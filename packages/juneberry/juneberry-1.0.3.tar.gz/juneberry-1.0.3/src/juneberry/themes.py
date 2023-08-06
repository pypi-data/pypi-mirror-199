# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2023 mmlvgx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
'''Juneberry themes'''
from .colors import Color


class Theme:
    '''
    Represents a Juneberry theme

    Attributes:
        info (str): Color for info level
        warn (str): Color for warn level
        debug (str): Color for deubg level
        error (str): Color for error level
        fatal (str): Color for fatal level
        timestamp (str): Color for timestamp
        message (str): Color for message
    '''

    def __init__(
        self,
        info=None,
        warn=None,
        debug=None,
        error=None,
        fatal=None,
        timestamp=None,
        message=None,
    ) -> None:
        self.info = info
        self.warn = warn
        self.debug = debug
        self.error = error
        self.fatal = fatal
        self.timestamp = timestamp
        self.message = message


# Default theme
default = Theme(
    Color.Default.WHITE,  # INFO
    Color.Default.BLUE,  # WARN
    Color.Default.YELLOW,  # DEBUG
    Color.Default.RED,  # ERROR
    Color.Default.RED,  # FATAL
    Color.Default.GREEN,  # Timestamp
    Color.Default.GREEN,  # Message
)
