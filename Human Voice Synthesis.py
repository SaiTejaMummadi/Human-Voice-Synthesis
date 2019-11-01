#import threading

import time #for time
import os #file manipulation
from tkinter import * #Graphical User Interface
import threading #for Multi Threading
import pyttsx3#Python library for automatic text to speech
import random #To generate random numbers for filename

#Speech Recognition using Google 
import speech_recognition as sr
r = sr.Recognizer()


#Dictionary of punctuations for converting into symbols
list_of_punctuations = {'comma': ',', 'fullstop': '.', 'full stop': '.',
                        'new line': '\n', 'newline': '\n', 'colon': ':',
                        "exclamation mark": '!', "semicolon": ';', 'question mark': '?',
                        'hyphen': '-', 'underscore': '_', 'hash': '#'}
#Fonts for GUI labels
fnt1 = ('Arial',12,'bold')
fnt2 = ('Arial',20,'bold')

#Global Variables
btnAnim = 0
rec = 0



#Function for converting text to speech automatically
def speakText(text):
    try:
        engine = pyttsx3.init() #Initialsing the text to speech class
        # engine.setProperty(
        #     'voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        engine.setProperty('rate', 120)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1
        engine.say(text) #Input as text and Output as Speech, WORKS ONLY IN POWERSHELL
        engine.runAndWait() #Returns when all commands queued before this call are emptied from the queue.
    except:
        pass

#Function for converting speech to text
def stt():
    global btnAnim, rec, L2 #Taking global variables

    if(rec ==1):
        L2.delete(0.0,END) #Clearing previous text
        L2.insert(0.0," "*25+"Please Stay Silent for few Seconds") 
        #Entering into command line
        print('Calibrating Microphone')
        print('Please be silent for few seconds.')
        time.sleep(1) #1 second
        with sr.Microphone() as source: 
            r.adjust_for_ambient_noise(source,duration=4) #Calibrating surrounding
            L2.delete(0.0,END)
            L2.insert(0.0, " "*25+"                 Speak Now")
            time.sleep(1) #1 second



        with sr.Microphone() as source: #Initialising and handling exception with "with" keyword
            print("Say something!")
            try:
                #Listening and converting into audio, waits for 10 seconds if there's no audio
                audio = r.listen(source,timeout = 10) 
            except Exception as e:
                print("MIC ERROR : ",e)
                

        #Recognize speech using Google Speech Recognition
        try:
            #Sending audio file to Google REQUIRES INTERNET CONNECTION
            b = r.recognize_google(audio) 
            print('\n\n\n'+ b)
            #Replacing the punctuations with symbols
            for x in list_of_punctuations.keys():
                if x in b:
                    b = b.replace(x, list_of_punctuations[x])           
            print('\n\n\n'+ b)
            L2.delete(0.0,END) #Clearing previous text
            L2.insert(0.0,b) #Inserting converted text
            speakText(b) #Converting text to speech
            temp = str(random.randint(100,1000)) #Random file number generation
            #Opening a file and storing the updated text into the file.
            f = open("storedText"+temp+".txt",'w')
            f.write(b)
            f.close()
            print("Output Saved in storedText"+temp+".txt")
            
        #Handling inaudible speech error
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            L2.delete(0.0,END)
            L2.insert(0.0," Speech Recognition could not understand audio. Please Speak Clearly")
        #Handling Internet Connection error
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            L2.delete(0.0,END)
            L2.insert(0.0,"Could not request results from Google Speech Recognition service. Please Check for Internet Connection ")

        time.sleep(2) #two seconds
        print('\n\n')
        btnAnim, rec = 0,0

root = Tk()
#root = tk.Toplevel() #Creating object for GUI
root.title("Advance Speech to Text") # Title of Label1
root.geometry("500x500+400+10") #Dimensions of the Label1 window

N = 3 #change N value to exact number of frames your gif contains for full  play
frames = [PhotoImage(file='micrec.gif',format = 'gif -index  %i' %(i)) for i in range(N)] #

#Function for animating GIF
def update(ind):
    global btnAnim
    if(btnAnim==1):
            ind = ind%N
            frame = frames[ind]
            ind += 1
            B1.config(image=frame)
    root.after(100, update, ind)

#Function for multithreading
def multiThreading():
    while True:
        stt()
        

t1 = threading.Thread(target = multiThreading) #Initialise multithreading
t1.start() #Starts the thread

#Function sets the global values to 1
def start1():
    global btnAnim, rec
    btnAnim = 1
    rec = 1
    
#Creating window using GUI object and assigning background color
win = Frame(root, bg ='powderblue')

L1 = Label(win,text="ADVANCE SPEECH TO TEXT") #Displaying text on Label1 window
L1.config(font = fnt2,bg ='powderblue') #Assigning font and background color
L1.place(x=25,y=10,height = 30,width = 450) #Dimensions of Label1

L2 = Text(win) #Initially empty, displays converted text
L2.config(font = fnt1) #Assigning font for Label2
L2.place(x=25,y=50,height = 200,width = 450) #Dimensions of Label2

B1 = Button(win) #Creating a button on the window
photo = PhotoImage(file = "micrec.gif") #Displays the gif file
B1.config(image=photo,relief = RAISED, command = start1) #Shows a highlighted button photo, triggers with "start1" 
B1.config(bg='red') #Setting backgroung color of the gif
B1.place(x = 150, y = 280, height = 200, width = 200) #Dimensions of the button



win.place(x=0,y=0,height = 500,width = 500) #Overall dimensions of the GUI window
root.after(0, update, 0) #For updating GIF
mainloop() #For TKinter


