# <p align="center"><img src="https://github.com/Mc0Shell/FaceCrypt/assets/55066055/1979ac47-79c7-4569-a10a-f376d9b22571" alt="Image" width="400" height="400"></p>

Secure Login and File Encryption Program

This is a secure login and file encryption program that allows users to log in using their face, hand gesture, password, and optional pin via a TUI (Text-based User Interface). 
Once logged in, users can encrypt and decrypt files and folders using their login credentials.

--------------------------------------------------------------------------------

<b>STATUS</b>: Under developing

   Next update: 
   
   - Auth Config section
   - More hand gesture
   - More speed

--------------------------------------------------------------------------------

<b>FEATURES</b>

   - Secure login using face, hand gesture, password, and optional pin
   - Encrypt and decrypt files and folders using login credentials
   - Lightweight and fast performance
   - Inline shell parameters options added (Fast crypt/decrypt)
    
    
--------------------------------------------------------------------------------

<b>HOW IT WORKS</b>

   The program works by combining the facial recognition and hand gesture data with the user's password to generate a unique key that is used to encrypt and decrypt the user's files.

   When a user logs in, the program captures their face and hand gesture data and combines it with their password using a one-way hashing algorithm. 
   This creates a unique, encrypted key that is used to encrypt and decrypt the user's files.

--------------------------------------------------------------------------------

<b>INSTALLATION</b>

To install and use this program, follow these steps:

   Clone the repository to your local machine

    git clone https://github.com/Mc0Shell/FaceCrypt.git

   Install the required dependencies

    pip3 install -r requirements.txt
    
  
--------------------------------------------------------------------------------

<b>USAGE</b>

   To start the program, open a terminal or command prompt and navigate to the directory where you have cloned the repository. 
   Then, run the following command:

    python3 face_login.py

   When you first run the program, you will be prompted to create a new account. 
   You will need to provide your name, your face, a hand gesture, a password, and an optional pin. 
   These will be used for your secure login credentials.

   Once you have created your account, you can log from the main menu with face and optional hand gesture. 
   You will be prompted to enter your password and, if you have set up a pin, your pin as well.

   Once you have successfully logged in, you can encrypt and decrypt files and folders using the "Encryption" and "Decryption" options from the main menu.
   
   For a fast usage:
   
      python3 face_login.py -p /User/user/Documents/FolderToCrypt -t crypt -k folder
      
   or
   
      python3 face_login.py -p /User/user/Documents/FileToCrypt.txt -t crypt -k file
      
   All options:
   
      -p -> Folder/File Path
      -t -> Method Type [crypt/decrypt]
      -k -> Data type [folder/file]

--------------------------------------------------------------------------------

![Istantanea_2023-04-13_19-20-29](https://user-images.githubusercontent.com/55066055/232245851-6e75761a-f14b-4592-b0f5-b40020500a63.png)

![Istantanea_2023-04-13_18-34-26](https://user-images.githubusercontent.com/55066055/231826250-d3cb4e81-c0c2-419b-95b9-104805710592.png)

--------------------------------------------------------------------------------
<b>Credits</b>

This program was developed by Mc0Shell.




