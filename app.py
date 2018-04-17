
from flask import Flask, render_template, request
import requests
import model 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def show_member_table():
    state_territory_abbrev = request.form['stateterritory']
    if 'sort' in request.form:
        sort = request.form['sort']
        rows = model.process_request(state_territory_abbrev, sort)
    else:
        rows = model.process_request(state_territory_abbrev)

    state_territory_name = rows[0][4]
    article_lst = model.get_article_lst(state_territory_name)

    num_tuple = model.get_count(state_territory_abbrev)
    d_num = num_tuple[0]
    r_num = num_tuple[1]
    bar_chart = model.plot_bar(d_num, r_num)

    state_territory_map = model.plot_state_territory(state_territory_name)
    
    return render_template('table.html', rows=rows, stateterritory=state_territory_name, list=article_lst, barchart=bar_chart, state_territory_map=state_territory_map)

@app.route('/search/<ident>')
def show_member_detais(ident):
    row = model.get_member_details(ident)
    return render_template('about.html', name=row[0], party=row[1], stateterritory=row[2], desc=row[3][:-10])



if __name__ == '__main__':
    # model.build_db()
    app.run(debug=True)