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
    """ Api call for the COVID-19 info """
    not_state_lst = ['Veteran Affair', 'Federal Bureau of Prisons', 'US Military', 'Northern Mariana Islands',
                     'Wuhan Evacuee', 'US Virgin Islands', 'Diamond Princess', 'Guam', 'Grand Princess',
                     'Navajo Nation', 'Puerto Rico', 'Washington, D.C.']
    url = 'https://finnhub.io/api/v1/covid19/us?'
    r = requests.get(url, params={'token': FinhubAPI})
    states_dict = json.loads(r.text)
    states_lst = [(x['state'], human_format(x['case']), human_format(x['death'])) for x in states_dict if
                  x['state'] not in not_state_lst]
    csv_lst = [{'State': x['state'], 'Cases': x['case']} for x in states_dict if x['state'] not in not_state_lst]
    csv_lst = sorted(csv_lst, key=lambda k: k['State'])
    states_lst.sort()
    cases_lst = [(x['case'], x['state']) for x in states_dict if x['state'] not in not_state_lst]
    death_lst = [(x['death'], x['state']) for x in states_dict if x['state'] not in not_state_lst]
    end_data = {'min_cases': min(cases_lst)[0], 'min_cases_name': min(cases_lst)[1],
                'min_deaths': min(death_lst)[0], 'min_deaths_name': min(death_lst)[1], 'most_cases': max(cases_lst)[0],
                'most_cases_name': max(cases_lst)[1], 'most_deaths': max(death_lst)[0],
                'most_deaths_name': max(death_lst)[1]}
    death_only_lst = [x[0] for x in death_lst]
    case_only_lst = [x[0] for x in cases_lst]
    total_lst = [human_format(sum(death_only_lst)), human_format(sum(case_only_lst))]
    for end in end_data:
        if isinstance(end_data[end], int):
            end_data[end] = human_format(end_data[end])
    return states_lst, total_lst, end_data, csv_lst


# change to have better interchange to html
# combine state list and csv to one by adding human format later
# total to end data
# change colors by average
#add explain comments
#make chart responsive

@app.route('/index')
@app.route('/')
def hello_world():
    states_lst, total_lst_format, end_data, csv_lst = init_data()
    return render_template('index.html', states_lst=states_lst, total_lst_format=total_lst_format, end_data=end_data,
                           csv_lst=csv_lst)


if __name__ == '__main__':
    app.run(debug=True)
