import numpy as np
import utils


query = {'type': '454', 'vibid': '27820001217419'}
summary_query = {'type': '222', 'vibid': '27820001217419'}
query.update(utils.COMMON)
summary_query.update(utils.COMMON)
page = utils.get_data(query)
summary_page = utils.get_data(summary_query)
header = page[6].drop([0, 1, 2]).T.iloc[1].reset_index(drop=True)
per_time = page[6].drop([0, 1, 2]).T.drop([0, 1]).T.reset_index(drop=True)
per_time = np.array(per_time)
summary = summary_page[7].drop([0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]).reset_index(drop=True)
summary = np.array(summary)
(attendance_array, valid_sheets) = ([], [])
candidates_collection = [
    {'label': 'Беглов', 'color': 'red', 'data': summary[3]},
    {'label': 'Амосов', 'color': 'blue', 'data': summary[2]},
    {'label': 'Тихонова', 'color': 'green', 'data': summary[4]}
]
for k in range(0, len(per_time)):
    for i in range(1, 5):
        per_time[k, i] = float(per_time[k, i].replace('%', ''))
        if i != 1:
            per_time[k, i] = round(per_time[k, i] + per_time[k, i - 1], 2)
for i in range(0, 3):
    utils.voters_percent_in_time(per_time[i, 1:], header[i])
for i in summary[1]:
    valid_sheets.append(int(i))
for candidate in candidates_collection:
    for index, j in enumerate(candidate['data']):
        candidate['data'][index] = float(j.split(' ')[1].replace('%', ''))
    utils.valid_voters_plot(valid_sheets, candidate['data'], candidate['label'])
for i in range(0, len(per_time)):
    attendance_array.append(per_time[i, 4])
utils.votes_dependencies(attendance_array, candidates_collection)