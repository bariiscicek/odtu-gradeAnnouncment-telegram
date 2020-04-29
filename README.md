### METU Grade Announcement System with Telegram

An application that sends grades of courses as a telegram message using telegram bot.
User get notifications about exam grades when they are announced.

Requirements:
```console
$ pip install pyTelegramBotAPI
```

Step-by-step Guide for Telegram bot

- Download and install Telegram application to your smart phone.
- Search for @BotFather and type /start
- Type /newbot and follow insturctions. And then, your bot token is created. Keep that token secretly.

Now our Telegram bot is ready. Its time to insert users to the system..


- Edit *checkGrades.py*, *fileInitializer.py*, *recordUsers.py* to change Telegram bot token
- Run all files using **crontab**

**That code will open crontab console**
```console
$ sudo nano /etc/crontab
```
**Insert code below into the console**
```console
0,30 * * * * root python3 checkGrades.py
5 */3 * * * root python3 recordUsers.py
10 */3 * * * root python3 fileInitializer.py
```

Now, we can wait for user input on Telegram Application.

Users can login the system with sending message to the telegram bot. Message format should be like *userid password*. For example *e222222 barissifre*

- The system checks new grades for every 30 minutes. Frequency may be changed using crontab.
