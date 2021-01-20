from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re,subprocess,pyautogui,threading

Meet_id = 0
name = ''
Meet_pass = ''

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    
def fucti():
    
    subprocess.call('C:\\Users\\jainh\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe')
    pyautogui.getWindowsWithTitle("Zoom")[0].maximize()
    clickjoin = pyautogui.locateCenterOnScreen('joinIMG.png', confidence = 0.4)
    pyautogui.moveTo(clickjoin)
    pyautogui.click()
    pyautogui.press('enter', interval=5)
    pyautogui.write(str(Meet_id))

    pyautogui.press('tab',presses=2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write(name)
    pyautogui.press('enter', interval=10)
                
    pyautogui.write(str(Meet_pass))
    pyautogui.press('enter', interval=10)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    global Meet_id,Meet_pass,name
    try:
        check = re.findall(r'(zoom|Zoom|inviting|scheduled|meeting|Join)', msg) 
        if check:            
            if msg.find('inviting you to a scheduled') != -1 or msg.find('Join Zoom Meeting') or msg.find('Meeting ID'):
                Url_if=re.search("(?P<url>https?://[^\s]+)", msg).group("url")
                f = open("name.txt", "r")
                name = str(f.readline())
                split = msg.split("D:")
                Meet_id = split[1] 
                Meet_id = Meet_id.split("P")[0]
                Meet_id = int(Meet_id.replace(" ", ""))
                Meet_pass = msg.split("ode:")[1]
                Meet_pass = Meet_pass.replace(" ", "") 
                print(Url_if)
                print(Meet_id,Meet_pass)
                print('Meeting pass:',Meet_pass)
                alls = Url_if+" and"+str(Meet_id)+":"+Meet_pass
                start_thread(fucti)
                resp = MessagingResponse()
                resp.message("You Details are: {}".format(alls))
                return str(resp)

                
        else:
            resp = MessagingResponse()
            resp.message("Harsh said: {}".format(msg)) 
            return str(resp) 
                  
    except Exception as e:
        print(e)

    
    

    

if __name__ == "__main__":
    app.run(debug=True) 
