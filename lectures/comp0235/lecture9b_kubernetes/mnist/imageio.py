# Write PGM images, with the classification as the comment.
# d - the 2d list to write.
# filename - the file to write to.
# classification - the classification of the image
def writepgm(d, filename, classification):
    buffer = 2147483647 # 2 megabytes
    white = 255
    x = len(d)
    y = len(d[0])

# Open our file.
    f = open(filename, mode='w', buffering=buffer)

# Write header.
    f.write('P2\n')
    f.write(f'# {classification}\n')
    f.write(f'{x} {y}\n')
    f.write(f'{white}\n')

# Write out 2d list.
    for j in range(y):
        for i in range(x):
            v = d[j][i]
            quantised = int(v * (white))
            
            # Protect against having colour values outside our range.
            if quantised < 0:
                quantised = 0
            if quantised >= white:
                quantised = white

            f.write(f'{quantised} ')
        f.write('\n')

# Tidy up.
    f.close()

def readpgm(filename):
    import numpy

    with open(filename) as f:
        raw_str = f.read().splitlines()

        # Line 0 is "P2"
        assert raw_str[0].strip() == "P2"

        # Line 1 is classification
        classification = raw_str[1][1:].strip()

        # Line 2 is width, height
        width_s, height_s = raw_str[2].split()
        width = int(width_s)
        height = int(height_s)

        # Line 3 is white value, should be 255
        white = int(raw_str[3])

        if white != 255:
            print(f"Warning - white value is not 255: {white}")
        
        # Initialise image
        image = numpy.zeros(shape=(height,width))
        for ln in range(height):
            numberline = raw_str[4 + ln].split()
            for pt in range(width):
                quantised = int(numberline[pt])
                realval = quantised/white
                image[ln,pt] = realval

        return classification, image
