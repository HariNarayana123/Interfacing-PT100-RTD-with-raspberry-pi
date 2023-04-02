import spidev
import time

# Define SPI bus and chip select pins
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0 as CS pin

# Define MAX31865 registers
MAX31865_REG_CONFIG = 0x00
MAX31865_REG_RTD_MSB = 0x01
MAX31865_REG_RTD_LSB = 0x02
MAX31865_REG_HIGH_FAULT_MSB = 0x03
MAX31865_REG_HIGH_FAULT_LSB = 0x04
MAX31865_REG_LOW_FAULT_MSB = 0x05
MAX31865_REG_LOW_FAULT_LSB = 0x06
MAX31865_REG_FAULT_STATUS = 0x07

# Define MAX31865 configuration bits
MAX31865_CONFIG_BIAS = 0x80
MAX31865_CONFIG_MODE_AUTO = 0x40
MAX31865_CONFIG_MODE_OFF = 0x00
MAX31865_CONFIG_1SHOT = 0x20
MAX31865_CONFIG_3WIRE = 0x10
MAX31865_CONFIG_FAULTSTAT = 0x02
MAX31865_CONFIG_FILTER50HZ = 0x01

# Define PT100 RTD constants
PT100_A = 3.9083e-3
PT100_B = -5.775e-7
PT100_R0 = 100.0

# Define function to read MAX31865 registers
def max31865_read_reg(reg):
    tx_data = [reg, 0x00]
    rx_data = spi.xfer2(tx_data)
    return rx_data[1]

# Define function to write MAX31865 registers
def max31865_write_reg(reg, data):
    tx_data = [reg | 0x80, data]
    spi.xfer2(tx_data)

# Configure MAX31865
max31865_write_reg(MAX31865_REG_CONFIG, MAX31865_CONFIG_BIAS | MAX31865_CONFIG_3WIRE | MAX31865_CONFIG_FAULTSTAT)

while True:
  try:
    # Read RTD MSB and LSB registers
    rtd_msb = max31865_read_reg(MAX31865_REG_RTD_MSB)
    rtd_lsb = max31865_read_reg(MAX31865_REG_RTD_LSB)
    
    # Calculate RTD resistance
    rtd_raw = ((rtd_msb << 8) | rtd_lsb) >> 1
    rtd_resistance = rtd_raw * 0.385
    print("RTD Resistance: {} Ohms".format(rtd_resistance))
    
    # Calculate temperature using PT100 RTD formula
    rtd_ratio = rtd_resistance / PT100_R0
    temperature = ((PT100_A * PT100_R0) - (PT100_A * rtd_resistance) + (PT100_B * (PT100_R0 ** 2)) - (PT100_B * PT100_R0 * rtd_resistance)) / (PT100_R0 * (1 + (PT100_A * (25 - PT100_R0))))
    print("Temperature: {:.2f} °C".format(temperature))
    
    time.sleep(1)
 except KeyboardInterrupt:
    print("Program terminated by user")
    sys.exit()
 finally:
     spi.close()
 
