import math

from hardware.reagentdispenser.base import ReagentDispenser
from hardware.lab_device import LabDevice


class SyringePump(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict, devices: dict[str, LabDevice]):
        """
        Initialize a SyringePump by configuring its axes on the GRBL controller.

        :param reagent_dispenser_config: dict containing:
            id: str
                Logical name of this dispenser
            grblID: str
                Key into `devices` for the GRBL controller instance
            syringePumpsConfig: dict
                Mapping of axis labels ('X', 'Y', 'Z') to their mechanical parameters:
                  mmPerRev: float
                      Linear travel (mm) per 1 motor revolution (leadscrew pitch)
                  stepsPerRev: int
                      Stepper motor steps per revolution
                  mmPerMl: float
                      Travel distance (mm) required to dispense 1 mL of fluid
                  maxMmPerMin: float
                      Maximum allowed feed-rate (mm/min) for that axis

        :param devices: dict
            Hardware device instances; must include a GRBL controller under the key given by grblID

        Upon construction, this will:
          1. Compute and store a "safe" minimum feed-rate (mm/min) to avoid stalling.
          2. Calculate steps-per-mm for each axis and write it to GRBL's `$10n` setting.
          3. Write each axis's maximum feed-rate to GRBL's `$11n` setting.
        """
        super().__init__(reagent_dispenser_config['id'])
        self.device: 'hardware.grbl.base.GRBL' = devices[reagent_dispenser_config['grblID']]
        self.syringe_pumps_config = reagent_dispenser_config['syringePumpsConfig']
        self.axis_min_mm_per_min: dict[str, float] = {}

        # GRBL exposes each axis's settings under numbered variables:
        # $100 = X-axis steps/mm
        # $101 = Y-axis steps/mm
        # $102 = Z-axis steps/mm
        # $110 = X-axis max feed-rate (mm/min)
        # $111 = Y-axis max feed-rate (mm/min)
        # $112 = Z-axis max feed-rate (mm/min)
        # Map our logical axes to GRBL's axis index (0=X, 1=Y, 2=Z)
        axis_to_cnc_id: dict[str, str] = {'X': '0', 'Y': '1', 'Z': '2'}

        for axis, cfg in self.syringe_pumps_config.items():
            # Determine how many stepper steps equal 1 mm of linear motion:
            # steps_per_mm = (motor steps per rev) / (mm traveled per rev)
            steps_per_mm = cfg['stepsPerRev'] / cfg['mmPerRev']

            # Calculate a safe minimum feed-rate to avoid stalling:
            # Use 30 RPM as the slowest screw speed, convert rev/min -> mm/min:
            #   30 rev/min × (mmPerRev) = mm/min at 30 RPM
            # Then round up to the next integer feed-rate.
            self.axis_min_mm_per_min[axis] = math.ceil(30 * cfg['mmPerRev'])

            # Send GRBL the steps/mm setting for this axis:
            #   $10n = steps/mm for axis n (0=X,1=Y,2=Z)
            cmd_steps = f'$10{axis_to_cnc_id[axis]}={steps_per_mm}'
            self.device.write_gcode(cmd_steps)
            self.logger.debug(f'Configured steps/mm ({axis}): {cmd_steps}')

            # Send GRBL the max feed-rate (mm/min) for this axis:
            #   $11n = max feed-rate for axis n (0=X,1=Y,2=Z)
            max_mm_per_min = cfg['maxMmPerMin']
            cmd_max_rate = f'$11{axis_to_cnc_id[axis]}={max_mm_per_min}'
            self.device.write_gcode(cmd_max_rate)
            self.logger.debug(f'Configured max feed-rate ({axis}): {cmd_max_rate}')

    def dispense(self, pump_id: str, volume: int, duration: int = None) -> float:
        """ :inheritdoc: """
        max_mm_per_min = self.syringe_pumps_config[pump_id]['maxMmPerMin']
        mm_per_ml = self.syringe_pumps_config[pump_id]['mmPerMl']

        # Determine feed rate (F) in mm/min
        # If duration given (in s), convert desired ml/s to mm/min:
        #   (volume / duration) [ml/s] * mm_per_ml [mm/ml] * 60 [s/min]
        # Else use max_mm_per_min
        if duration:
            desired_mm_per_min = (volume / duration) * mm_per_ml * 60  # *60 to convert from mm/s to mm/min for GRBL
            feed_mm_per_min = min(desired_mm_per_min, max_mm_per_min)
        else:
            feed_mm_per_min = max_mm_per_min

        # Total movement in mm
        total_mm = volume * mm_per_ml

        # Build GRBL motion command:
        # G91 = Set to Relative Positioning mode (moves are relative to current position)
        # G1  = Linear motion with specified feed rate
        # F   = Feed rate in mm/min (GRBL expects per-minute units)
        command = f'G91 G1 {pump_id}{total_mm} F{feed_mm_per_min}'
        self.logger.debug(self.t['dispensing-command'].format(command))
        self.device.write_gcode(command)

        # Calculate actual dispense time: distance / speed
        # speed = feed_mm_per_min [mm/min] => feed_mm_per_min/60 = mm/s
        dispense_time = abs(total_mm) / (feed_mm_per_min / 60)  # /60 to convert mm/min to mm/s

        self.logger.info(self.t['dispensing-specific'].format(volume, feed_mm_per_min, dispense_time))
        return dispense_time

    def get_pump_limits(self, pump_id: str) -> dict[str, float]:
        """ :inheritdoc: """
        max_mm_per_min = self.syringe_pumps_config[pump_id]['maxMmPerMin']
        mm_per_ml = self.syringe_pumps_config[pump_id]['mmPerMl']

        # Convert mm/min to ml/s: mm/min / mm_per_ml = ml/min, then /60 => ml/s
        max_speed_ml_s = max_mm_per_min / mm_per_ml / 60
        min_speed_ml_s = self.axis_min_mm_per_min[pump_id] / mm_per_ml / 60
        return {'minSpeed': min_speed_ml_s, 'maxSpeed': max_speed_ml_s}

    def close(self) -> None:
        self.device.close()
