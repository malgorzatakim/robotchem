import picamera
from time import sleep

camera=picamera.PiCamera()
camera.capture("test1.png")
