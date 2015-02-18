# Framemarker-Generator

In Chapter 2 of [Mastering OpenCV with Practical Computer Vision Projects][0] there is a framemarker that is used with the project. However, if you want to track multiple framemarkers with different values or change their size.

I wrote this python script to generate PDFs of the framemarkers with all values between 0-1023. You can also change the size of the marker from 7cm to something bigger or smaller depending on your needs.

## About the framemarker

The framemarkers use a modified hamming code comprised of 5 codewords, each 5-bits long. Each word carries only 2 data bits. Hence the reason there are only 1024 possible markers. The 4 valid codewords are below:

    1 0 0 0 0,
    1 0 1 1 1,
    0 1 0 0 1,
    0 1 1 1 0

1s are white, 0s are black. The data bits are in columns 2 and 3.

[0]: https://www.packtpub.com/application-development/mastering-opencv-practical-computer-vision-projects
