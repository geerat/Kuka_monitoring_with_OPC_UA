# README
#
# This is the source code for the server assignment. Make sure to work on your individual files
#
# Work you have to do is clearly marked by TODO. Otherwise please do not change the code.
#
# Read through the (commented) code and try to understand it.

from time import sleep


# import OPC UA library
#from opcua import ua, uamethod, Server
import opcua

# This class connects to the (simulated) KUKA KR10 robot. You need to use it in order to prove your completion of the assignment
from kukabridge import KUKABridge

# Pre-declare global instance of kukabridge
kuka = 0

# Main method of this program (executed after this sourcefile is loaded)


def main():

    # create instance/object of type opcua.Server
    myserver = opcua.Server()
    print("Server instance created")

    # create instance of kukacontroller with unique identifier
    global kuka  # use kuka as a global variable
    kuka=KUKABridge("5915524839") # do not change!
    print("KUKA Bridge instance created")

    # Load XML model into server
    # TODO: find the method to 'import' nodes defined in 'XML'. to find it check the documentation https://python-opcua.readthedocs.io/en/latest/server.html
    # TODO: In the line below replace the underscores with the method you found earlier. This will call the method from the myserver object.
    # TODO: As the fuction argument provide the path/name of the XML file you were given
    myserver.____("____")
    print("Adress space model imported into server")

    # Assemble server endpoint/URL
    ep_protocol = "opc.tcp"  # OPC UA protocol
    ep_ip = "localhost"  # do not change, localhost    
    ep_port = "____" # TODO: chose a free unblocked port (for the assignment chose a random number between 9000 and 10000)    
    ep_path = "freeopcua/server/group___" # TODO: add your group number. Path on the server where the address space is accesible. One server can host multiple address spaces
    endpoint = ep_protocol+"://"+ep_ip+":" + \
        ep_port+"/"+ep_path  # assemble the string

    # Set endpoint for address space on the server
    myserver.set_endpoint(endpoint)

    # Get reference to the Objects node of the server.
    # TODO: start the 'opcua-modeler' software as outlined in the assignment documents.
    # TODO: open the provided XML to inspect it, so you can understand how the address space is navigated and references to nodes obtained
    objects = myserver.get_objects_node()

    # Get references to the robot and position nodes in the server
    node_kuka = objects.get_child("0:KUKA_KR10")
    # 'Axis_Act' is the robot's position. It is an array with 7 elements. 6 robot axes and 1 linear track.
    axis_act = node_kuka.get_child("0:Axis_Act")
    # There is no data from the KUKA controller available right now
    axis_act.set_value('unavailable')

    # Get reference to the controller node
    # TODO: Get a reference to the 'controller' node. Have a look at the previous four lines of code, and the address space in the xml file.
    node_controller = ____

    # Get reference to the status node
    machinestatus = ____  # TODO: Get a reference to the 'status' node
    ____  # TODO: Set the machinestatus to 'unavailable'

    print("OPC UA variable nodes linked against KUKA controller")

    # In the following callback function the value of the nodes will be updated with the data from the KUKA controller
    # Callback method that gets called when the KUKA controller has new axisdata
    def NewAxisData(axis_data, status):

        # Write position data from KUKA controller into OPC UA nodes
        axis_act.set_value(axis_data)
        machinestatus.set_value(status)

    # Register above callback method with the KUKA controller
    kuka.register_callback(NewAxisData)

    print("Callback with KUKA controller registered")

    # Get references to the OPC UA Controller methods
    controller_loadprogram = ____  # TODO get reference to 'Load' method node
    controller_start = ____  # TODO get reference to 'Start' method node
    controller_stop = ____  # TODO get reference to 'Stop' method node

    # Link OPC UA methods with Python methods
    myserver.link_method(controller_loadprogram, LoadProgram)
    ____.(____, Start)  # TODO add code to link start method
    ____.(_____, Stop)  # TODO add code link stop method

    print("OPC UA methods nodes linked against KUKA controller")

    # starting! The server will continue running
    myserver.start()
    print("Server up and running")


# Methods to execute when an OPC UA client calls a method on the OPC UA server

# Method to load program
@opcua.uamethod
def LoadProgram(parent, path):
    print("Calling load program")
    if kuka.LoadProgram(path):
        result = True
    else:
        result = False
    return result

# Method to start/execute loaded program
@opcua.uamethod
def Start(parent):
    print("Calling start prgram")
    kuka.____  # TODO call 'Start' method on KUKA Bridge
    sleep(0.05)
    result = True
    return result

# Method to stop exectuion
@opcua.uamethod
def Stop(parent):
    print("Calling stop prgram")
    kuka.Stop()
    result = "program stopped"
    return result


if __name__ == "__main__":
    main()
