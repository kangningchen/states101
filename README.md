# Congress-Flask-App

# Data Sources
This application crawls C-SPAN Members of 115th Congress pages (https://www.c-span.org/congress/members/?chamber=house&all 
AND https://www.c-span.org/congress/members/?chamber=Senate&all), as well as accesses New York Times Article Search API (NYT API) and 
Google Places API (Google API). In order to access NYT API and Google API, you would need API keys and save them in the format of 
nyt_key='<your API key>' and google_key='<your API key>' in a file named secrets.py, which should be saved in the same directory as app.py. 
You can get your NYT and Google API keys by signing up at https://developer.nytimes.com/signup 
and at https://developers.google.com/places/web-service/get-api-key respectively.

# Additional Information
In order to run this application, you would need a few modules installed, all of which are specified in requirements.txt. You can set up 
a virtual environment and run: pip install -r requirements.txt to get started.

# Code Structure
1. get_House and get_Senate are functions that crawl C-SPAN pages, both of which return a list of sub lists. Each sub list represent one 
member and contains info about that particular member (name, party, title etc.). This data structure faciliates writing the data to 
database.
2. build_db combines several functions that together initialize a database containing four tables (Member, Title, Party, and State) and
insert data crawled into the database.
3. an Article class was built to parse data returned from NYT API.
4. process_request and get_member_details query database to return Congress member info by state or territory requested by user.
5. plot_bar and plot_state_territory employs Plotly to generate bar chart of number of democrats vs. republicans, as well as 
visualization of state or territory on U.S. map.

# How to Run
Save all the files in this repo in a directory (Please use the same folder structure as this repo). In your terminal, cd to the directory 
where you save app.py and run: python/python3 app.py. You would see:
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 852-803-819
Go to http://127.0.0.1:5000/ in your browswer and begin interacting with the application!
