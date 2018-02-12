"""
Topic: Detecting stickers (vignettes, stickers from LEZ zones ets.) on cars' windshields
"""
# -*- coding: utf-8 -*-

from main import *


def test_cars_detection(video, num_cars):
    detection_threshold = 0.8  # let's say, if at least 80% of cars are recognised, test is passed
    cars = []
    cap = cv2.VideoCapture(video)

    while cap.isOpened():
        try:
            ret, frame = cap.read()

            cars = find_cars(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(str(e))
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(cars) != num_cars:
        if (len(cars) / num_cars) < detection_threshold:
            print("Test failed - on this video there are %d cars, but %d were detected!" % (num_cars, len(cars)))
            return False
        else:
            print("On this video there are %d cars, %d were detected, but it's still above the threshold!"
                  % (num_cars, len(cars)))

    return True


def run_all_car_detection_tests():
    results = []
    passed = 0
    # Scenario 1 - 'videos/video.avi', 10 cars on the video
    results.append(test_cars_detection(video='videos/video.avi', num_cars=10))

    for i in range(0, len(results)):
        print(results)
        if results[i]:
            print("Testcase ", i, " passed!")
            passed += 1
        else:
            print("Testcase ", i, " failed!")

    if passed == len(results):
        print("All tests passed!!!")
    else:
        print("%d / %d testcases failed!" % (passed, len(results)))


def test_stickers_and_windshield_detection(windshield_testing_enabled, img, num_stickers, stickers_types,
                                           stickers_locations):
    """
    Test stickers detection and validation, possible to test windshield detection too
    :param windshield_testing_enabled: whether to test windshield detection too
    :param img: path to image
    :param num_stickers: number of stickers on given image
    :param stickers_types: types of stickers on given image (LEZ, vignette, registration sticker)
    :param stickers_locations: locations of stickers on given image (top/bottom left/right)
    :return: Pass/Fail
    """
    if windshield_testing_enabled:
        print("Test stickers detection with windshield testing enabled")
        car = cv2.imread(img, 0)
        windshield = find_windshield(car)
    else:
        print("Test stickers detection with windshield testing disabled")
        windshield = cv2.imread(img, 0)

    stickers = find_stickers(windshield)

    # Validate number of detected stickers
    if len(stickers) != num_stickers:
        print("Test failed - there is only 1 sticker in this scenario, but " + str(len(stickers)) + " were detected!!!")
        return False

    # Validate sticker properties - type and location
    for sticker, sticker_type in zip(stickers, stickers_types):
        if sticker.type != sticker_type:
            print("Test failed - this is a registration sticker, but was recognised as " + sticker.type + " !!!")
            return False

    for sticker, location in zip(stickers, stickers_locations):
        if sticker.location != location:
            print("Test failed - this sticker is located in bottom left corner of the windshield, but was recognised "
                  "as in " + sticker.location + " corner!!!")
            return False

    # Check if all the stickers were marked as valid
    is_valid_sticker = validate_sticker(stickers)
    if not is_valid_sticker:
        print("Test failed - all the stickers in this scenario are valid, but were recognised as invalid!!!")
        return False


def run_all_stickers_tests():
    results = []
    passed = 0
    # Scenario 1 - 'test_car1.jpg', windshield detection enabled, one valid registration sticker in bottom left corner
    results.append(test_stickers_and_windshield_detection(windshield_testing_enabled=True,
                                                        img='images/car1.jpg',
                                                        num_stickers=1,
                                                        stickers_types=['registration'],
                                                        stickers_locations=['bottom left']))
    # Scenario 2 - 'test_car2.jpg', windshield detection enabled, no stickers
    results.append(test_stickers_and_windshield_detection(windshield_testing_enabled=True,
                                                        img='images/car2.jpg',
                                                        num_stickers=0,
                                                        stickers_types=[],
                                                        stickers_locations=[]))
    # Scenario 3 - 'test_windshield1.jpg', windshield detection disabled, 2 registration stickers in bottom left corner
    results.append(test_stickers_and_windshield_detection(windshield_testing_enabled=False,
                                                        img='images/test_windshield2.jpg',
                                                        num_stickers=2,
                                                        stickers_types=['registration', 'registration'],
                                                        stickers_locations=['bottom left', 'bottom left']))
    # Scenario 4 - 'test_windshield2.jpg', windshield detection disabled, one valid vignette in bottom left corner
    results.append(test_stickers_and_windshield_detection(windshield_testing_enabled=False,
                                                        num_stickers=1,
                                                        img='images/test_windshield2.jpg',
                                                        stickers_types=['vignette'],
                                                        stickers_locations=['bottom left']))
    # Scenario 5 - 'test_windshield3.jpg', windshield detection disabled, two valid lez stickers in bottom left corner
    results.append(test_stickers_and_windshield_detection(windshield_testing_enabled=False,
                                                        img='images/test_windshield3.jpg',
                                                        num_stickers=2,
                                                        stickers_types=['lez', 'lez'],
                                                        stickers_locations=['bottom left', 'bottom left']))
    for i in range(0, len(results)):
        if results[i]:
            print("Testcase ", i, " passed!")
            passed += 1
        else:
            print("Testcase ", i, " failed!")

    if passed == len(results):
        print("All tests passed!!!")
    else:
        print("%d / %d testcases failed!" % (passed, len(results)))


if __name__ == '__main__':
    run_all_car_detection_tests()
    # run_all_stickers_tests()
