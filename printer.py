import numpy as np
import StringIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

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
    # Back up to bottom, left-hand corner
    x -= (size / 2)
    y -= (size / 2)

    # Divide the region into 7 sub-squares
    square_size = size / 7

    # Set the color to black for stroke and fill
    cv.setStrokeColorRGB(0.0, 0.0, 0.0)
    cv.setFillColorRGB(0.0, 0.0, 0.0)

    # Get the codewords for the number
    message = np.array(list(convert_to_codeword(convert_to_binary_list(number, 10))))

    # Draw a thin outline
    cv.rect(x - (square_size / 2), y - (square_size / 2), size + square_size, size + square_size, 1)

    # Draw a black box inside
    cv.rect(x, y, size, size, 1, 1)

    start_x = x + square_size
    start_y = y + square_size
    # Change the color to white for stroke and fill
    cv.setStrokeColorRGB(1.0, 1.0, 1.0)
    cv.setFillColorRGB(1.0, 1.0, 1.0)
    for column in range(0, 5):
        for row in range(0, 5):
            if message[4 - column, row] == 1:
                x_offset = (square_size * row)
                y_offset = (square_size * column)
                cv.rect(start_x + x_offset, start_y + y_offset, square_size, square_size, 1, 1)

def main():
    author = 'Cameron Lowell Palmer'
    catalog = True
    pagesize = A4
    number = 213
    size = 5
    font_size = 24
    font_name = 'Helvetica'

    packet = StringIO.StringIO()

    cv = canvas.Canvas(packet, pagesize)
    page_width, page_height = pagesize
    if catalog:
        title = 'Framemarker Catalog'
        filename = 'catalog.pdf'
        size = 2 * cm
        padding = 2 * cm
        padded_size = size + padding
        x = 0
        y = page_height
        columns_per_page = int(page_width / padded_size)
        rows_per_page = int(page_height / padded_size)
        for number in range(0, 1024):
            current_column = number % columns_per_page
            current_row = number / columns_per_page

            page_row = current_row % rows_per_page
            x_offset = (current_column * padded_size) + (padded_size / 2)
            y_offset = (page_row * padded_size) + (padded_size / 2)

            if current_row > 0 and current_column == 0 and page_row == 0:
                cv.showPage()

            draw_marker(cv, x + x_offset, y - y_offset, number, size)
            cv.setFont(font_name, 8)
            cv.setFillColorRGB(0.0, 0.0, 0.0)
            cv.drawCentredString(x + x_offset, y - y_offset - (padded_size / 2) + 8, str(number))
    else:
        filename = 'marker_%04d.pdf' % number
        title = 'Marker %d - %d cm' % (number, size)
        cv.setFont(font_name, font_size)
        cv.drawCentredString(page_width / 2, page_height - font_size * 4, title)
        draw_marker(cv, page_width / 2, page_height / 2, number, size)

    cv.setAuthor(author)
    cv.setTitle(title)

    cv.save()
    packet.seek(0)
    with open(filename, 'wb') as f:
        f.write(packet.getvalue())
    f.close()
    packet.close()


if __name__ == "__main__":
    main()
