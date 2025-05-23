from hardware.reagentdispenser.base import ReagentDispenser


class SimulatedReagentDispenser(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict):
        super().__init__('simulation')
        self.min_speed = reagent_dispenser_config.get('minSpeed') or 0.1
        self.max_speed = reagent_dispenser_config.get('maxSpeed') or 10.0

    def dispense(self, pump_id: str, volume: int, duration: int = None) -> float:
        """
        Displays pump dispensing message.

        :param pump_id:
            The pump id. One of 'X' or 'Y' or 'Z'
        :param volume:
            The number ml to dispense
        :return:
            dispensed volume
        """
        if pump_id == 'X':
            self.logger.info(self.t['dispensing-x'].format(volume))
        elif pump_id == 'Y':
            self.logger.info(self.t['dispensing-y'].format(volume))
        elif pump_id == 'Z':
            self.logger.info(self.t['dispensing-z'].format(volume))
        else:
            raise ValueError(self.t['pump-doesnt-exist'].format(pump_id))
        return abs(volume)

    def getPumpSpeedLimits(self, pump_id: str) -> dict[str, float]:
        """ :inheritdoc: """
        return {
            "minSpeed": self.min_speed,
            "maxSpeed": self.max_speed
        }
