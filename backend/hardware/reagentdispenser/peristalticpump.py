import time
import config
import serial
from hardware.reagentdispenser.base import ReagentDispenser
import logging

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

class PeristalticPump(ReagentDispenser):
    def __init__(self, args):
        """
        Constructor. Initializes the pumps.
        :param args:
          dict
            arduinoPort
                string - Serial device for communication with the Arduino 
            peristalticPumpsConfig
                dict - Configuration for the peristaltic pump motors
                F   Flow rate
                X
                    mlPerUnit   Arbitrary scaling factor
                Y
                    mlPerUnit   Arbitrary scaling factor
                Z
                    mlPerUnit   Arbitrary scaling factor
        """
        self.peristalticPumpsConfig = args["peristalticPumpsConfig"]
        self.grblSer = serial.Serial(args["arduinoPort"], 115200, timeout=1)
        grblWrite(self.grblSer, 'G91')

    def dispense(self, pumpId, volume, duration=None):
        """
        Dispense reagent from a peristaltic pump

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """
        fValue = self.peristalticPumpsConfig['F']
        mmPerml = self.peristalticPumpsConfig[pumpId]['mlPerUnit']
        totalmm = volume * mmPerml

        dispenseSpeed = fValue
        if duration:
            dispenseSpeed = min((volume/duration) * 60 * mmPerml, dispenseSpeed)
        grblWrite(self.grblSer, 'G91 {0}{1} F{2}\n'.format(pumpId, totalmm, dispenseSpeed))
        
        dispenseTime = abs(totalmm)/(dispenseSpeed/60)
        logging.info("Dispensing {}ml with motor speed of {}mm/min over {} seconds".format(volume, dispenseSpeed, dispenseTime))
        # sleep for estimated dispense time, plus one second to account for (de)acceleration of the motor
        time.sleep(dispenseTime + 1)
