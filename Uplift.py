#!/usr/bin/env python







import mraa
import time
import serial
import bluetooth
from mindwavemobile.MindwaveDataPoints import MeditationDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap

MEDITATION_HIGH_THRESHOLD = 65
MEDITATION_LOW_THRESHOLD = 63

HIGH_SPEED = 1400
LOW_SPEED = 1200


def readPacket():
	print(str(ser.read(1)))
	if False: #HIGH_SPEED==0xAA:
		if ser.read(1)==0xAA:
			print("Received Packet")
			payloadLength=ser.read(1)
			if payloadLength>169:
				return
			for i in range(payloadLength):
				payloadData[i] = ser.read(1)
			checksum=ser.read(1)
			genChecksum=0
			for i in range(payloadLength):
				genChecksum=genChecksum+payloadData[i]
				genChecksum=genChecksum&0x000000FF
			genChecksum=0xFF-genChecksum
			if genChecksum==checksum:
				print("Passed Checksum")
				for i in range(payloadLength):
					if payloadData[i]==0x05:
						meditation=payloadData[i+1]
						return meditation
					if payloadData[i]==0xD2:
						ser.write("AUTOCONNECT")
						return meditation
	return 0

def updateFan(meditate):
	print meditate
	if meditate>MEDITATION_HIGH_THRESHOLD:
		servo.pulsewidth_us(HIGH_SPEED)
		#ser.write(chr(HIGH_SPEED))
		#print "High"
	elif (meditate<MEDITATION_LOW_THRESHOLD)&(meditate>0):
		servo.pulsewidth_us(LOW_SPEED)
		#ser.write(chr(LOW_SPEED))
		#print "Low"
	elif meditate==0:
		servo.pulsewidth_us(1000)
		#print "Zero"
	return

if __name__ == '__main__':
	print "Init Servo"
	servo = mraa.Pwm(3)
	servo.period_us(15000)
	servo.pulsewidth_us(1000)
	servo.enable(True)
	x=mraa.Uart(0)
	ser = serial.Serial('/dev/ttyMFD1',115200)
	fanval=127
	ser.write("AUTOCONNECT")
	#ser.write(chr(fanval))
	print "Finding Mindwave"
	#mindwaveDataPointReader = MindwaveDataPointReader()
	#mindwaveDataPointReader.start()
	if True: #(mindwaveDataPointReader.isConnected()):
		print "Mindwave Connected"
		while True:
			updateFan(readPacket())
			#dataPoint = mindwaveDataPointReader.readNextDataPoint()
			#if (dataPoint.__class__ is MeditationDataPoint):
			#	time.sleep(0.5)
			#	fanval+=1
			#	updateFan(dataPoint.MeditationValue)
			#	if fanval>80:
			#		fanval=50



