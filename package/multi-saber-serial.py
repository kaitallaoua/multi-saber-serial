class MultiSaberLegacy:


	#private - should not be available to user
	MOTOR1 = 0
	MOTOR2 = 4

	uartMsg = "" # initalize empty uart Msg



	def __init__(self, addresses, baudrates):
		self.baudrates = baudrates
		self.addresses = addresses

	def driveMotors(self, speeds):
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
				





	def speedToCmd(self, speed, motor): # take [-1.0, 1.0] speeds to command, data parameters
		# motor should be either 1 or 2
		# speed is a float in range [-1.0, 1.0]

		# we know which motor to control, need to figure out which 
		# direction command to send
		if speed > 0:
			command = self.MOTOR1
		else:
			command = self.MOTOR




