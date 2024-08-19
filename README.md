# temple-attendance-tracker

## Installation

To run this, you will need:

* Python 3.6 or above
* Git, in order to git clone the repository
* A few python packages: requests, gspread, pandas

### Installing python

If you are not sure if you have python installed, you can check by opening a terminal window (use cmd.exe or powershell in Windows) and run
```console
python --version
```
If you get an error, you need to install python.

It is probably easiest to go to the website and install it from there: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Once install has completed, check it is working properly:
```console
python --version
```

### Installing required packages

Installing the required python packages should be pretty simple with pip.

```console
pip install requests
pip install pandas
pip install gspread
```

### Installing git

This is needed to not only clone the repository to begin with, but will also allow you to keep up to date with any future changes.

If you are on Windows and not a developer, there is a good chance Git is not installed. However, you can still check with:
```console
git --help
```
This is another tool that is probably best downloaded from the website: [https://git-scm.com/downloads](https://git-scm.com/downloads)
Git doesn't seem to work well in Powershell without a special package posh-git, at least for me, but I've had success with running this and successive steps on cmd.exe.
Once installed, check that the command works with `git --help`. 

### Cloning the Repo

Navigate to the place where you'd like to download and run the script from, and run
```console
git clone [url]
```

Subsequently, if you ever need to update the script from its source, you can navigate into the temple-attendance-tracker folder and just run
```console
git pull
```

## Credentials

### Warcraft Logs

Sign in to Warcraft Logs. Click your profile icon in the upper right, then click Settings at the bottom of the menu. On the settings page, scroll down to the bottom and there should be 
an API section. Copy the v1 API key and paste it into your config json file as the value for the `"wcl_api_key"` key.

### Google Sheets

Unfortunately, the script had to be registered to google in "testing phase" and so the credentials will expire after one week and will need to be regenerated.

Go to [https://console.cloud.google.com/welcome?project=temple-raid-attendance-v1](https://console.cloud.google.com/welcome?project=temple-raid-attendance-v1) and click on
"APIs and Services" under Quick Access. In the menu on the left-hand side, click "Credentials", then click on "+ Create Credentials" in the bar above the main content. In the options that pop up, select OAuth Client ID. 
In the next window, for Application Type select "Desktop app". For Name, I always call it "Desktop client 1" but i don't think it really matters. When you press create, a pop-up will show with the new credentials.
Don't X out of this immediately, but click the download icon to save a json file. **Save the file to C:\%APPDATA%\gspread\credentials.json**.

To test that the credentials are working, open up a python interpreter in your terminal window by running
```console
python
```
And then run the following commands to authorize your credentials and make sure they are working:
```python
import gspread
gc = gspread.oauth()
sh = gc.open("Temple Attendance Sheet (Test)")
```

#### Regenerating Google Credentials

After 7 days, your google credentials will expire. When this happens, first go to C:\%APPDATA%\gspread\credentials.json and delete the authorized_user file. You can then follow the steps above to create new credentials
and save them to the same location.


## Running the Script
