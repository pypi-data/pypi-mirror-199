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
'''Ashberry generator'''
import random
import string

from enum import Enum


SCHEMES = ['https', 'http']
EXTENSIONS = ['com', 'org', 'net']

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits


class Level(Enum):
    '''
    Represents a Juneberry level

    Attributes:
        FIRST (int): First level of generation
        SECOND (int): Second level of generation
        THIRD (int): Third level of generation
    '''
    FIRST = 10
    SECOND = 15
    THIRD = 20


class Generator:
    '''
    Represents a Juneberry generator

    Attributes:
        level (int): Level of generation
    '''
    def __init__(self, *, level: Level=Level.FIRST) -> None:
        self.level = level

    def generate(self) -> str:
        '''Generate URL'''
        domain = str()
        characters = str()

        levels = {
            '10': LOWER,
            '15': LOWER + UPPER,
            '20': LOWER + UPPER + DIGITS
        }

        characters += levels[str(self.level)]

        for _ in range(random.randint(1, 15)):
            domain += random.choice(characters)

        scheme = random.choice(SCHEMES)
        extension = random.choice(EXTENSIONS)

        URL = f'{scheme}://{domain}.{extension}'

        return URL
