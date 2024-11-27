import spidev
import struct

class ADXL355:
    def __init__(self, bus=0, device=0, spi_speed=10000000):
        """Initialize the SPI interface for ADXL355."""
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = spi_speed
        self.spi.mode = 0  # SPI mode 0 (CPOL=0, CPHA=0)

    def read_register(self, reg_address, length=1):
        """Read a byte or multiple bytes from a register."""
        if length == 1:
            return self.spi.xfer2([0x80 | reg_address, 0x00])[1]
        return self.spi.xfer2([0x80 | reg_address] + [0x00] * length)[1:]

    def write_register(self, reg_address, value):
        """Write a single byte to a register."""
        self.spi.xfer2([reg_address & 0x7F, value])

    def get_device_id(self):
        """Get the device ID from register 0x00."""
        return self.read_register(0x00)

    def get_temperature(self):
        """Read and calculate temperature from TEMP2 and TEMP1 registers."""
        temp_data = self.read_register(0x06, 2)
        temp_raw = (temp_data[0] << 8 | temp_data[1]) >> 4
        if temp_raw & 0x800:
            temp_raw -= 0x1000
        temperature_c = 25 + (temp_raw / 256.0)
        return temperature_c

    def get_axes(self):
        """Read the X, Y, and Z axes' acceleration data."""
        data = self.read_register(0x08, 9)  # Read 9 bytes (3x 3-byte values)
        x = self._convert_data(data[0:3])
        y = self._convert_data(data[3:6])
        z = self._convert_data(data[6:9])
        return {"X": x, "Y": y, "Z": z}

    def _convert_data(self, data):
        """Convert 3 bytes of data to a 20-bit signed integer."""
        raw = (data[0] << 16) | (data[1] << 8) | data[2]
        raw >>= 4  # 20-bit right-aligned
        if raw & 0x80000:
            raw -= 0x100000  # Convert to signed
        return raw * 0.0000039  # Convert to g's (scale factor)

    def set_power_control(self, power_on=True):
        """Set the power control mode: Power-on or Standby."""
        reg_value = 0x00 if power_on else 0x01
        self.write_register(0x2D, reg_value)

    def reset_device(self):
        """Reset the device by writing to the reset register."""
        self.write_register(0x2F, 0x52)

    def close(self):
        """Close the SPI connection."""
        self.spi.close()
