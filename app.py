# all modules
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re,subprocess,pyautogui,threading,requests,emoji,json,time,keyboard,psutil,smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText


# var
Meet_id = 0
name = ''
Meet_pass = ''
options = ("cat", "dog", "koala", "fox", "birb", "red_panda", "panda", "racoon", "kangaroo")
running = False
PROCNAME = "notepad.exe"


# All fuctions
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
    
def animalimage(animal):
    r = requests.get("https://some-random-api.ml/img/" + animal)
    r = r.json()
    return r["link"]
			

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    resp = MessagingResponse()
    msg_send= resp.message()
    """Respond to incoming calls with a simple text message."""

    msg = request.form.get('Body')
    if msg.lower().startswith('bird'):
        msg = 'birb'
    # Global Var    
    global Meet_id,Meet_pass,name,running
    # Code for opening zoom and joining zoom
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
                msg_send.body("You Details are: {}".format(alls))
                

            
        elif msg.lower() in ['hello','howdy','hi','hey','helo']:
            response = emoji.emojize("""
                *Hi! I am the Harsh's Bot* :wave:
                *Let us be friends*:two_men_holding_hands:
                """ ,use_aliases=True)
            msg_send.body(response)

        

        elif msg.lower() in ['joke','tell me a joke','joke of the day']:
            data = requests.get("https://official-joke-api.appspot.com/random_ten")
            tt = json.loads(data.text)
            response = emoji.emojize("""
                *{}* :confused:
                *{}*:laughing:
                """ ,use_aliases=True).format(tt[1]['setup'],tt[1]['punchline'])
            msg_send.body(response)
 
        
        elif msg.lower().startswith(options):
            print('true')
            animal = msg.lower().split()[0]
            link = animalimage(animal)
            msg_send.body(animal+' Image')
            msg_send.media(link)

        
        elif msg.lower() in ['animal','animal image','a animal','show me an animal','an animal']:
            response = emoji.emojize("""
                *Hi! I have images of only 9 animals* :tiger2:
                *The following Are some-*:point_down:
                *Cat*:pouting_cat:
                *Dog*:dog2:
                *Koala*:koala:
                *Fox*:wolf:
                *Bird*:bird:
                *Panda*:panda_face:
                *Red_Panda*:red_circle:
                *racoon*:monkey:
                *Kangaroo 🦘* 
                """ ,use_aliases=True)
            msg_send.body(response)
            
        elif msg.lower() in ['email','send email']:
            tell = pyautogui.alert('Enter:\n𝔽𝕣𝕠𝕞\n𝕋𝕠\n𝕊𝕦𝕓𝕛𝕖𝕔𝕥\n𝔹𝕠𝕕𝕪\nℙ𝕒𝕤𝕤𝕨𝕠𝕣𝕕\n𝕌𝕤𝕖𝕣𝕟𝕒𝕞𝕖\nrespectively in each line\𝕻𝖑𝖊𝖆𝖘𝖊 𝕻𝖗𝖊𝖘𝖘 𝕮𝖙𝖗𝖑 + 𝖘 after that ')
            if tell:            
                with open('cred.txt', 'w') as filehandle:
                    filebuffer = ["From:", "To:", "Subject:","Body:","Password:","Username:","....................................................................."]
                    filehandle.writelines("%s\n" % line for line in filebuffer)
                subprocess.Popen(['notepad.exe','cred.txt'])
                hotkey = "ctrl + s"
                while not running:
                    if keyboard.is_pressed(hotkey):
                        for proc in psutil.process_iter():
                            # check whether the process name matches
                            if proc.name() == 'notepad.exe':
                                proc.kill()
                        running = True     
                           
                f=open('cred.txt')
                lines=f.readlines()
                var_names = ["from_mail","to","subject","body","password","username"]
                count = 0
                for name in var_names:
                    globals()[name] = lines[count]
                    count += 1
                print(from_mail)
                usernames = username.replace(' ','').split(":",1)[1]
                passwords = password.replace(' ','').split(":",1)[1] 
                Subjects_mail = subject.split(":",1)[1] 
                bodys = body.split(":",1)[1] 
                tos = to.replace(' ','').split(":",1)[1] 
                froms = from_mail.replace(' ','').split(":",1)[1]
                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.ehlo()
                        smtp.login(usernames,passwords)
                        msg = f'Subject:{Subjects_mail}\n\n{bodys}'
                        smtp.sendmail(froms,tos,msg)
                except Exception as e:
                    print(e)
                    print('Invalid credentials or turn on less secure apps on google account')
                    exit()
                running = False                          
        else:
            resp = MessagingResponse()
            msg = resp.message()
            msg.body('My Response')
            msg.media('https://picsum.photos/200/300?random=1')

        # return the message
        return str(resp) 
                  
    except Exception as e:
        print(e)

    
    

    

if __name__ == "__main__":
    app.run(debug=True) 
