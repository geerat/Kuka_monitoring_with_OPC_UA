# README
#
# This is the source code for the client assignment. Make sure to work on your individual files
#
# Work you have to do is clearly marked by TODO. Otherwise please do not change the code.
#
# Read through the (commented) code and try to understand it.

# Module to get current time
from datetime import datetime

# Module to slow down loop
from time import sleep

# Module to write downloaded data to file
import csv

# OPC UA module, we use the client
import opcua

if __name__ == "__main__":

    # Assemble server endpoint/URL
    ep_protocol = "opc.tcp"  # OPC UA protocol
    ep_ip = "localhost"  # do not change, localhost
    ep_port = "____"  # TODO: chose the port of your OPC UA server
    # TODO: add your group number. Path on the server where the address space is accesible. One server can host multiple address spaces
    ep_path = "freeopcua/server/group____"
    endpoint = ep_protocol+"://"+ep_ip+":" + \
        ep_port+"/"+ep_path  # assemble the string

    # Create instance for client and pass the endpoint
    client = opcua.Client(endpoint)

    try:
        # Connect to server
        print("Connecting to: "+endpoint)
        connected = False
        while (not connected):
            try:
                client.connect()
                connected = True
            except:
                sleep(1)
        print("Connected")

        # Get the root node of the adress space
        objects_node = client.get_objects_node()

        # TODO: Start the opcua-modeler and inspect the XML file.
        # Get 'Axis_Act' node
        # 'Axis_Act' is the robot's position. It is an array with 7 elements. 6 robot axes and 1 linear track.
        axis_act = ____  # TODO get reference to the 'Axis_Act' node

        # Get controller node
        controller_node = ____  # TODO get reference to the 'controller' node

        # Get status node
        controller_status = ____  # TODO get reference to the 'status' node

        print("Linked adress space nodes to code")

        # Call the load method on the controller node. Pass the program name as a parameter
        return_value = controller_node.call_method("0:Load", 'step1_1.src')
        print("Sent command to load program")
        if return_value == False:
            print('Could not load program')
            assert(False)
        else:
            print('Succesfully loaded program')

        # Call the start method on the controller
        # TODO call 'Start' method on the controller node
        ____
        print("Sent Start command")

        # Create a new CSV file where the data will be logged
        # TODO add your group number to the file name
        with open('EMCO_LoggedData_Group_XX__.csv', 'w', newline='') as csvfile:
            # Configure how to write to the CSV file
            datalogger = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # Write the header of the CSV file
            # TODO give meaningful names for columnheaders. The columns will be: current time, one column per element in the 'axis_act' array, controller status
            datalogger.writerow(["___", "__0__", "__1__", "__2__", "__3__", "__4__", "__5__", "__6__", "____"])

            print("About to start logging data")

            # Log data as long as the controller status is not stopped i.e. the machine is running
            while controller_status.get_value() == "Running":
                # Log every 10 ms
                sleep(0.01)
                # Log the machine data to the CSV file
                row_array = [datetime.now().strftime('%D %H:%M:%S.%f')[:-3]]
                axis_acts_value = axis_act.get_value()
                if axis_acts_value != None and axis_acts_value != 'unavailable':
                    for axis in axis_acts_value:
                        row_array.append(axis)
                    # TODO: Get the value of the 'Status' node
                    node_status_value = ___
                    row_array.append(node_status_value)
                    datalogger.writerow(row_array)

            print("Finished logging data")

    finally:

        # Disconnect from server
        client.disconnect()
        print("Disconencted from server")
