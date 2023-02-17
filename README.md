# Delta-Robot-Toothbrush-Detector

This repository contains a code developed using OpenCV for identifying toothbrushes on a conveyor belt and outputting their coordinates and angles. The code uses OpenCV's inbuilt functionalities for image processing and object detection, allowing it to process grayscale images and draw contours around the toothbrushes.

The toothbrush information is used to control the movement of a delta robot through inverse kinematics. To accomplish this, the code uses principal component analysis to calculate the centroid and angle of each toothbrush. However, the orientation of the toothbrush can change, causing issues with determining its external angle. To address this, the code uses template matching to identify the toothbrush's head and correct the polarity of its angle.

Additionally, the code includes a calibration model to convert pixel coordinates to millimeters and ensure accurate movement of the delta robot. This model is automated using OpenCV to measure the pixel length of a known box and calculate the conversion factor. Overall, this code provides an efficient solution for toothbrush identification and control of a delta robot.


<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562388-59ed1b65-bc34-4d5d-b179-7cb7ed465017.png">

<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562461-490ce308-1e5c-4e43-9b4f-ddcf15c444fc.png">

<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562575-293ca591-d03f-4d57-a779-40fdc883b0c4.png">

<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562587-fdb66a54-7caa-476c-89cb-e45015425b48.png">

<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562604-95a88466-5e28-4dcd-8d65-9853d271cda5.png">

<img width="200" alt="image" src="https://user-images.githubusercontent.com/121004983/219562640-089eed18-8da7-418f-9660-543d0a3ce728.png">


