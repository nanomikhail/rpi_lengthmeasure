import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

TRIG = 16 
ECHO = 18

print ('Distance Measurement In Progress')

def measure():
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.output(TRIG, False)
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()
	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 1)
	lcd_string("Distance:", LCD_LINE_1)
	lcd_string(str(distance)+' cm', LCD_LINE_2)

#---------------------------------------------------------------#

# Define GPIO to LCD mapping(Use BOARD GPIO numbers)
LCD_RS = 5
LCD_E  = 3
LCD_D4 = 12
LCD_D5 = 11
LCD_D6 = 13
LCD_D7 = 15
 
# Define some constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
E_PULSE = 0.0005
E_DELAY = 0.0005

# Define some functions
def lcd_init():

	GPIO.setup(LCD_E,  GPIO.OUT)
	GPIO.setup(LCD_RS, GPIO.OUT)
	GPIO.setup(LCD_D4, GPIO.OUT)
	GPIO.setup(LCD_D5, GPIO.OUT)
	GPIO.setup(LCD_D6, GPIO.OUT)
	GPIO.setup(LCD_D7, GPIO.OUT)
	lcd_byte(0x33,LCD_CMD)
	lcd_byte(0x32,LCD_CMD)
	lcd_byte(0x06,LCD_CMD)
	lcd_byte(0x0C,LCD_CMD)
	lcd_byte(0x28,LCD_CMD)
	lcd_byte(0x01,LCD_CMD)
	time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
	GPIO.output(LCD_RS, mode)

	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)
	lcd_toggle_enable()

	# Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x01==0x01:
		GPIO.output(LCD_D4, True)
	if bits&0x02==0x02:
		GPIO.output(LCD_D5, True)
	if bits&0x04==0x04:
		GPIO.output(LCD_D6, True)
	if bits&0x08==0x08:
		GPIO.output(LCD_D7, True)
	lcd_toggle_enable()
 
def lcd_toggle_enable():
	time.sleep(E_DELAY)
	GPIO.output(LCD_E, True)
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)
	time.sleep(E_DELAY)

def lcd_string(message,line):
	message = message.ljust(LCD_WIDTH," ")
	lcd_byte(line, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

def lcd_chr(num):
	string = "0000000000000000"
	lcd_byte(LCD_LINE_1, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(num ,LCD_CHR)
	lcd_byte(LCD_LINE_2, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(num ,LCD_CHR)

GPIO.setmode(GPIO.BOARD)    
GPIO.setup(LCD_E,  GPIO.OUT) 
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

#---------------------------------------------------------------#

lcd_init()

lcd_byte(0x40, LCD_CMD)

lcd_byte(0b00000100, LCD_CHR)
lcd_byte(0b00000110, LCD_CHR)
lcd_byte(0b00011111, LCD_CHR)
lcd_byte(0b00010100, LCD_CHR)
lcd_byte(0b00000110, LCD_CHR)
lcd_byte(0b00001100, LCD_CHR)
lcd_byte(0b00010111, LCD_CHR)
lcd_byte(0b00000100, LCD_CHR)

lcd_byte(0x80, LCD_CMD)

while True:
	measure()
	time.sleep(0.5)

	

GPIO.cleanup()