import numpy as np
import Image
import StringIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def convert_to_codeword(binary_message):
    codewords = [[1,0,0,0,0],
                 [1,0,1,1,1],
                 [0,1,0,0,1],
                 [0,1,1,1,0]]

    for first, second in chunks(binary_message, 2):
        if first == 0 and second == 0:
            codeword = codewords[0]
        elif first == 0 and second == 1:
            codeword = codewords[1]
        elif first == 1 and second == 0:
            codeword = codewords[2]
        elif first == 1 and second == 1:
            codeword = codewords[3]
        else:
            print "Error"

        yield codeword

def convert_to_binary_string(num, length=8):
    """
    Convert a number into a list of binary digits
    :param num: The number to convert
    :param length: The minimum length of the returned binary number (padding)
    :return: A list of binary digits representing the input number
    """
    return format(num, '0{}b'.format(length))

def convert_to_binary_list(num, length=8):
    return [int(digit) for digit in list(convert_to_binary_string(num, length))]

def chunks(arr, size):
    """
    Yield successive n-sized chunks from arr.
    :param arr: The input array
    :param size: The size of the desired sub-arrays
    :return: Yield a chunk of the original array of size
    """
    for i in xrange(0, len(arr), size):
        yield arr[i:i+size]

def draw_marker(cv, x, y, number=213, size=7):
    image_size = size * cm

    # Back up to bottom, left-hand corner
    x -= (image_size / 2)
    y -= (image_size / 2)

    # Divide the region into 7 sub-squares
    square_size = image_size / 7

    # Set the color to black for stroke and fill
    cv.setStrokeColorRGB(0.0, 0.0, 0.0)
    cv.setFillColorRGB(0.0, 0.0, 0.0)

    # Get the codewords for the number
    message = np.array(list(convert_to_codeword(convert_to_binary_list(number, 10))))

    # Draw a thin outline
    cv.rect(x - (square_size / 2), y - (square_size / 2), image_size + square_size, image_size + square_size, 1)

    # Draw a black box inside
    cv.rect(x, y, image_size, image_size, 1, 1)

    x += square_size
    y += square_size

    # Change the color to white for stroke and fill
    cv.setStrokeColorRGB(1.0, 1.0, 1.0)
    cv.setFillColorRGB(1.0, 1.0, 1.0)
    for column in range(0, 5):
        for row in range(0, 5):
            if message[4 - column, row] == 1:
                x_offset = (square_size * row)
                y_offset = (square_size * column)
                cv.rect(x + x_offset, y + y_offset, square_size, square_size, 1, 1)

    cv.save()

def main():
    pagesize = A4
    number = 213
    size = 5
    font_size = 24
    font_name = 'Helvetica'
    title = 'Marker %d - %d cm' % (number, size)
    filename = 'marker_%04d.pdf' % number

    packet = StringIO.StringIO()

    cv = canvas.Canvas(packet, pagesize)
    page_width, page_height = pagesize
    cv.setFont(font_name, font_size)
    cv.drawCentredString(page_width / 2, page_height - font_size * 4, title)

    draw_marker(cv, page_width / 2, page_height / 2, number, size)

    packet.seek(0)
    with open(filename, 'wb') as f:
        f.write(packet.getvalue())
    f.close()
    packet.close()


if __name__ == "__main__":
    main()