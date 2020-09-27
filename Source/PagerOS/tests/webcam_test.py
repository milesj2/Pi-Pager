import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN


def scan():
    while True:
        _, frame = cap.read()

        decoded_objects = pyzbar.decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            print("Found data:", data)
            if data[0: 7] == "WIFI:S:":
                return data

            #cv2.putText(frame, str(obj.data), (50, 50), font, 2,
            #            (255, 0, 0), 3)

        # cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break


def main():
    wifi_info = scan()
    wifi_info = "WIFI:S:MeinTurtle;T:WPA;P:**332333*8867villaine;H:false;;"
    print("Found wifi info:", wifi_info)
    print("\n")
    test = wifi_info.split(';')
    ssid = test[0].split(':')[2]
    encryption = test[1].split(':')[1]
    password = test[2].split(':')[1]
    print("SSID:", ssid)
    print("Encryption:", encryption)
    print("Password:", password)
    print("Connecting to wifi...")

    # scheme = wifi_manager2.SchemeWPA('wlp8s0', ssid,
    #                                 {"ssid": ssid, "psk": password})
    #print(scheme.activate())


if __name__ == "__main__":
    main()

