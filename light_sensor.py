# 0% light and 100% light

LIGHT_REMAP = [500, 11]
THRESHOLD = 55


class LightSensor:
    def __init__(self, mcp_channel: int):
        self.mcp_channel = mcp_channel

    def read_data(self):
        from hardware_components import hardware
        adc_value = hardware.mcp.read_adc(self.mcp_channel)
        return LightMeasure(round(self.map(0, 100, LIGHT_REMAP[0], LIGHT_REMAP[1], adc_value), 4))

    def is_dark(self):
        return self.read_data().percents < THRESHOLD

    @staticmethod
    def map(min_value, max_value, origin_min, origin_max, value):
        from connections import connections
        connections.logger.debug(f"Read data from sensor -> {value}")
        remap_rate = (abs(max_value - min_value)) / (abs(origin_max - origin_min))
        if origin_min > origin_max:
            absolute_value = abs(value - origin_max) * remap_rate
        else:
            absolute_value = abs(value - origin_min) * remap_rate
        if origin_min > origin_max:
            return max_value - absolute_value
        return min_value + absolute_value


class LightMeasure:
    def __init__(self, value):
        self.percents = value

    def save(self):
        from mqtt import publish_message
        publish_message("illumination/1", self.percents)
