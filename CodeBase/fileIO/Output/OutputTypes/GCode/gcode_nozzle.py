class GcodeNozzle:
    def __init__(self, name, nozzle_code, nozzle_size_mm, filament_diameter_mm, nozzle_temp_c, cooling_fan_percent,
                 infill_percent, print_speed, travel_speed, initial_layer_speed, retraction_distance, retraction_speed):
        self.name = name
        self.nozzle_code = nozzle_code
        self.nozzle_size_mm = nozzle_size_mm
        self.filament_diameter_mm = filament_diameter_mm
        self.nozzle_temp_c = nozzle_temp_c
        self.cooling_fan_percent = cooling_fan_percent
        self.infill_percent = infill_percent
        self.print_speed = print_speed
        self.travel_speed = travel_speed
        self.initial_layer_speed = initial_layer_speed
        self.retraction_distance = retraction_distance
        self.retraction_speed = retraction_speed
