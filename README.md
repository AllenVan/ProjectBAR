# ProjectBAR

## 1. Install Requirements

Install python requirements with: `pip install -r requirements.txt`

## 2. Setup Token File

Create `credentials/token.json` file and place your bot token in the file:
```
{
    "token": "TOKEN"
}
```

## 3. Setting up Environment
Make sure virtualenv is installed using command `pip install virtualenv`

Run `python -m virtualenv bot-env -p python3.10.10` to create environment (**You must have this version of Python already installed**)

On Linux/Mac, run `source bot-env/bin/activate`

On Windows, run `bot-env\Scripts\activate.bat`

If on Windows Powershell, run `bot-env\Scripts\Activate.ps1`

Once you have confirmed that you are in the virtual environment, run `pip install -U discord.py`

## 4.Starting up the bot
Start bot by issuing `py -3 bar.py` in command line