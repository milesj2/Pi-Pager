print("Importing")
import pyzbar.pyzbar as pyzbar
print("Importing2")
import cv2


print("Imports finished")

image = cv2.imread("test-qrcode.png")

print("Image read")

decodedObjects = pyzbar.decode(image)

print("Image decoded")

for obj in decodedObjects:
    print("Type:", obj.type)
    print("Data: ", obj.data, "\n")
