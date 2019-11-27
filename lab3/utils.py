import matplotlib.pyplot as mpl_p
import numpy as np
import pandas as pd


FETCH = 'http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg'
COMMON = {
    'action': 'show',
    'tvd': '27820001217417', 'vrn': '27820001217413',
    'region': '78', 'sub_region': '78', 'prver': '0'
}


def voters_percent_in_time(x, label):
    protocol = [10.00, 12.00, 15.00, 18.00]
    mpl_p.bar(protocol, x, width=1, color='green')
    mpl_p.title(label)
    for i in protocol:
        mpl_p.text(i - 0.8, x[protocol.index(i)] + 3.2, str(x[protocol.index(i)]) + '%')
    mpl_p.xlabel('Time')
    mpl_p.ylabel('Voters percent, %')
    mpl_p.xlim([0, 23])
    mpl_p.ylim([0, 100])
    mpl_p.yticks(np.arange(0, 101, 10))
    mpl_p.xticks(np.arange(0, 24, 1))
    mpl_p.show()


def least_sqr_method(x, y):  # y = ax + b
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    (x_min, x_max) = (min(x), max(x))
    (x2, xy) = (0, 0)
    ls = np.linspace(x_min, x_max)
    for i in range(0, len(x)):
        xy += x[i] * y[i]
    for i in range(0, len(x)):
        x2 += pow(x[i], 2)
    a = (len(x) * xy - np.sum(x) * np.sum(y)) / (len(x) * x2 - pow(np.sum(x), 2))
    b = (np.sum(y) - a * np.sum(x)) / len(x)
    return a, b, ls


def valid_voters_plot(x, y, label):
    mpl_p.scatter(x, y, linewidths=1, c="white", edgecolors='green')
    mpl_p.title(label)
    mpl_p.xlabel('Valid sheets')
    mpl_p.ylabel('Voters percent')
    mpl_p.show()


def votes_dependencies(attendance, candidates):
    for candidate in candidates:
        a, b, ls = least_sqr_method(attendance, candidate['data'])
        mpl_p.plot(ls, a * ls + b, color=candidate['color'])
    for candidate in candidates:
        mpl_p.scatter(attendance, candidate['data'], color=candidate['color'], s=10, label=candidate['label'])
    mpl_p.xlabel('Attendance percent, %')
    mpl_p.ylabel('Voters percent, %')
    mpl_p.legend()
    mpl_p.show()


def compile_query(query_dict):
    (result, index) = ('', 0)
    for key in query_dict:
        result += (key + '=' + query_dict[key])
        index += 1
        if index <= len(query_dict.keys()) - 1:
            result += '&'
    return '?' + result


def get_data(query):
    return pd.read_html(FETCH + compile_query(query), encoding='CP1251')