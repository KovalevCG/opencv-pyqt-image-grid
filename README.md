# Application for combining multiple images into 1 file.
<br/>
It is very common for a 3D artist to compose several images and put them on Trello so that the Lead Artist can comment or accept the 3D model. Usually this is done in Photoshop, but Photoshop is not very suitable for these tasks.
I wrote an application that makes it very easy to compose multiple images. The application is written in Python using the PyQt and OpenCV libraries.

<br/><br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/screenshot_01.jpg)

<br/>

The application automatically calculates the optimal resolution based on the resolution of the incoming images.
It also extends the image using the border color of the image if the incoming image is too small.
The layout of two or four images is currently supported.


App allows to upload images in two ways, using drag and drop of premade screenshots:

<br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/Image_Grid_dragNdrop_02.gif)

<br/>

and a faster way that allows not to create unnecessary files - creating new screenshots inside app:

<br/>

![](https://raw.githubusercontent.com/KovalevCG/opencv-pyqt-image-grid/master/Gifs/Image_Grid_screenshot.gif)

<br/>
