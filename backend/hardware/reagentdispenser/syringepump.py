import time
import config
import serial
from hardware.reagentdispenser.base import ReagentDispenser

def grblWrite(grblSer, command):
    """
    Writes the given command to grbl. 

    :param grblSer:
    Serial device to write the command to

    :param command:
    String of grbl command to execute

    :return:
    None
    """
    grblSer.reset_input_buffer()
    grblSer.write(bytes(command, 'utf-8'))
    # Grbl will execute commands in serial as soon as the previous is completed.
    # No need to wait until previous commands are complete. Ok only signifies that it
    # parsed the command
    response = grblSer.read_until()
    if 'error' in str(response):
        raise Exception("grbl command error: {0}".format(response))

class SyringePump(ReagentDispenser):
    syringePumpsConfig = None
    grblSer = None
    def __init__(self, args):
        """
        Constructor. Initializes the stirrer.
        :param args:
          dict
            arduinoPort
                string - Serial device for communication with the Arduino 
            syringePumpsConfig
                dict - Configuration for the syringe pump motors

                X
                    dict - configuration of the X axis/motor

                    mmPerRev
                        Number of mm the stepper motor moves per full revolution, 
                        this is the pitch of the threaded rod
                    stepsPerRev
                        Number of steps per revolution of the stepper motor, 
                        reference the documentation for the motor
                    mmPerml
                        Number of mm of movement needed to dispense 1 ml of fluid, 
                        this is the length of the syringe divided by its fluid capacity
                    maxmmPerMin
                        Maximum speed the motor should run in mm/min
                Y
                    dict - configuration of the Y axis/motor, 
                    same as documented above but for the Y axis  

                    mmPerRev
                    stepsPerRev
                    mmPerml
                    maxmmPerMin
        """
        self.syringePumpsConfig = args["syringePumpsConfig"]
        self.grblSer = serial.Serial(args["arduinoPort"], 115200, timeout=1)

    def dispense(self, pumpId, volume):
        """
        Dispense reagent from a syringe

        :param pumpId:
            The pump id. One of 'X' or 'Y'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """

        maxmmPerMin = self.syringePumpsConfig[pumpId]['maxmmPerMin']
        mmPerml = self.syringePumpsConfig[pumpId]['mmPerml']
        totalmm = volume*mmPerml
        grblWrite(self.grblSer, 'G91{0}{1}\n'.format(pumpId, totalmm))

        # sleep for estimated dispense time, plus one second to account for (de)acceleration of the motor
        time.sleep(abs(totalmm)/maxmmPerMin*60 + 1)
