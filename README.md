# ProjectBAR

Bot in progress.
Current build is just building the fundamentals.

# Setting up Environment
Make sure virtualenv is installed using command `pip install virtualenv`

Run `python -m virtualenv bot-env -p python3.10.10` to create environment (**You must have this version of Python already installed**)

On Linux/Mac, run `source bot-env/bin/activate`

On Windows, run `bot-env\Scripts\activate.bat`

If on Windows Powershell, run `bot-env\Scripts\Activate.ps1`

Once you have confirmed that you are in the virtual environment, run `pip install -U discord.py`

# Starting up the bot
Make sure parameter in `client.run('')` is **YOUR UNIQUE TOKEN.**
Start bot by issuing `py -3 example_bot.py` in command line
