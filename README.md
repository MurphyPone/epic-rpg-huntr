# epic-rpg-huntr
An auto-grinder for epic-rpg (hopefully not in violation of Discord ToS)

## How to Use:

1. Create a file called `conf.py` as follows: 

```
URL = "URL to the discord server you want to work in"
CHANNEL_NAME = "Name of the channel you want to use, e.g. '#bot-spam'"
USER = "hunter12@aol.com"
PASS  = "hunter12"
OS = "OSX" #Windows users may need to do additional installation for Tesseract / path deifnitions
QUIPS = ["List", "of", "messages", "to send along with the botted commands at 5 min intervals"]
```

2. Install the project requireements via `pip install -r requirements.txt`
3. `python main.py`
4. Modify the main script file accordingly depending on what tier of gathering you want to do.
