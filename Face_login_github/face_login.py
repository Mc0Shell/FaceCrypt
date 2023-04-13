import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import getch
import json
from termcolor import colored
import face_recognition
import cv2
import numpy as np
import time
import mediapipe as mp
import tensorflow as tf
tf.get_logger().setLevel('INFO')
from tensorflow.keras.models import load_model
import hashlib
from tkinter import Tk, filedialog
from cryptography.fernet import Fernet
from os import path
import codecs
import magic
import concurrent.futures
from tqdm import tqdm
from progress.bar import PixelBar
import subprocess



key = b'Kuc11VOV_igMzl1z0bGh2NBegtBfaNPdkrKAQmQ-iUE=' # DON'T EDIT
fernet = Fernet(key)

rootTK = Tk()
rootTK.withdraw()
rootTK.attributes('-topmost', True)
video_capture = cv2.VideoCapture(0)
    
#Global var
pincheck = "n"
password = ""
hand = ""
pin = ""
userData = None
checkPassword = ""

# This allow you to use the program skipping the login phase
# True for bypass
bypassVerification = False
# Your login password
bypassPassword = "<your-password>"


banner = """
   __________________________________________________________________________________________
  |                                                                                          |
  |  @@@@@@@@   @@@@@@    @@@@@@@  @@@@@@@@   @@@@@@@  @@@@@@@   @@@ @@@  @@@@@@@   @@@@@@@  |
  |  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@ @@@  @@@@@@@@  @@@@@@@  |
  |  @@!       @@!  @@@  !@@       @@!       !@@       @@!  @@@  @@! !@@  @@!  @@@    @@!    |
  |  !@!       !@!  @!@  !@!       !@!       !@!       !@!  @!@  !@! @!!  !@!  @!@    !@!    |
  |  @!!!:!    @!@!@!@!  !@!       @!!!:!    !@!       @!@!!@!    !@!@!   @!@@!@!     @!!    |
  |  !!!!!:    !!!@!!!!  !!!       !!!!!:    !!!       !!@!@!      @!!!   !!@!!!      !!!    |
  |  !!:       !!:  !!!  :!!       !!:       :!!       !!: :!!     !!:    !!:         !!:    |
  |  :!:       :!:  !:!  :!:       :!:       :!:       :!:  !:!    :!:    :!:         :!:    |
  |   ::       ::   :::   ::: :::   :: ::::   ::: :::  ::   :::     ::     ::          ::    |
  |   :         :   : :   :: :: :  : :: ::    :: :: :   :   : :     :      :           :     |
  |                                                                                          |
  |                                                                      by Mc0Shell         |
  |__________________________________________________________________________________________|
  
"""         

class UserData:
    password = ""
    hand = ""
    pin = ""

    def __init__(self):
        self.password = password
        self.hand = hand
        self.pin = pin

# Password encode: sha1(md5(password))
def hashPassword(passw):
    return hashlib.sha1((hashlib.md5(passw.encode()).hexdigest()).encode()).hexdigest()

def printMenu(stage):
    with open('json_data/config.json', 'r') as f:
        data = json.load(f)
        
    if(data['config_data']['face'] == "Saved" and data['config_data']['password'] == "Saved" and data['config_data']['hand'] == "Saved"):
        configType = colored("  Valid config", "green")
    else:
        configType = colored("Invalid config", "red")

    pinStatus = pinStatus = "  "+data['config_data']['passwordPin'] if data['config_data']['passwordPin'] == "Active" else data['config_data']['passwordPin']

    menu = """
         _________________________       _______________________________________________
        |                         |     |   # Current Config    |                       |
        |    """+colored("[1]", "cyan")+""" Crypt            |     |_______________________|   """+configType+"""      |
        |    """+colored("[2]", "cyan")+""" Decrypt          |     |                                               |
        |    """+colored("[3]", "cyan")+""" Auth Config      |     | Face:      """+data['config_data']['face']+""" | Count:        """+str(data['config_data']['faceCount'])+"""            |
        |                         |     | Password:  """+data['config_data']['password']+""" | PIN(3F):      """+pinStatus+"""     |
        |    """+colored("[Q]", "red")+""" Quit             |     | Hand:      """+data['config_data']['hand']+""" | Gestures n°:  """+str(data['config_data']['gesturesN'])+"""            |
        |_________________________|     |_______________________________________________|
    """   
    
    menuS1 = """
         _________________________       _______________________________________________
        |                         |     |   # Current Config    |                       |
        |    """+colored("[1]", "cyan")+""" Folder           |     |_______________________|   """+configType+"""      |
        |    """+colored("[2]", "cyan")+""" File             |     |                                               |
        |                         |     | Face:      """+data['config_data']['face']+""" | Count:        """+str(data['config_data']['faceCount'])+"""            |
        |                         |     | Password:  """+data['config_data']['password']+""" | PIN(3F):      """+pinStatus+"""     |
        |    """+colored("[3]", "red")+""" Back             |     | Hand:      """+data['config_data']['hand']+""" | Gestures n°:  """+str(data['config_data']['gesturesN'])+"""            |
        |_________________________|     |_______________________________________________|
    """
    
    match stage:
        case 1:
            print(menu)
        case 2:
            print(menuS1)
    
def getPress():
    print("         => ", end='', flush=True)
    action = getch.getch()
    print(action, end='', flush=True)
    return action
    
def faceInitData():
    nC = 0
    
    face_names = []
    process_this_frame = True

    while True:
        faces_data = []
        face_locations = []
        face_encodings = []
        ret, frame = video_capture.read()
    
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            face_encoding = face_recognition.face_encodings(frame)
            try:
                faces_data.append(face_encoding[0])
            except:
                continue
    
        process_this_frame = not process_this_frame
    
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 5
            left *= 4
    
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
        if(nC == 50):
            break
        else:
            nC += 1
    
    med_array = []
    
    for arrayN in faces_data:
        if len(list(med_array)) == 0:
            med_array = arrayN
        else:
            med_array = map(sum, zip(med_array, arrayN))
    
    video_capture.release()
    cv2.destroyAllWindows()
    
    return list(med_array)

def handRecognize(gesture):

    # initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    
    # Load the gesture recognizer model
    model = load_model('mp_hand_gesture')
    
    # Load class names
    f = open('hand_data/gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()
    
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    nC = 0
    nS = 0
    
    while True:
        _, frame = cap.read()
        x, y, c = frame.shape
    
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        result = hands.process(framergb)
    
        className = ''
    
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    #print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
    
                    landmarks.append([lmx, lmy])
    
    
                # Predict gesture
                prediction = model.predict([landmarks], verbose=0)
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]      
            
        if(gesture in classNames):
            if className == gesture:
                if(nC == 50):
                    break
                elif(nC == 1):
                    print(colored("\n      Recognized gesture ("+gesture+"), remain still in this position", "cyan"))
                    
                nC += 1
        elif(className != ""):
            if(hashPassword(className) == gesture):
                if(nC == 15):
                    break
                else:
                    nC += 1
            elif(nS == 15):
                return False
            nS += 1
        
    
    cap.release()
    cv2.destroyAllWindows()
    
    return True
    
    

def checkPIN(pin):
    check = 0
    errorString = ""

    if len(pin) == 4:
        check += 1
        if pin.isdigit():
            check += 1
        else:
            errorString = "PIN must contain only digits"
    else:
        errorString = "PIN must be 4 digits long"
        
    if(check == 2):
        return True, errorString
    else:
        return False, errorString


def showFirstConfig():
    global pincheck
    os.system('clear')
    print(banner)
    print(colored("  # Initial configuration", "magenta"))
    print("  ↳ ", end='')
    print(colored("# Face data info", "magenta"))
    print("    ↳ ", end='')
    print(colored("Watch the camera for scanning, slowly move the head in each direction (360°).\n      Press ENTER to start", "cyan"))
    getch.getch()
    
    faceData = faceInitData()
    
    print(colored("      ✓ Face model created", "green"))
    
    with open('json_data/config.json', 'r') as f:
        data = json.load(f)
        
    if(faceData == []):
        print(colored("      X Error during face scanning, restart the program", "red"))
        quit()
        
    with open('json_data/config.json', 'w') as f:
        data['faces_data']['main'] = faceData
        json.dump(data, f, indent=4)
    
    print(colored("      ✓ Face data collected", "green"))
    
    print(colored("\n    # Password selection", "magenta"))
    
    global password
    global pin
    global hand
    while not password:
        print("    ↳ ", end='', flush=True)
        password = input()
        
        if(len(password) == 0):
            print(colored("      X Password error: Empty field", "red"))
        else:
            print(colored("      ✓ Password stored", "green"))
    
    pincheck = input(colored("\n      Add extra PIN? (4 numbers) [Y/n]: ", "blue"))
    if(pincheck == 'y' or pincheck == 'Y'):
        c = False
        while not c:
            pin = input("      ↳ ")
            
            c, error = checkPIN(pin)
            
            if(c):
                print(colored("        ✓ PIN stored", "green"))
            else:
                print(colored("        X PIN error: " + error, "red"))
                
    print(colored("\n    # Hand gesture selection (3FA)", "magenta"))
    hand = ""
    while not hand:
        
        print("""
     [1] 'Ok'        [4] 'Live long'
     [2] 'Peace'     [5] 'Thumbs up'
     [3] 'Rock'      [6] 'Thumbs down'
        """)
    
        print("    ↳ ", end='', flush=True)
        hand = input()
        
        if(hand.isdigit()):
            if(not hand):
                print(colored("      X Hand gesture error: Empty field", "red"))
            elif(int(hand) < 1 or int(hand) > 6):
                print(colored("      X Hand gesture error: Invalid choice", "red"))
            else:
                print(colored("\n      Perform the gesture in front of the camera.\n      Press ENTER to start\n\n", "cyan"))
                break
        else:
            print(colored("      X Hand gesture error: must use only digits", "red"))
        
    if(hand == '1'):
        hand = "okay"
    elif(hand == '2'):
        hand = "peace"
    elif(hand == '3'):
        hand = "rock"
    elif(hand == '4'):
        hand = "live long"
    elif(hand == '5'):
        hand = "thumbs up"
    elif(hand == '6'):
        hand = "thumbs down"
        
    check = handRecognize(hand)
    
    if(check):
        print(colored("      ✓ Hand data collected", "green"))
    else:
        print("error")
        
    # End of config
    print(colored("\n\n  # ALL DATA SAVED SUCCESSFULLY", "green"))
    print("    ↳ Configuration summary:", end='', flush=True)
    print("""
    
        Face data:  ✓
        Hand data:  ✓ ("okay")
        Password:   ✓ sha1(md5("""+password[0]+password[1]+"""...))
        PIN:        ✓ sha1(md5("""+pin+"""))   
    
    """)
    print(colored("\n\n  # Final step", "magenta"))
    print("    ↳ Confirm the configuration? [Y/n]", end='', flush=True)
    print(colored("\n      You can modify the data when you want", "cyan"))
    l = input("      ↳ ")
    
    if(l == 'y' or l == 'Y'):
        saveConfigData()
    else:
        quit()

def saveConfigData():
    with open('json_data/config.json', 'r') as f:
        data = json.load(f)
        
    with open('json_data/config.json', 'w') as f:
        data['app_data']['fo'] = False
        data['config_data']['face'] = "Saved"
        data['config_data']['password'] = "Saved"
        data['config_data']['hand'] = "Saved"
        data['config_data']['faceCount'] = 1
        
        if(pincheck == 'y' or pincheck == 'Y'):
            data['config_data']['passwordPin'] = "Active"
        else:
            data['config_data']['passwordPin'] = "Inactive"
            
        data['config_data']['gesturesN'] = 1
        
        data['personal_data']['password'] = hashPassword(password)
        data['personal_data']['handGesture'] = hashPassword(hand)
        data['personal_data']['pin'] = hashPassword(pin)
        
        json.dump(data, f, indent=4)

def faceRecognition():
    nC = 0
    nS = 0
    know_faces_data = []
    known_face_encodings = []
    known_face_names = []
    name = "Unknown"

    with open("json_data/config.json") as f:
        know_faces_data = json.load(f)
    
    for x in range(len(know_faces_data['faces_data'])):
        known_face_encodings.append(know_faces_data["faces_data"]["main"])
        known_face_names.append("Verified User")
    
    face_locations = []
    process_this_frame = True
    
    while True:
        ret, frame = video_capture.read()
    
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
            rgb_small_frame = small_frame[:, :, ::-1]
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
    
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
    
                face_names.append(name)
    
        process_this_frame = not process_this_frame
        ret = ""
        
        if name == "Verified User":
            if(nC == 15):
                ret = True    
            nC += 1
        elif name == "Unknown":
            if(nS == 15):
                ret = False
                break
            nS += 1
                
        if(ret != ""):
            video_capture.release()
            cv2.destroyAllWindows()
            
            return ret
    
def login():
    global bypassVerification

    if not bypassVerification:
        print(colored("                              # Press ENTER to start the login", "magenta"), end='', flush='True')
        getch.getch()
        
        login_frame = """
                             __________________________________________
                            |                                          |
                            |                # LOGIN                   |
                            |                                          |
                            |             Face Check: Checking         |
                            |             Hand Check:                  |
                            |__________________________________________|
        
        """
        
        print(login_frame, flush='True')
        check = faceRecognition()
        
        if(check):
            login_frame = """
                             __________________________________________
                            |                                          |
                            |                # LOGIN                   |
                            |                                          |
                            |             Face Check: """+colored("✓", "green")+"""                |
                            |             Hand Check:                  |
                            |__________________________________________|\n
                            """+colored("# Hand check", "magenta")+"""
                            """+colored("Starting hand recognition, perform your gesture", "cyan")+"""
            """
        else:
            login_frame = """
                             __________________________________________
                            |                                          |
                            |                # LOGIN                   |
                            |                                          |
                            |             Face Check: """+colored("X", "red")+"""                |
                            |             Hand Check:                  |
                            |__________________________________________|\n
                            """+colored("# Access negated", "red")+"""
            """
            
        os.system('clear')
        print(colored(banner, "yellow"), flush='True')
        print(login_frame, flush='True')
        
        if(not check):
            quit(())
            
        with open('json_data/config.json', 'r') as f:
            data = json.load(f)
        
        check2 = handRecognize(data['personal_data']['handGesture'])
        
        if(check2):
            login_frame = """
                             __________________________________________
                            |                                          |
                            |                # LOGIN                   |
                            |                                          |
                            |             Face Check: """+colored("✓", "green")+"""                |
                            |             Hand Check: """+colored("✓", "green")+"""                |
                            |__________________________________________|\n
                            """+colored("↳ Password: ", "magenta")
        else:
            login_frame = """
                             __________________________________________
                            |                                          |
                            |                # LOGIN                   |
                            |                                          |
                            |             Face Check: """+colored("✓", "green")+"""                |
                            |             Hand Check: """+colored("X", "red")+"""                |
                            |__________________________________________|\n
                            """+colored("# Access negated", "red")+"""
            """
        
        os.system('clear')
        print(colored(banner, "yellow"), flush='True')
        print(login_frame, end='', flush='True')
        
        global checkPassword
        checkPIN = ""
        
        if(not check2):
            quit()
        else:
            checkPassword = input()
            
            if(hashPassword(checkPassword) == data['personal_data']['password']):
                if(data['config_data']['passwordPin'] == "Active"):
                    print(colored("                              PIN: ", "magenta"), end='', flush='True')
                    checkPIN = input()
                    if(hashPassword(checkPIN) == data['personal_data']['pin']):
                        print(colored("                              # Access granted\n", "green"), end='', flush='True')
                        print(colored("                              Press ENTER to start: ", "cyan"), end='', flush='True')
                        getch.getch()
                    else:
                        print(colored("                              X Wrong PIN ", "red"), end='', flush='True')
                        quit()
            else:
                print(colored("                              X Wrong password ", "red"), end='', flush='True')
                quit()
                
    return True
    
def userDataLoad():
    global password
    global hand
    global pin
    global userData
    global checkPassword
    global bypassPassword

    with open('json_data/config.json', 'r') as f:
        data = json.load(f)
        
        userData = UserData()
        
        userData.password = data['personal_data']['password']
        userData.clrPassword = checkPassword
        userData.hand = data['personal_data']['handGesture']
        userData.pin = data['personal_data']['pin']
        
    if bypassVerification:
        userData.clrPassword = bypassPassword        

def strToInt(string):
    tmp = []

    for x in range(len(string)):
        tmp.append(int(ord(string[x])))

    return tmp

def intToString(int):
    tmp = []

    for x in range(len(int)):
        tmp.append(str(chr(int[x])))

    return tmp
    
def checkFile(inputFile):
    if os.path.isfile(inputFile):
        return False
    else:
        print(colored("\n                              Error with folder path, press ENTER to retry ", "red"), end='', flush='True')
        return True

def cryptFolder(filePath):
    crArr = []
    tmpPassword = userData.clrPassword

    with open(filePath, 'rb') as f:
        ofile = f.read()
        encrypted = fernet.encrypt(ofile)
    
        crText = strToInt(str(encrypted))
        crPassword = strToInt(tmpPassword)
                    
        crRes = []
        y = 0
                    
        for x in range(len(crText)):
            crRes.append(crText[x] + crPassword[y])
                    
            if y == len(tmpPassword)-1:
                y = 0
            else:
                y = y + 1
                    
        st = ""
        for x in crRes:
            st += str(x) + " "
        st = st[0:-1]
                    

        crArr.append(st)
                            
    with open(filePath, "w") as f:
        f.write(st)
        
    #print(colored("         " + str(os.getpid()) + " - File: " + filePath, "yellow"), flush='True')
                
    f.close()
    
def decryptFolder(filePath):
    tmpPassword = userData.clrPassword

    crPassword = strToInt(tmpPassword)

    with open(filePath, 'r') as f:
        st = f.read()
        crRes = [int(x) for x in st.split()]
                    
        crText = []
        y = 0
                    
        for x in range(len(crRes)):
            crText.append(crRes[x] - crPassword[y])
                    
            if y == len(tmpPassword)-1:
                y = 0
            else:
                y = y + 1
                    
        encrypted = intToString(crText)
        
        string = ""
        
        for char in encrypted:
            string += char
            
        ofile = fernet.decrypt(bytes(string[2:-1], 'utf-8'))
                
    with open(filePath, "wb") as f:
        f.write(ofile)
        
    #print(colored("         " + str(os.getpid()) + " - File: " + filePath, "green"), flush='True')
                
    f.close()

def init():
    global rootTK

    with open('json_data/config.json', 'r') as f:
        data = json.load(f)
        
    if(data['app_data']['fo']):
        showFirstConfig()
    else:
        os.system('clear')
        print(colored(banner, "yellow"))

        if(login()):     
            userDataLoad()
        
            while True: 
                os.system('clear')
                print(colored(banner, "yellow"))
                printMenu(1)
                action = getPress()
                
                if action == 'Q' or action == 'q':
                    quit()
                    
                # TO DO
                # Auth Config section
                if action == '3' or action == '3':
                    continue
                
                os.system('clear')
                print(colored(banner, "yellow"))
                printMenu(2)
                atype = getPress()
                
                fileList = []  
                
                if(atype == '1'):
                    filePath = filedialog.askdirectory()
                    try:
                        data = os.listdir(filePath)
                    except:
                        continue
                elif(atype == '2'):
                    filePath = filedialog.askopenfilename()
                    try:
                        fileList.append(filePath)
                    except:
                        continue
                elif atype == '3':
                    continue
                  
                for root, dirs, files in os.walk(filePath):
                    for file in files:
                        fileList.append(os.path.join(root, file))
                
                print("\n") 
                label = colored("         Processing..", "magenta")
    
                with PixelBar(label, suffix='%(percent)d%%', max = (len(fileList) if atype == '1' else 1)) as bar:
                    for file in fileList:
                        if action == '1':
                            if atype == '1':
                                with concurrent.futures.ProcessPoolExecutor(max_workers=40) as executor:
                                    future = executor.submit(cryptFolder(file))
                                    bar.next()
                            if atype == '2':
                                cryptFolder(file)
                                bar.next()
                        elif action == '2':
                            if atype == '1':
                                with concurrent.futures.ProcessPoolExecutor(max_workers=40) as executor:
                                    future = executor.submit(decryptFolder(file))
                                    bar.next()
                            if atype == '2':
                                decryptFolder(file)
                                bar.next()
                           
                    
                                 
                print(colored("\n         # All data converted successfully", "magenta"))
                print(colored("         Press ENTER to return Menu: ", "cyan"), end='', flush='True')
                getch.getch()
                
    
init()