# MIT License

# Copyright (c) 2022 Dr Owain Kenway

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Micro Library to print out a greyscale 2D python data structure as an
# "ASCII-art" to the terminal.

# Owain Kenway, The third of November in the year of our Lord two thousand
#               and twenty-two.

# Assumptions: The 2D structure is "well formed" as in the fields are all a 
#              double between 0.0 and 1.0.
#              The structure is rectangular i.e. width is the same for each
#              row.

COLOURS=' ░▒▓█'
ASCII_COLOURS=' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
EMOJI_COLOURS=['️⬛','🟫','🟧','🟥','🟪','🟦','🟩','🟨️','⬜']

# 256 colour ANSI
_ansi_colour_numbers = [x + 231 + 1 for x in range(24)]
_ansi_colour_numbers.append(231)
ANSI_COLOURS=['\033[48;5;'+str(x)+'m  \033[m' for x in _ansi_colour_numbers]

def show(data, colours=ANSI_COLOURS):
	height = len(data)
	num_colours=len(colours)
	for a in range(height):
		width = len(data[a])
		for b in range(width):
			v = data[a][b]
			quantised = int(v * (num_colours - 1))

# Protect against having colour values outside our range.
			if quantised < 0:
				quantised = 0
			if quantised >= num_colours - 1:
				quantised = num_colours - 1

			print(colours[quantised], end='')
		print('')
