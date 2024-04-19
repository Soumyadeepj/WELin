import utime
import network
import urequests
import PN532
import machine

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("WEL_6_2.4", "wel6wifi@123")

# Main loop
while True:
    # Read UID tag
    tag = PN532.read_uid()
    if tag is not None:
        print("CARD ID:", tag)
        # Turn on GPIO pin 11 (GP11) for 3 seconds
        gp11 = machine.Pin(11, machine.Pin.OUT)
        gp11.on()
        utime.sleep(3)  # Wait for 3 seconds
        gp11.off()  # Turn off GP11
        print("pin15 is turned on and off check it")
        
        # Get current date and format it as YYYY-MM-DD
        current_date = utime.localtime()[0:3]  # Year, month, day
        formatted_date = "{:04d}-{:02d}-{:02d}".format(*current_date)
        formatted_date = formatted_date.strip()
        
        # Get current time and format it as HH:MM:SS
        current_time = utime.localtime()[3:6]  # Hour, minute, second
        formatted_time = "{:02d}:{:02d}:{:02d}".format(*current_time)
        print("Date of scanning:",formatted_date)
        print("Time of scanning:",formatted_time)
        
        # Update sensor value and date in the API endpoint URL
        sheets_api_url = f"https://script.google.com/macros/s/AKfycbzJwmOBTvqyd9G3cEPF4PWdiSXCAKc0qSzcotynxWSRTIBXSXd4nw-X3RheWGLZeRLplA/exec?date={formatted_date}&time={formatted_time}&tag={tag}"    
        # Send HTTP GET request to update sensor value
        response = urequests.get(sheets_api_url)
        
        # Close the response
        response.close()
    
    # Wait for one minute
    utime.sleep(5)
