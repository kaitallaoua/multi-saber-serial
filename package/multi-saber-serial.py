class MultiSaberLegacy:


	#private - should not be available to user
	MOTOR1 = 0
	MOTOR2 = 4

	uartMsg = "" # initalize empty uart Msg



	def __init__(self, addresses, baudrates):
		self.addresses = addresses
		self.baudrates = baudrates		

	def driveMotors(self, speeds):
		self.uartMsg = "" # reset uart msg buffer

		for isaber, address in enumerate(self.addresses): # for each sabertooth

			# are we on the last sabertooth?
			notLastSaber = len(self.addresses) - 1 != isaber

			# is there an even number of motors to control?
			evenNumOfMotors = len(speeds) % 2 == 0

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

				checksum = (address + int(command) + int(data)) & 0b01111111
				print("Checksum: " + str(checksum) + "\n" + "----------------------")

				self.uartMsg += str(address) + str(command) + str(cmdData.get("data")) + str(checksum)
                                

		# python write uart message
		return bytearray(self.uartMsg, "utf-8")




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

import serial
#https://pyserial.readthedocs.io/en/latest/pyserial_api.html
instance = MultiSaberLegacy([128, 129, 130], [115200])

print(instance.driveMotors([-0.4, 0.3, 0.4, -0.9, 1.0, 0.2]))


