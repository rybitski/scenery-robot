from RoboControl import RoboControl
from RoboNetwork import RoboNetwork

def main():
	control = RoboControl(DEBUG=True)
	network = RoboNetwork('192.168.1.2', 29281, 20, 5, DEBUG=True)
	
	controller_connected = False
	robot_connected = False
	
	controller_connected = control.connect()
	if controller_connected:
		print("Controller connected!")
		print("Starting controller program")
		control.start()
	else:
		print("No controller connected")
	
	#while not robot_connected:
	if not robot_connected:
		robot_connected = network.connect()
		if robot_connected:
			print("Robot connected")
		else:
			print("No robot detected, timeout")
		
	while (not control.exit):
		#if network.connected and len(control.commands) > 0:
		if len(control.commands) > 0:
			command = control.commands.popleft()
			print(command)
			if network.connected:
				network.conn.send(command[0])
				network.conn.send(command[1])
	network.exit = True
	
if __name__ == "__main__":
	main()