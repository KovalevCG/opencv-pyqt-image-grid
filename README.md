# Application for combining multiple images into 1 file.
<br/>

The pipeline of the organization I currently work for implies that before sending images to the Lead Artist, images need to be combined. I realized that it’s possible to make a program that will do this much more efficiently than Photoshop and developed that app. The program was very well received and gradually some of the artists started offerring additional functionality that I implemented. Now my application is part of pipeline of the studio I am working in.

The application is written in Python using the PyQt and OpenCV libraries.

<!--
<br/><br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/screenshot_01.jpg)

<br/>
-->

<br/><br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/v1_1/3images.gif)

<br/>

The application automatically calculates the optimal resolution based on the resolution of the incoming images.
It also extends the image using the border color of the image if the incoming image is too small.
The layout of two or four images is currently supported.


App allows to upload images in two ways, using drag and drop of premade screenshots:

<!--
<br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/Image_Grid_dragNdrop_02.gif)

<br/>
-->

and a faster way that allows not to create unnecessary files - creating new screenshots inside app:

<!--
<br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/Image_Grid_screenshot.gif)

<br/>
-->
