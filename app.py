import json
from config import FinhubAPI
from flask import Flask, render_template
import requests

app = Flask(__name__)


def human_format(num):
    """Gets a number and formats the number to a String that is easier to read"""
    num = float(num)
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def init_data():
    """ Api call for the COVID-19 info, returns list of tuples with state, cases, deaths
    and returns dict with min/max/total cases and deaths """
    not_state_lst = ['Veteran Affair', 'Federal Bureau of Prisons', 'US Military', 'Northern Mariana Islands',
                     'Wuhan Evacuee', 'US Virgin Islands', 'Diamond Princess', 'Guam', 'Grand Princess',
                     'Navajo Nation', 'Puerto Rico', 'Washington, D.C.']
    url = 'https://finnhub.io/api/v1/covid19/us?'
    r = requests.get(url, params={'token': FinhubAPI})
    states_dict = json.loads(r.text)
    states_lst = [(x['state'], x['case'], x['death']) for x in states_dict if
                  x['state'] not in not_state_lst]
    states_lst.sort()
    cases_lst = [(x[1], x[0]) for x in states_lst]
    death_lst = [(x[2], x[0]) for x in states_lst]
    death_only_lst = [x[0] for x in death_lst]
    case_only_lst = [x[0] for x in cases_lst]
    end_data = {'min_cases': min(cases_lst)[0], 'min_cases_name': min(cases_lst)[1],
                'min_deaths': min(death_lst)[0], 'min_deaths_name': min(death_lst)[1], 'most_cases': max(cases_lst)[0],
                'most_cases_name': max(cases_lst)[1], 'most_deaths': max(death_lst)[0],
                'most_deaths_name': max(death_lst)[1],
                "total_cases": sum(case_only_lst), "total_deaths": sum(death_only_lst)}
    return states_lst, end_data


states_lst, end_data = init_data()


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html', states_lst=states_lst, end_data=end_data,
                           human_format=human_format)


@app.route('/charts')
def charts():
    return render_template("charts.html", states_lst=states_lst, end_data=end_data,
                           human_format=human_format)


if __name__ == '__main__':
    app.run(debug=True)
