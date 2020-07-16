class MultiSaberLegacy:

#https://code.tutsplus.com/tutorials/professional-error-handling-with-python--cms-25950
	#private - should not be available to user
	MOTOR1 = 0
	MOTOR2 = 4

	uartMsg = "" # initalize empty uart Msg

	def __init__(self, addresses):
		self.addresses = addresses
		#self.enableFailsafe = enableFailsafe			

	def driveMotors(self, speeds):
		self.uartMsg = "" # reset uart msg buffer

		lenOfSabers = len(self.addresses)

		lenOfSpeeds = len(speeds)

		nOfSabersEqualSpeeds = lenOfSabers * 2 != lenOfSpeeds
		nOfSabers1EqualSpeeds = lenOfSabers * 2 - 1 != lenOfSpeeds

		print(nOfSabersEqualSpeeds)
		print(nOfSabers1EqualSpeeds)

		if nOfSabersEqualSpeeds ^ nOfSabers1EqualSpeeds:

			for isaber, address in enumerate(self.addresses): # for each sabertooth

				# are we on the last sabertooth?
				notLastSaber = lenOfSabers - 1 != isaber

				# is there an even number of motors to control?
				evenNumOfMotors = lenOfSpeeds % 2 == 0

				if notLastSaber or evenNumOfMotors:
					availableMotors = 2
				else:
					availableMotors = 1 

				for imotor in range(availableMotors):
					if imotor == 0:
						motorCommand = self.MOTOR1
					else:
						motorCommand = self.MOTOR2
						
					cmdData = self.speedToCmd(speeds[(isaber * 2) + imotor], motorCommand)

					print("Address: " + str(address) + "\n")
					
					command = cmdData.get("command")
					print("Command: " + str(command) + "\n")

					data = cmdData.get("data")
					print("Data: " + str(data) + "\n")

					checksum = self.checksum(address, command, data)
					print("Checksum: " + str(checksum) + "\n" + "----------------------")

					self.uartMsg += str(address) + str(command) + str(cmdData.get("data")) + str(checksum)
	                                

			# python write uart message
			print("END___________________________________________")
			return bytes(bytearray(self.uartMsg, "utf-8"))
			#return self.uartMsg.encode()

		else: # Mismatch too many or too litte motor speeds for the amount of sabertooths to control

			#if enableFailsafe:
			#	pass



			print("Mismatch of Motors to control compared to available Sabertooths")
	def speedToCmd(self, speed, motorCmd): # take [-1.0, 1.0] speeds to command, data parameters
		# motor should be either 1 or 2
		# speed is a float in range [-1.0, 1.0]

		# we know which motor to control, need to figure out which 
		# direction command to send

		if speed > 0:
			command = motorCmd
		else:
			command = motorCmd + 1

		data = int(abs(speed) * 127)

		return {"command":command, "data":data}

	def checksum(self, address, command, data):
		return (address + int(command) + int(data)) & 0b01111111

import serial
import time

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)


#https://pyserial.readthedocs.io/en/latest/pyserial_api.html
instance = MultiSaberLegacy([128, 129])

serial_port.write(instance.driveMotors([-0.2, 0.3, 0.2, -0.1]))

time.sleep(5)

serial_port.write(instance.driveMotors([0, 0, 0, 0]))

serial_port.close()
