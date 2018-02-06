"""
Topic: detecting stickers (vignettes, stickers from LEZ zones ets.) on cars' windshields
"""
# -*- coding: utf-8 -*-

# import numpy as np
import cv2


def main():
    # Read from file
    cap = cv2.VideoCapture('video/test1.mp4')

    while cap.isOpened():
        ret, frame = cap.read()

        [cars] = find_cars(frame)
        for car in cars:
            windshield = find_windshield(frame, car)
            license_plate = find_license_plate(car)
            match_stickers(windshield, license_plate)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# TODO 2: odnajdywanie aut jadących przodem do kamery
def find_cars(frame):
    # TODO 2a: processing wielu aut na raz -> w wątkach czy jedno po drugim?
    # TODO 2b: czy procesować tylko z jednego "regionu", tak żeby nie powtarzać processingu tego samego auta?
    return True


# TODO 3: znajdywanie szyby na aucie
def find_windshield(frame, car):
    new_pic = calibrate_picture(frame, car)
    return new_pic


def find_license_plate(car):
    return car


# TODO 4: przeskalowanie szyby tak aby była prostokątem a nie pod kątem
def calibrate_picture(frame, car):
    return frame


def match_stickers(windshield, license_plate):
    stickers, locations = find_stickers(windshield)
    for idx in range(1, len(stickers)):
        is_valid_sticker = validate_sticker(stickers[idx], locations[idx])
        if is_valid_sticker:
            is_valid_number = validate_license_plate(stickers[idx], license_plate)
            if not is_valid_number:
                remember_license_plate(license_plate)
        else:
            remember_license_plate(license_plate)


# TODO 5: znajdywanie wszystkich naklejek na szybie
def find_stickers(windshield):
    return [], []


# TODO 6: dopasowywanie naklejek do znanych obrazków: winiet, naklejek z LEZ, naklejek tych w PL z numerem tablicy
def validate_sticker(sticker, location):
    # TODO 6a: dobra najlejka w dobrym miejscu
    # TODO 6b: dobra naklejka w złym miejscu
    # TODO 6c: brak danej naklejki
    # TODO 6d: coś oszukańczego na szybie co udaje naklejke
    # TODO 6e: naklejka przestarzała
    return True


# TODO 7: sprawdzanie czy zgadza się numer z tablicą rejestracyjną (tu również porównywanie dwóch obrazków)
def validate_license_plate(sticker, license_plate):
    # TODO 7a: okej, zgadza się
    # TODO 7b: zły numer
    return True


# TODO 8: jeśli coś jest nie tak, to zapamiętywanie tablicy rejestracyjnej
def remember_license_plate(license_plate):
    pass


if __name__ == '__main__':
    main()
