from hardware.stirring.base import Stirrer

RELAY_ON: int = 1
RELAY_OFF: int = 0


class GPIOStirrer(Stirrer):

    def __init__(self, stirrer_config: dict, devices: dict):
        """
        Initializes the stirrer.
        :param stirrer_config: Config dict including:
            - id: device name.
            - gpioID: The ID of the GPIO device used to control stirring
            - stirrerPin: Which gpio pin to control the stirrer
        :param devices: Dict of hardware devices.
        """
        super().__init__(stirrer_config['id'])
        self.device = devices[stirrer_config['gpioID']]
        self.stirrerPin = stirrer_config['stirrerPin']
        
        self.device.setup(self.stirrerPin)
        self.device.output(self.stirrerPin, RELAY_OFF)

    def turnStirrerOn(self) -> None:
        """ :inheritdoc: """
        self.device.output(self.stirrerPin, RELAY_ON)

    def turnStirrerOff(self) -> None:
        """ :inheritdoc: """
        self.device.output(self.stirrerPin, RELAY_OFF)
