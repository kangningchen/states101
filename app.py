
from flask import Flask, render_template, request
import requests
import model 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def show_state_details():
    state_territory_abbrev = request.form['stateterritory']
    try:
        if 'sort' in request.form:
            # if user selects to only see democrats or republicans for a certain state or territory
            sort = request.form['sort']
            rows = model.process_request(state_territory_abbrev, sort)

            state_territory_name = rows[0][4] 
            # Plot state or territory on map
            state_territory_map = model.plot_state_territory(state_territory_name)

            # Get state or territory name and use it as a query term to search for relevant articles on NYT API
            article_lst = model.get_article_lst(state_territory_name)

            return render_template('table-nobar.html', rows=rows, stateterritory=state_territory_name, state_territory_map=state_territory_map, list=article_lst)

        else:
            # Both democrats and republicans would show up in member table
            rows = model.process_request(state_territory_abbrev)
            
            state_territory_name = rows[0][4]
            # Plot state or territory on map
            state_territory_map = model.plot_state_territory(state_territory_name)

            # Show a bar chart of democrats vs.republicans only if user choose to see both 
            num_tuple = model.get_count(state_territory_abbrev)
            d_num = num_tuple[0]
            r_num = num_tuple[1]
            barchart = model.plot_bar(d_num, r_num)

            # Get state or territory name and use it as a query term to search for relevant articles on NYT API
            article_lst = model.get_article_lst(state_territory_name)

            return render_template('table.html', rows=rows, stateterritory=state_territory_name, state_territory_map=state_territory_map, barchart=barchart, list=article_lst)
    
    except:

        errormsg = 'Please enter a valid state or territory abbreviation'
        # If user inputs an invalid state or territory abbreviation, show an error message
        return render_template('error.html', errormsg=errormsg)

@app.route('/search/<ident>')
def show_member_detais(ident):
    # Get member details
    row = model.get_member_details(ident)
    return render_template('about.html', name=row[0], party=row[1], stateterritory=row[2], desc=row[3][:-10])


if __name__ == '__main__':
    # model.build_db()
    app.run(debug=True)