import RPi.GPIO as GPIO
import time as time
import pygame.mixer 
import feedparser
import settings 

USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
LABEL = settings.LABEL
SOUND = settings.SOUND

#GPIUO Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Initialize LED Pins as outputs and default them to OFF
LED_1 = 25
LED_2 = 22
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)

GPIO.output(LED_1, False)
GPIO.output(LED_2, False)

#Define & Initialize Stepper Pins, setStep to 0 to release motor and save power
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

    

#initialize pygame mixer and sounds
pygame.mixer.init(48000, -16, 1, 1024)
sndA = pygame.mixer.Sound(SOUND)
soundChannelA = pygame.mixer.Channel(1)


#define Step, Stepper forward and stepper backwards
# This sends tiny pulses of current to the coils in sequential order to keep the motor turning
# Delay sets the speed (lower is faster, fastest seems to be 2, slowest I tried is 20
# There are 512 steps in 360*
def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        if i%10 == 0:
            GPIO.output(LED_1, False)
            GPIO.output(LED_2, True)
        elif i%5 == 0:
            GPIO.output(LED_1, True)
            GPIO.output(LED_2, False)

def backwards(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        if i%10 == 0:
            GPIO.output(LED_1, False)
            GPIO.output(LED_2, True)
        elif i%5 == 0:
            GPIO.output(LED_1, True)
            GPIO.output(LED_2, False)


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

setStep(0,0,0,0)


try:
        
    #read from the Gmail Atom Feed
    inbox = feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom/" + LABEL)

    # Grab Publshed date from each email with Safari Flow Signup in the subject
    # GMAIL FAIL Atom Feed only contains earliest unread email in thread, and my alerts were all threaded
    # Created a script that ran every 30 seconds and marked everything but the newest email as read, but I think the usage causes it to be disabled?
    # See http://2sdd.blogspot.ru/2012/11/how-to-clean-up-gmail-inbox-from-emails.html
    
    with open('log', 'r+') as log:
        last_signup = log.readline().replace('\n', '')
  
    print last_signup + " -Last Stored Email Timestamp from Log File"
    
    timestamps = []
    
    for emails in inbox['entries']:
        # Store this in a variable so it doesn't have to parse every time
        timestamps.append(emails.get('published', ''))
    
    print max(timestamps) + " -Newest Evmail Timestamp in Inbox"
    
    if max(timestamps) > last_signup:
        
        #Play the Heron Mating Call
        soundChannelA.play(sndA)
        
        #While Heron is mating, Flap Wings
        while soundChannelA.get_busy():
            forward(3 / 1000.0, 25) #seconds | convert to millis  | # of Steps 128 = 360*
            backwards(3 / 1000.0, 25)

        #Cleanup Pin Status, Release stepper motor
        GPIO.output(LED_1, False)
        GPIO.output(LED_2, False)
        setStep(0,0,0,0)
        GPIO.cleanup()
    
        with open('log', 'w+') as log:
            log.write(str(max(timestamps))+"\n")
            log.write(str(len(timestamps))+" qualifying email events today")
            print "Updated Newest Email Timestamp in file"
    
    else:    
        print "Didn't write anything to file"
    
    
    exit()

except KeyboardInterrupt:
    exit()