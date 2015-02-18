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

def generate_marker(number):
    filename = 'marker_%04d.pdf' % number
    title = 'Marker %d' % number
    image_size = 7 * cm

    packet = StringIO.StringIO()
    cv = canvas.Canvas(packet, pagesize=A4)

    font_size = 24
    page_width, page_height = A4
    cv.setFont('Helvetica', font_size)
    cv.drawCentredString(page_width / 2, page_height - font_size * 4, title)

    square_size = image_size / 7
    start_x = (page_width / 2) - (image_size / 2)
    start_y = (page_height / 2) - (image_size / 2)
    cv.setStrokeColorRGB(0.0, 0.0, 0.0)
    cv.setFillColorRGB(0.0, 0.0, 0.0)
    message = np.array(list(convert_to_codeword(convert_to_binary_list(number, 10))))
    cv.rect(start_x - (square_size / 2), start_y - (square_size / 2), image_size + square_size, image_size + square_size, 1)
    cv.rect(start_x, start_y, image_size, image_size, 1, 1)

    start_x += square_size
    start_y += square_size
    cv.setStrokeColorRGB(1.0, 1.0, 1.0)
    cv.setFillColorRGB(1.0, 1.0, 1.0)
    for column in range(0, 5):
        for row in range(0, 5):
            x = start_x + (square_size * row)
            y = start_y + (square_size * column)
            if message[4 - column, row] == 1:
                cv.rect(x, y, square_size, square_size, 1, 1)

    cv.save()

    packet.seek(0)
    with open(filename, 'wb') as f:
        f.write(packet.getvalue())
    f.close()
    packet.close()

def main():
    generate_marker(213)

if __name__ == "__main__":
    main()