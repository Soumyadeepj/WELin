import NFC_PN532 as nfc
import machine
def read_uid():
    # SPI
    spi_dev = machine.SPI(0, baudrate=400000, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
    cs = machine.Pin(5, machine.Pin.OUT)
    cs.on()

    # SENSOR INIT
    pn532 = nfc.PN532(spi_dev, cs)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    print('Reading...')
    uid = pn532.read_passive_target(timeout=1000)
    if uid is None:
        print('CARD NOT FOUND')
        return None
    else:
        string_ID = '-'.join([str(i) for i in uid])
        print('Found card with UID:', [str(i) for i in uid])
        print('Number_id: {}'.format(string_ID))
        return string_ID
        
        # Turn on GPIO pin 14 (GP14) for 3 seconds
        gp11 = machine.Pin(11, machine.Pin.OUT)
        gp11.on()
        time.sleep(3)  # Wait for 3 seconds
        gp11.off()  # Turn off GP14
