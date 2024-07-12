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

class SyringePump(ReagentDispenser):
    def __init__(self, args):
        """
        Constructor. Initializes the pumps.
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
                Z
                    dict - configuration of the Z axis/motor, 
                    same as documented above but for the Z axis  

                    mmPerRev
                    stepsPerRev
                    mmPerml
                    maxmmPerMin
        """
        self.syringePumpsConfig = args["syringePumpsConfig"]
        self.grblSer = serial.Serial(args["arduinoPort"], 115200, timeout=1)
        for axis, syringeConfig in self.syringePumpsConfig.items():
            stepsPerMM = syringeConfig['stepsPerRev']/syringeConfig['mmPerRev']
            axisToCNCID = {
                "X": "0",
                "Y": "1",
                "Z": "2",
            }
            #configure steps/mm
            grblWrite(self.grblSer, '$10{0}={1}\n'.format(axisToCNCID[axis], stepsPerMM))
            #configure max mm/min
            grblWrite(self.grblSer, '$11{0}={1}\n'.format(axisToCNCID[axis], syringeConfig['maxmmPerMin']))

    def dispense(self, pumpId, volume, duration=None):
        """
        Dispense reagent from a syringe

        :param pumpId:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number of ml to dispense
        :return:
            None
        """

        maxmmPerMin = self.syringePumpsConfig[pumpId]['maxmmPerMin']
        mmPerml = self.syringePumpsConfig[pumpId]['mmPerml']
        dispenseSpeed = maxmmPerMin
        if duration:
            dispenseSpeed = min((volume/duration) * 60 * mmPerml, dispenseSpeed)
        totalmm = volume*mmPerml
        command = 'G91 G1 {0}{1} F{2}\n'.format(pumpId, totalmm, dispenseSpeed)
        logging.debug("Dispensing with command '{}'".format(command))
        grblWrite(self.grblSer, command)
        dispenseTime = abs(totalmm)/(dispenseSpeed/60)

        logging.info("Dispensing {}ml with motor speed of {}mm/min over {} seconds".format(volume, dispenseSpeed, dispenseTime))
        # sleep for estimated dispense time, plus one second to account for (de)acceleration of the motor
        time.sleep(dispenseTime + 1)
