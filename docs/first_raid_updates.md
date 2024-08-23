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
    "guild_reports": true,
    "guild_report_ids": ["c8Bxgt3jGY6VzJC4"],
    "non_guild_report_id": [],
    "non_guild_user": null,
    "non_guild_raid_name": null,
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
python temple-attendance-script.py config.json alts.json
```

Take a look at the spreadsheet Temple Attendance Sheet (Test) to make sure it looks how you would expect.

#### Run script against real sheet

Go back into the `config.json` file and edit the attendance file name to `"Temple Attendance Sheet (New)"`. Make sure to save.

Run the script with the same command as before.
