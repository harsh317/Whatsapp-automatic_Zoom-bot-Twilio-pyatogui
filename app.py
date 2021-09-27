# The message sent by User2 comes to our /bot endpoint which  *listnets to POST request* and has a key of 'body'
from flask import Flask, request # flask's request can used to get these POST request 
from twilio.twiml.messaging_response import MessagingResponse # Twilio expects an response given in TwiML(Xml based) language. This class can be used to covert our respose into TwiML
import re, threading, subprocess, pyautogui, os

# Our Global Vars
Meet_id = 0
name = ''
Meet_pass = ''

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

app = Flask(__name__) # Initialte Our Flask App

@app.route("/") # if we open the '/' route
def hello(): 
    return "Hello, World!"

def Openzoom(): 
    print('Id is:', Meet_id, 'Pass is : ', Meet_pass, 'name is: ', name)
    subprocess.call('C:\\Users\\jainh\\AppData\\Roaming\\Zoom\\bin_00\\Zoom.exe') # Open Zoom
    pyautogui.getWindowsWithTitle("Zoom")[0].maximize() # Maximize the window
    clickjoin = pyautogui.locateCenterOnScreen('joinIMG.png', confidence = 0.4) # Locate the join Button
    pyautogui.moveTo(clickjoin) # Move To the Join Button
    pyautogui.click(interval=1) # Click it
    pyautogui.write(str(Meet_id), interval=1) # Write our Meeting Password
    pyautogui.press('tab',presses=2) # Press Tab key 2 times to reach the Enter your name column
    pyautogui.hotkey('ctrl', 'a') # Press Ctrl + a  to select all
    pyautogui.write(name) # write the name
    pyautogui.press('enter', interval=5) # press enter
    pyautogui.write(str(Meet_pass)) # Enter Meeting Password
    pyautogui.press('enter', interval=5) # Press Enter


@app.route("/bot", methods=['POST']) # Our '/bot' route and this will only listen to POST requests
def bot():

    # Create reply
    resp = MessagingResponse()

    # Global Var
    global Meet_id,Meet_pass,name

    # Fetch the message
    message = request.form.get('Body') # Get the message sent by other user(The request will have a key of 'Body')
    try:
        check = re.findall(r'(zoom|Zoom|inviting|scheduled|meeting|Join)', message) # Check and returns an array if substring is there in this string
        if check: # if it contains
            if message.find('inviting you to a scheduled') != -1 or message.find('Join Zoom Meeting') or message.find('Meeting ID'): # Check if these sentences are therein that string (Just for a second check)
                Url_if=re.search("(?P<url>https?://[^\s]+)", message).group("url") # Get The url in the string
                f = open("name.txt", "a+") # This is the file that will contain my name while joining the meeting
                f.seek(0) #  set the reference point at the beginning of the file 
                nameGet = str(f.readline()) # Read that name
                if nameGet == '':
                    name = 'Defualt Bot name'
                name = nameGet
                f.close()
                split = message.split("D:") # Split the message
                Meet_id = split[1] # the 2 array item that has been splited
                Meet_id = int(Meet_id.split("P")[0].replace(" ", "")) # Split the string, Get the Id, Remove the Extra Splace, Convert to int
                Meet_pass = message.split("code:")[1].replace(" ", "")  # Same as above just dont conert to int
                alldetails = 'Url is: ',Url_if, " and Id is: ",str(Meet_id), "And pass is: "+Meet_pass
                start_thread(Openzoom) # Start the thread
                resp.message("You Details are: {}".format(alldetails))
        else:
             resp.message("You just said that: {}".format(message)) 
    except Exception as e:
        print(e)

    return str(resp) # Return the resp

if __name__ == "__main__":
    app.run(debug=True)
