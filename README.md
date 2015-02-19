# Framemarker-Generator

In Chapter 2 of [Mastering OpenCV with Practical Computer Vision Projects][0] there is a framemarker that is used with the project. However, only one marker (value 213) is provided in PNG format. If you want to track multiple framemarkers with different values or change their size you have to write your own tool.

I wrote this python script to generate PDFs of the framemarkers with all values between 0-1023. You can also change the size of the marker from 7cm to something bigger or smaller depending on your needs. 

## About the framemarker

![Framemarker 213](marker_213.png?raw=true "Disco shoe")

The framemarkers use a modified hamming code comprised of 5 codewords, each 5-bits long. Each word carries only 2 data bits. Hence the reason there are only 1024 possible markers. The 4 valid codewords are below:

    1 0 0 0 0,
    1 0 1 1 1,
    0 1 0 0 1,
    0 1 1 1 0

1s are white, 0s are black. The data bits are in columns 2 and 3. The one provided in the book is the number 213 and the printed version is 7x7 centimeters.

If you're interested in trying out their code you should buy the book and download the [source code][1].

[0]: https://www.packtpub.com/application-development/mastering-opencv-practical-computer-vision-projects
[1]: https://github.com/MasteringOpenCV/code
