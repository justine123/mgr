"""
Topic: Detecting stickers (vignettes, stickers from LEZ zones ets.) on cars' windshields
"""
# -*- coding: utf-8 -*-

# import cv2
from main import *


def test_stickers_detection(windshield_testing_enabled):
    """
    Test stickers detection and validation, possible to test windshield detection too
    :param windshield_testing_enabled: enabled windshield detection testing
    :return: True/False, depending on algorithm correctness (should return True, if algorithm works)
    """
    if windshield_testing_enabled:
        car = 'images/car1.jpg'
        windshield = find_windshield(car)
    else:
        windshield = 'images/test_windshield1.jpg'

    stickers = find_stickers(windshield)
    # Validate number of detected stickers
    if len(stickers != 1):
        print("Test failed - there is only 1 sticker in this scenario, but " + str(len(stickers)) + " were detected!!!")
        return False

    # Validate sticker properties - type and location
    sticker = stickers[0]
    if sticker.type != 'registration':
        print("Test failed - this is a registration sticker, but was recognised as " + sticker.type + " !!!")
        return False

    if sticker.location != 'bottom left':
        print("Test failed - this sticker is located in bottom left corner of the windshield, but was recognised as in "
              + sticker.location + " corner!!!")
        return False

    # Check if all the stickers were marked as valid
    is_valid_sticker = validate_sticker(stickers)
    if not is_valid_sticker:
        print("Test failed - all the stickers in this scenario are valid, but were recognised as invalid!!!")
        return False


if __name__ == '__main__':
    test_stickers_detection(windshield_testing_enabled=False)
