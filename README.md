Master's thesis by Justyna Handzlik
===================================
This program detects stickers (like vignettes or stickers from LEZ zones) on cars' windshields.

# Installation
    git clone git@github.com:justine123/mgr.git 
    pip install -r requirements.txt

# Usage
In `main()` function, choose a video from folder `video` and type it into the following line: \
`cap = cv2.VideoCapture('video/filename.mp4')`. \
Next, run the program.

# How it works
## Camera configuration
A single camera has the following attributes:
- ...

## Car detection
In while loop, cars are detected, thanks to `cars.xml` classifier. 
The program is only looking for the cars with front windshield visible.

## Windshield detection and calibration
In the next step, front windshield of each car is detected and calibrated, in order to get rectangular shape.

## Finding stickers
On the windshield, program detects all the stickers and compares them to the ones in the database. 
Next, it validates the stickers' locations.

## Checking license plate
If the program finds a sticker with a number, it is compared with the car's license plate.

## Possible outcomes
Validating stickers can have a few different outcomes:
- correct sticker in correct place,
- correct sticker in incorrect place,
- no sticker, that should be there,
- something that looks like sticker, but is not a sticker (cheating!),
- outdated sticker,
- wrong license plate number on a sticker.

## Memorizing license plate
If there is something wrong with the car's stickers, its license plate number is saved into database.
