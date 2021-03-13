# Description
### Telegram bot to receive notifications about the current status of homework review in Yandex.Praktikum

# Run
### To install on a local computer, you must:
* Download project files from the repository or clone it: https://github.com/nNDVG/api_sp1_bot.git
* Create your telegram bot at the godfather bot 
* Register on the Heroku website: https://heroku.com/
* Click on the tab "Nev"
* Click "Create new app"
* Here give a name to your app and select a suitable region
* Then choose to place with github and follow the instructions
* After placement, go to the application settings and go to specify the following variables in the "Config Vars" section:
 - PRACTICUM_TOKEN:  your token from prakticum
 - TELEGRAM_TOKEN : token your telegram bot
 - CHAT_ID: your telegram chat ID 

# Author
 - https://github.com/nNDVG/
 - https://hub.docker.com/u/ndvg/

# Tech stack:
* Python
* Python-dotenv
* Python-telegram-bot
