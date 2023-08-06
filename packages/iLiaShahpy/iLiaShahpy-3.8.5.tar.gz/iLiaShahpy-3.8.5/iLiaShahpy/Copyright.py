from datetime import datetime
import pytz
from time import sleep
import os

class copyright:
        	red = '\033[91m'
        	green = '\033[92m'
        	blue = '\033[94m'
        	yellow = '\033[93m'
        	magenta = '\033[95m'
        	cyan = '\033[96m'
        	white = '\033[97m'
        	bold = '\033[1m'
        	underline = '\033[4m'
        	black='\033[30m'
        	ir = pytz.timezone("Asia/Tehran")
        	time = f"{datetime.now(ir).strftime(f'{yellow}[{magenta}%H:%M:%S{yellow}]')}"
        	CopyRight = print(f"""{bold}
{white} 〔༄〕- {cyan} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵𝗽𝘆 {magenta} 𝗩𝗲𝗿𝘀𝗶𝗼𝗻  {yellow}3.8.5    

{white} 〔༄〕- {cyan} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵𝗽𝘆 {magenta} 𝙲𝚘𝚙𝚢𝚁𝚒𝚐𝚑𝚝 (𝙲) {yellow} 2023 {red} 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵   

{white} 〔༄〕- {cyan} 𝗥𝘂𝗯𝗶𝗸𝗮{magenta} 𝗖𝗵𝗮𝗻𝗲𝗹𝗹  {yellow} @𝚂𝚘𝚞𝚛𝚜𝚎_𝚙𝚢

{white} 〔༄〕- {cyan} 𝗧𝗶𝗺𝗲 {magenta}{time}

{white}⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁⌁
""")
        	for x in range(3):
              	  for i in ("⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"):
                		sleep(0.1)
                		if x == 10:
                		   print('',end='')
                		   break
                		else:
                			print( magenta+'   𝗟𝗶𝗯𝗿𝗮𝗿𝘆 𝗶𝗟𝗶𝗮𝗦𝗵𝗮𝗵 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁....',cyan+i,end='\r')
        	print(white+"\n")