from typing import Literal, Optional, Any

from hardware.reagentdispenser.base import ReagentDispenser
from hardware.lab_device import LabDevice


class PeristalticPump(ReagentDispenser):
    def __init__(self, reagent_dispenser_config: dict[str, Any], devices: dict[str, LabDevice]):
        """
        Initializes the peristaltic pump.

        :param reagent_dispenser_config: Config dict including:
            - id: device name.
            - grblID: Device id for GRBL controller.
            - peristalticPumpsConfig: Config for pumps, including:
                * F: Max feed rate in mm/min for GRBL.
                * X/Y/Z: Each with 'mmPerMl' scaling factor.
        :param devices: Dict of hardware devices.
        """
        super().__init__(reagent_dispenser_config['id'])
        self.pump_config = reagent_dispenser_config['peristalticPumpsConfig']
        self.device: 'hardware.grbl.base.GRBL' = devices[reagent_dispenser_config['grblID']]
        # G91: Set GRBL to incremental (relative) positioning mode
        self.device.write_gcode('G91')

    def dispense(self, pump_id: Literal['X', 'Y', 'Z'], volume: float, duration: Optional[float] = None) -> float:
        """
        Dispense reagent using GRBL-controlled peristaltic pump.

        :inheritdoc:
        """
        f_value = self.pump_config['F']  # Max feed rate in mm/min
        mm_per_ml = self.pump_config[pump_id]['mmPerMl']
        total_mm = volume * mm_per_ml  # Total distance in mm to move the pump

        # Determine dispense speed (mm/min): default to max, optionally limit by desired duration
        dispense_speed = f_value
        if duration:
            # Convert target rate (ml/s) to mm/min: (volume_ml / duration_s) * (60 s/min) * mm_per_ml
            desired_mm_per_min = (volume / duration) * 60 * mm_per_ml
            dispense_speed = min(desired_mm_per_min, f_value)

        # Construct GRBL command:
        # G1 = linear move (in mm), F parameter is feed rate in mm/min
        # G91 placed before ensures move is relative
        command = f'G91 G1 {pump_id}{total_mm} F{dispense_speed}'
        self.logger.debug(self.t['dispensing-command'].format(command))
        self.device.write_gcode(command)

        # Calculate dispense time in seconds:
        # dispense_speed (mm/min) / 60 gives mm/s, so time = distance_mm / (mm/min / 60)
        dispense_time = abs(total_mm) / (dispense_speed / 60)
        self.logger.info(self.t['dispensing-specific'].format(volume, dispense_speed, dispense_time))
        return dispense_time

    def get_pump_limits(self, pump_id: Literal['X', 'Y', 'Z']) -> dict[str, float]:
        """
        Returns minimum and maximum dispense speeds for pump in ml/s.

        GRBL stepper performance limits:
        - Max pulse rate ~30,000 pulses/sec; GRBL limit: https://github.com/grbl/grbl/issues/1255
        - Default pulses/mm ~250 (machine default)
        """
        mm_per_ml = self.pump_config[pump_id]['mmPerMl']

        f_value = self.pump_config['F']  # Max feed rate in mm/min
        # Convert F (mm/min) to mm/s, then to ml/s
        f_mm_per_s = f_value / 60
        f_ml_per_s = f_mm_per_s / mm_per_ml

        # Hardware max in ml/s
        # Maximum movement in mm/s = max pulses/sec / pulses_per_mm
        # Using 30,000 pulses/sec / 250 pulses/mm = 120 mm/s
        max_mm_per_second = 30000 / 250  # GRBL max step rate divided by default resolution
        # convert mm/s to ml/s: divide by mm_per_ml
        hw_max_ml_s = max_mm_per_second / mm_per_ml

        # Final max speed capped by both hardware and configuration limits
        max_speed_ml_s = min(hw_max_ml_s, f_ml_per_s)

        # Minimum speed: assume smallest reliable pulse rate ~30 pulses/sec (1% of max)
        # => 30 pulses/sec / 250 pulses/mm = 0.12 mm/s => / mm_per_ml ml/s
        min_mm_per_second = 30 / 250  # Lower bound from GRBL reliable pulse timing
        min_speed_ml_s = min_mm_per_second / mm_per_ml

        return {
            'minSpeed': min_speed_ml_s,
            'maxSpeed': max_speed_ml_s,
        }

    def close(self) -> None:
        self.device.close()
