import csv
import json
from config import FinhubAPI
from flask import Flask, render_template
import requests

app = Flask(__name__)


def human_format(num):
    """Gets a number and formats the number to a String that is easier to read"""

    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def init_data():
    """ Api call for the COVID-19 info and returns a list of dictionaries """
    url = 'https://finnhub.io/api/v1/covid19/us?'
    r = requests.get(url, params={'token': FinhubAPI})
    not_state_lst = ['Veteran Affair', 'Federal Bureau of Prisons', 'US Military', 'Northern Mariana Islands',
                     'Wuhan Evacuee', 'US Virgin Islands', 'Diamond Princess', 'Guam', 'Grand Princess',
                     'Navajo Nation', 'Puerto Rico', 'Washington, D.C.']
    states_dict = json.loads(r.text)
    states_lst = list()
    csv_lst = list()
    end_data = {'min_cases': states_dict[0]["case"], 'min_cases_name': states_dict[0]["state"],
                'min_deaths': states_dict[0]['death'], 'min_deaths_name': states_dict[0]["state"], 'most_cases': -1,
                'most_cases_name': 'ERROR', 'most_deaths': -1, 'most_deaths_name': 'ERROR'}
    total_lst = [0, 0]
    for state in states_dict:
        if state["state"] not in not_state_lst:
            state_name = state["state"]
            state_cases = state["case"]
            state_deaths = state["death"]
            total_lst[0] = total_lst[0] + state_deaths
            total_lst[1] = total_lst[1] + state_cases
            states_lst.append((state_name, human_format(state_cases), human_format(state_deaths)))
            csv_lst.append({'State': state_name, 'Cases': state_cases})
            if state_cases < end_data['min_cases']:
                end_data['min_cases'] = state_cases
                end_data['min_cases_name'] = state_name
            elif state_cases > end_data['most_cases']:
                end_data['most_cases'] = state_cases
                end_data['most_cases_name'] = state_name
            if state_deaths < end_data['min_deaths']:
                end_data['min_deaths'] = state_deaths
                end_data['min_deaths_name'] = state_name
            elif state_deaths > end_data['most_deaths']:
                end_data['most_deaths'] = state_deaths
                end_data['most_deaths_name'] = state_name
    states_lst.sort()
    total_lst_format = list()
    end_data_format = dict()
    for i in total_lst:
        total_lst_format.append(human_format(i))
    for end in end_data:
        if isinstance(end_data[end], int):
            end_data[end] = human_format(end_data[end])
    csv_columns = ['State', 'Cases']
    csv_file = "csvs/states.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in csv_lst:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    return states_lst, total_lst_format, end_data


@app.route('/index')
@app.route('/')
def hello_world():
    states_lst, total_lst_format, end_data = init_data()
    return render_template('index.html', states_lst=states_lst, total_lst_format=total_lst_format, end_data=end_data)


if __name__ == '__main__':
    app.run(debug=True)
