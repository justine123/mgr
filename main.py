"""
Topic: Detecting stickers (vignettes, stickers from LEZ zones ets.) on cars' windshields
"""
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
# from matplotlib import pyplot as plt
# import numpy as np
import cv2


def main():
    """
    Main function, that detects cars on a video, then detects a front windshield of each car and finds + validates all
    the stickers on a windshield
    """
    # Read from file
    cap = cv2.VideoCapture('videos/video.avi')

    while cap.isOpened():
        ret, frame = cap.read()

        cars = find_cars(frame)
        for car in cars:
            windshield = find_windshield(car)
            # license_plate = find_license_plate(car)
            stickers = find_stickers(windshield)
            is_valid_sticker = validate_sticker(stickers)
            if is_valid_sticker:
                print("All the stickers in this car are valid!")
                # TODO: validate stickers with license plate and remember the number if something is wrong
                # is_valid_number = validate_license_plate(stickers, license_plate)
                # if not is_valid_number:
                #     remember_license_plate(license_plate)
            #     pass
            else:
                print("Invalid stickers!!!")
            #     remember_license_plate(license_plate)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def find_cars(frame):
    """
    Find cars in a video frame, thanks to cars.xml classifier
    :param frame: video frame
    :return: cars_array - array with cars' images
    """
    # TODO 2: odnajdywanie aut jadących przodem do kamery
    # TODO 2a: processing wielu aut na raz -> w wątkach czy jedno po drugim?
    # TODO 2b: co zrobić, żeby nie powtarzać processingu tego samego auta?
    # based on https://www.geeksforgeeks.org/opencv-python-program-vehicle-detection-video-frame/
    cars_array = []

    # Trained XML classifiers describes some features of some object we want to detect
    car_cascade = cv2.CascadeClassifier('cars.xml')
    # convert to gray scale of each frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detects cars of different sizes in the input image
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    # To draw a rectangle in each cars
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cars_array.append(frame[y:y+h, x:x+w])  # cut the piece with the car and add it to array with cars

    # Display frames in a window
    cv2.imshow('video2', frame)
    return cars_array


# TODO 3: znajdywanie szyby na aucie
def find_windshield(car):
    new_pic = calibrate_picture(car)
    return new_pic


# TODO 4: przeskalowanie szyby tak aby była prostokątem a nie pod kątem
def calibrate_picture(frame, car):
    return frame


def find_stickers(windshield):
    """
    Finds all the stickers in an image, by finding defined templates on it.
    :param windshield: windhield image
    :return: detected_stickers - list of dictionaries, each dict contains sticker parameters: image, type of sticker
    (LEZ, vignette, sticker type) and its location (for further validation)
    """
    # https://docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
    detected_stickers = []
    # locations = []
    img = windshield
    img2 = img.copy()
    height, width = img.shape
    templates = []
    sticker_types = []
    path_to_templates = 'stickers/'
    files = [f for f in listdir(path_to_templates) if isfile(join(path_to_templates, f))]
    for n in range(0, len(files)):
        templates[n] = cv2.imread(join(path_to_templates, files[n]))
        if files[n].find('lez'):
            sticker_types.append('lez')
        elif files[n].find('vignette'):
            sticker_types.append('vignette')
        elif files[n].find('registration'):
            sticker_types.append('registration')
        else:
            print("Invalid picture type: ", files[n])

    # All the 6 methods for comparison in a list
    # methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    # Match picture with all the possible stickers
    for n in range(0, len(templates)):
        template = templates[n]
        img = img2.copy()
        method = 'cv.TM_CCOEFF'

        # Apply template Matching
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #     top_left = min_loc
        # else:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # h, w, c = template.shape

        if (top_left[1] + h)/height < 0.5:
            if (top_left[0] + w)/width < 0.5:
                location = 'top left'
            else:
                location = 'top right'
        else:
            if (top_left[0] + w)/width < 0.5:
                location = 'bottom left'
            else:
                location = 'bottom right'

        if min_val < h * w * 3 * (20 * 20):
            cv2.rectangle(img, top_left, bottom_right, 255, 2)
            detected_stickers.append({'img': img[top_left[0]:top_left[0] + w, top_left[1]:top_left[1] + h],
                                      'type': sticker_types[n], 'location': location})
    return detected_stickers


def validate_sticker(detected_stickers):
    """
    Validation - checking if stickers are in proper locations + if each car has a mandatory registration sticker
    :param detected_stickers: array with all the stickers in a car
    :return: True/False, depending on validation result
    """
    # TODO 6d: coś oszukańczego na szybie co udaje naklejke
    # TODO 6e: naklejka przestarzała
    passed = 0
    has_registration_sticker = False

    # Check if every sticker is in correct location
    for sticker in detected_stickers:
        if sticker.type == 'lez' or sticker.type == 'vignette':
            if sticker.location == 'top left':
                passed += 1
            else:
                print("Wrong " + sticker.type + " sticker location - should be in top left corner, but is in " +
                      sticker.location)

        if sticker.type == 'registration':
            has_registration_sticker = True
            if sticker.location == "bottom left":
                passed += 1
            else:
                print("Wrong registration sticker location - should be in top left corner, but is in " +
                      sticker.location)

    # Registration sticker is mandatory in this scenario-
    if not has_registration_sticker:
        return False

    # Each sticker must be valid
    if passed == len(detected_stickers):
        return True
    else:
        return False


# def find_license_plate(car):
#     return car


# TODO 7: sprawdzanie czy zgadza się numer z tablicą rejestracyjną (tu również porównywanie dwóch obrazków)
# def validate_license_plate(sticker, license_plate):
#     # TODO 7a: okej, zgadza się
#     # TODO 7b: zły numer
#     return True


# TODO 8: jeśli coś jest nie tak, to zapamiętywanie tablicy rejestracyjnej
# def remember_license_plate(license_plate):
#     pass


if __name__ == '__main__':
    main()
