# First Raid Updates

### 8/19 Raid

#### Update Alts

Glance over the 8/19 raid log and see if there are any alts not present in the alts.json file. 
The format for adding any is 
```console
    "<alt name>": "<main name>",
    "<alt name>": "<main name>"
```
Make sure spelling and capitalization is correct, but no need for special characters (e.g. use "Acomp" with a normal A).

#### Update Config

Make a copy of the config_test.json and name it `config.json`. 

Edit it to be relevant to the 8/19 raid (but use the test attendance file first). Make sure to save when finished. It should look like:
```console
{
    "attendance_file_name": "Temple Attendance Sheet (Test)",
    "guild_reports": false,
    "guild_report_ids": [],
    "non_guild_report_id": "c8Bxgt3jGY6VzJC4",
    "non_guild_user": "Rapidfountain",
    "non_guild_raid_name": "Naxx",
    "raid_date": "2024-08-19",
    "bench": {
        "Naxx": ["Eurymedon"]
    },
    "wcl_api_key": "<your WCL key>"
}
```

#### Run script against test sheet

In powershell or cmd.exe, navigate to the directory containing the script. 

Run 
```console
python temple_attendance_tracker.py config.json alts.json
```

Take a look at the spreadsheet Temple Attendance Sheet (Test) to make sure it looks how you would expect.

#### Run script against real sheet

Go back into the `config.json` file and edit the attendance file name to `"Temple Attendance Sheet (New)"`. Make sure to save.

Run the script with the same command as before.

### 8/20 Raid

Follow the above instructions as before, but for the 8/20 raid. 

For the config file, you can either edit the same config file that you used before, or if you want to have a record of the info you used
each time you can create a new one. Just make sure not to change the original `config_test.json` file, and remember to refer to the correct
config file when running the script (i.e. `python temple_attendance_tracker.py <correct config file> alts.json`. 

This one is an example of a non-guild linked raid:
```console
{
    "attendance_file_name": "Temple Attendance Sheet (Test)",
    "guild_reports": false,
    "guild_report_ids": [],
    "non_guild_report_id": "KjfZ4Dx7XwYgHcJ1",
    "non_guild_user": "Rapidfountain",
    "non_guild_raid_name": "Naxx",
    "raid_date": "2024-08-20",
    "bench": {
        "Naxx": ["Tonyapples", "Thudsly", "Olgrampy"]
    },
    "wcl_api_key": "<your WCL key>"
}
```
Before running, check on Olgrampy's main/alt names perhaps and add to alts.json if needed. I'm not sure if he's tracked in the sheet already
and who all his alts are.

Then run the script the same as before, first against Test file, then against New file.

