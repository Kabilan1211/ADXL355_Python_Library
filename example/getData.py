from adxl355 import ADXL355

def main():
    adxl = ADXL355(bus=0, device=0)

    try:
        # Reset and initialize device
        adxl.reset_device()
        adxl.set_power_control(power_on=True)

        # Read and print the device ID
        device_id = adxl.get_device_id()
        print(f"Device ID: {hex(device_id)}")

        # Read and print temperature
        temperature = adxl.get_temperature()
        print(f"Temperature: {temperature:.2f} °C")

        # Read and print acceleration data
        axes_data = adxl.get_axes()
        print(f"Acceleration Data (g's):")
        print(f"  X: {axes_data['X']:.6f} g")
        print(f"  Y: {axes_data['Y']:.6f} g")
        print(f"  Z: {axes_data['Z']:.6f} g")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        adxl.close()

if __name__ == "__main__":
    main()
