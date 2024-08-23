from sys import argv
import datetime
import json
import gspread
import requests
import pandas as pd
import unicodedata


now = datetime.datetime.today()
start = now - datetime.timedelta(days=43)
curr_interval = f'{start.strftime("%m/%d")} - {now.strftime("%m/%d")}'


def normalize_unicode_to_ascii(unicode_string):
    return unicodedata.normalize('NFD', unicode_string).encode('ascii', 'ignore').decode('ascii')


def get_attendance_for_raids(config, known_player_alts):
    guild_reports_url = 'https://vanilla.warcraftlogs.com/v1/reports/guild/Tenple/Mankrik/US?api_key=' + config['wcl_api_key']
    reports = requests.get(guild_reports_url).json()
    output = {}
    for report in config['guild_report_ids']:
        report_info = [item for item in reports if item['id'] == report][0]
        for raid in ['MC', 'BWL', 'Naxx', 'AQ40']:
            if raid in report_info['title']:
                report_raid = raid
                break
        end = report_info['end']
        res = requests.get(
            f'https://www.warcraftlogs.com:443/v1/report/tables/summary/{report}?end={end}&api_key={config["wcl_api_key"]}'
        )
        attendees = [normalize_unicode_to_ascii(item['name']) for item in res.json()['composition']]
        attendees = list(set(attendees + config['bench'].get(raid, [])))
        attendees = [known_player_alts[attendee] if attendee in known_player_alts else attendee for attendee in attendees]
        output[report_raid] = { attendee: 1/float(len(config['guild_report_ids'])) for attendee in attendees }
    return output


def get_attendance_for_raid_outside_guild(config, known_player_alts, num_raids=1):
    user_reports_url = f'https://vanilla.warcraftlogs.com:443/v1/reports/user/{config["non_guild_user"]}?api_key={config["wcl_api_key"]}'
    reports = requests.get(user_reports_url).json()
    output = {}
    report_info = [item for item in reports if item['id'] == config["non_guild_report_id"]][0]
    end = report_info['end']
    res = requests.get(
        f'https://www.warcraftlogs.com:443/v1/report/tables/summary/{config["non_guild_report_id"]}'
        f'?end={end}&api_key=1ed54401421146e653b0e95e3eb575f6'
    )
    attendees = [normalize_unicode_to_ascii(item['name']) for item in res.json()['composition']]
    attendees = list(set(attendees + config['bench'].get(config['non_guild_raid_name'], [])))
    attendees = [known_player_alts[attendee] if attendee in known_player_alts else attendee for attendee in attendees]
    output[config['non_guild_raid_name']] = { attendee: 1/float(num_raids) for attendee in attendees }
    return output


def update_per_raid_attendance(raid_date, new_attendance_dict, sh):
    for raid in ['Naxx', 'AQ40', 'BWL']:
        sheet_name = raid + ' Attendance'
        summary_sheet_name = raid + ' Summary - 6 weeks'
        worksheet = sh.worksheet(sheet_name)
        dataframe = pd.DataFrame(worksheet.get_all_records())
        if raid in new_attendance_dict:
            raid_df = pd.DataFrame(new_attendance_dict[raid].items())
            raid_df.columns = ['Character', raid_date]
            try:
                merged = raid_df.merge(dataframe, how='outer', on='Character').fillna(0)
                dataframe = merged.sort_values('Character')
                #dataframe.insert(1, raid_date, new_list, allow_duplicates=False)
                worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
                print(f'{sheet_name} updated')
            except ValueError:
                print(f'No updates for {sheet_name}')
                pass

        keep = ['Character'] + [col for col in dataframe.columns[1:] if datetime.datetime.strptime(col, '%Y-%m-%d') > start]
        new_df = dataframe.filter(keep, axis=1)
        raid_count = sum(new_df.max(axis=0, numeric_only=True))
        print(raid_count, raid)
        attended = new_df.sum(axis=1, numeric_only=True)
        six_week_summ = pd.DataFrame(
            {
                'Character': new_df['Character'], 
                'Raid Count': [raid_count for i in range(len(new_df['Character']))],
                'Raid Attended': attended,
                'Attendance Pct': [i*100/float(raid_count) for i in attended]
            }
        )
        df2 = six_week_summ.sort_values(['Attendance Pct', 'Character'], ascending=[False, True])
        summ_sheet = sh.worksheet(summary_sheet_name)
        summ_sheet.update([df2.columns.values.tolist()] + df2.values.tolist())
        summ_sheet.update_cell(1,6, f'{start.strftime("%m/%d")} - {now.strftime("%m/%d")}')
        print(f'{summary_sheet_name} updated with latest attendance info')


def main():

    with open(argv[1]) as config_file:
        config_dict = json.load(config_file)

    with open(argv[2]) as alts_file:
        alts_dict = json.load(alts_file)

    result = get_attendance_for_raids(config_dict, alts_dict)

    gc = gspread.oauth()
    sh = gc.open(config_dict['attendance_file_name'])

    update_per_raid_attendance(config_dict['raid_date'], result, sh)

    naxx_all = sh.worksheet("Naxx Attendance")
    aq40_all = sh.worksheet("AQ40 Attendance")
    bwl_all = sh.worksheet("BWL Attendance")
    mc_all = sh.worksheet("MC Attendance")
    naxx_six = sh.worksheet("Naxx Summary - 6 weeks")
    aq40_six = sh.worksheet("AQ40 Summary - 6 weeks")
    bwl_six = sh.worksheet("BWL Summary - 6 weeks")
    #mc_six = sh.worksheet("MC Summary - 6 weeks")

    max_val_all = 0
    for sheet in [naxx_all, aq40_all, bwl_all, mc_all]:
        df = pd.DataFrame(sheet.get_all_records())
        max_val_all += sum(df.max(axis=0, numeric_only=True))
    total_raids = round(max_val_all)

    max_val_6w = 0
    for sheet in [naxx_six, aq40_six, bwl_six]:
        df = pd.DataFrame(sheet.get_all_records())
        max_val_6w += max(df['Raid Count'])
        #cols_list = sheet.row_values(1)
        #max_val = sum(float(val) for val in [max(sheet.col_values(i)[1:]) for i in range(2, len(cols_list)+1)])
        #max_val_all += max_val
    total_raids_6w = round(max_val_6w)

    naxx_dict = naxx_all.get_all_records()
    aq40_dict = aq40_all.get_all_records()
    bwl_dict = bwl_all.get_all_records()
    mc_dict = mc_all.get_all_records()
    naxx_6w_dict = naxx_six.get_all_records()
    aq40_6w_dict = aq40_six.get_all_records()
    bwl_6w_dict = bwl_six.get_all_records()
    #mc_6w_dict = mc_six.get_all_records()

    new_dict_all = {}

    for attendance_dict in [naxx_dict, aq40_dict, bwl_dict, mc_dict]:
        for char_dict in attendance_dict:
            if char_dict['Character'] not in new_dict_all:
                new_dict_all[char_dict['Character']] = {
                    'Character': char_dict['Character'], 
                    'Raid Count': total_raids,
                    'Raid Attended': 0,
                    'Attendance Pct': 0
                }
            attendance_val = sum([v for v in char_dict.values() if not isinstance(v, str)])
            new_dict_all[char_dict['Character']]['Raid Attended'] += attendance_val
            new_dict_all[char_dict['Character']]['Attendance Pct'] += attendance_val*100/float(total_raids)

    for attendance_dict in [naxx_6w_dict, aq40_6w_dict, bwl_6w_dict]:
        for char_dict in attendance_dict:
            if char_dict['Character'] not in new_dict_all:
                print('CHARACTER NOT FOUND')
            new_dict_all[char_dict['Character']].setdefault('Raid Attended (6w)', 0)
            new_dict_all[char_dict['Character']].setdefault('Raid Count (6w)', total_raids_6w)
            new_dict_all[char_dict['Character']]['Raid Attended (6w)'] += char_dict['Raid Attended']
            
    for k in new_dict_all.keys():
        new_dict_all[k]['Raid Attended'] = round(new_dict_all[k]['Raid Attended'], 2)
        try:
            new_dict_all[k]['Raid Attended (6w)'] = round(new_dict_all[k]['Raid Attended (6w)'], 2)
            new_dict_all[k]['Attendance Pct (6w)'] = new_dict_all[k]['Raid Attended (6w)']*100/float(total_raids_6w)
        except Exception:
            new_dict_all[k]['Raid Attended (6w)'] = 0
            new_dict_all[k]['Raid Count (6w)'] = total_raids_6w
            new_dict_all[k]['Attendance Pct (6w)'] = 0

    final_df = pd.DataFrame(list(new_dict_all.values()))

    final_df2 = final_df[
        ['Character', 'Raid Count (6w)', 'Raid Attended (6w)', 'Attendance Pct (6w)', 'Raid Count', 'Raid Attended', 'Attendance Pct']
    ]
    final_df2 = final_df2.sort_values(['Attendance Pct (6w)', 'Attendance Pct'], ascending=[False, False])

    final_sheet = sh.worksheet("Scheduled Raid Attendance - 6 weeks")
    final_sheet.update(final_df2.values.tolist(), 'A3')

    final_sheet.update([['Rolling 6 Week Attendance ' + curr_interval]], 'B1')


main()