import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import secrets
import plotly.graph_objs as go
import plotly.offline as offline


# Define Article class to parse data from NYT API
class Article():
    def __init__(self, article_dict = {}):
        self.headline = article_dict['headline']['main']
        self.pub_date = article_dict['pub_date'].split('T')[0]
        self.web_url = article_dict['web_url']

    def __str__(self):
        return '{} published on {}'.format(self.headline, self.pub_date)


# Open cache file
CACHE_FNAME = "congress_members.json"

try:
    cache_file = open(CACHE_FNAME, 'r')
    CACHE_DICTION = json.loads(cache_file.read())
    cache_file.close()
except:
    CACHE_DICTION = {}

# Crawl and cache House member data from C-SPAN
def get_House():
	url = 'https://www.c-span.org/congress/members/?chamber=house&all'

	if url in CACHE_DICTION:
		# print('Getting cached data...')
		soup = BeautifulSoup(CACHE_DICTION[url], 'html.parser')
	else: 
		# print('Getting new data...')
		html = requests.get(url).text
		CACHE_DICTION[url] = html
		dumped_json_cache = json.dumps(CACHE_DICTION)
		f = open(CACHE_FNAME, 'w')
		f.write(dumped_json_cache)
		f.close()
		soup = BeautifulSoup(html, 'html.parser')

	members = soup.find('section', class_='people tiled parties').find('ul').find_all('li')

	member_lst = []
	for member in members:
		member_info = []
		member_name = member.find('div', class_='text').find('h3').string
		member_url = 'https://www.c-span.org/person/?' + member.find('a')['href'].split('/')[-1]
		if member_url in CACHE_DICTION:
			# print('Getting cached data...')
			member_soup = BeautifulSoup(CACHE_DICTION[member_url], 'html.parser')
		else: 
			# print('Getting new data...')
			member_html = requests.get(member_url).text
			CACHE_DICTION[member_url] = member_html
			dumped_json_cache = json.dumps(CACHE_DICTION)
			f = open(CACHE_FNAME, 'w')
			f.write(dumped_json_cache)
			f.close()
			member_soup = BeautifulSoup(member_html, 'html.parser')
		try:
			member_desc = member_soup.find('p', class_='wikipedia').text
		except:
			member_desc = 'Not Available'
		member_title = member.find('div', class_='text').find('span', class_='position').string
		member_party_state = member.find('div', class_='text').find('span', class_='organization').string
		splitted_member_party_state = member_party_state.split()
		member_party = splitted_member_party_state[0].split('-')[0]
		member_state = splitted_member_party_state[0].split('-')[1]
		member_info.append(member_name)
		member_info.append(member_title)
		member_info.append(member_party)
		member_info.append(member_state)
		member_info.append(member_url)
		member_info.append(member_desc)
		member_lst.append(member_info)

	return member_lst


# Crawl and cache Senate member data from C-SPAN
def get_Senate():
	url = 'https://www.c-span.org/congress/members/?chamber=senate&all'

	if url in CACHE_DICTION:
		# print('Getting cached data...')
		soup = BeautifulSoup(CACHE_DICTION[url], 'html.parser')
	else: 
		# print('Getting new data...')
		html = requests.get(url).text
		CACHE_DICTION[url] = html
		dumped_json_cache = json.dumps(CACHE_DICTION)
		f = open(CACHE_FNAME, 'w')
		f.write(dumped_json_cache)
		f.close()
		soup = BeautifulSoup(html, 'html.parser')

	members = soup.find('section', class_='people tiled parties').find('ul').find_all('li')

	member_lst = []
	for member in members:
		member_info = []
		member_name = member.find('div', class_='text').find('h3').string
		member_url = 'https://www.c-span.org/person/?' + member.find('a')['href'].split('/')[-1]
		if member_url in CACHE_DICTION:
			# print('Getting cached data...')
			member_soup = BeautifulSoup(CACHE_DICTION[member_url], 'html.parser')
		else: 
			# print('Getting new data...')
			member_html = requests.get(member_url).text
			CACHE_DICTION[member_url] = member_html
			dumped_json_cache = json.dumps(CACHE_DICTION)
			f = open(CACHE_FNAME, 'w')
			f.write(dumped_json_cache)
			f.close()
			member_soup = BeautifulSoup(member_html, 'html.parser')
		try:
			member_desc = member_soup.find('p', class_='wikipedia').text
		except:
			member_desc = 'Not Available'
		member_title = member.find('div', class_='text').find('span', class_='position').string
		member_party_state = member.find('div', class_='text').find('span', class_='organization').string
		splitted_member_party_state = member_party_state.split('-')
		member_party = splitted_member_party_state[0]
		member_state = splitted_member_party_state[1]
		member_info.append(member_name)
		member_info.append(member_title)
		member_info.append(member_party)
		member_info.append(member_state)
		member_info.append(member_url)
		member_info.append(member_desc)
		member_lst.append(member_info)

	return member_lst


# Initiate database to store Congress member data
def init_db():
	conn = sqlite3.connect('congress_members.db')
	cur = conn.cursor()


	statement = '''
        DROP TABLE IF EXISTS 'Title';
    '''	
	cur.execute(statement)

	statement = '''
        DROP TABLE IF EXISTS 'Party';
    '''	
	cur.execute(statement)

	statement = '''
        DROP TABLE IF EXISTS 'StateTerritory';
    '''	
	cur.execute(statement)

	statement = '''
        DROP TABLE IF EXISTS 'Member';
    '''	
	cur.execute(statement)

	conn.commit()


	statement = '''
        CREATE TABLE 'Title' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'TitleName' TEXT
            );
    '''
	cur.execute(statement)


	statement = '''
        CREATE TABLE 'Party' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'PartyAbbreviation' TEXT,
            'PartyName' TEXT
            );
    '''
	cur.execute(statement)


	statement = '''
        CREATE TABLE 'StateTerritory' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'StateTerritoryAbbreviation' TEXT,
            'StateTerritoryName' TEXT
            );
    '''
	cur.execute(statement)

	
	statement = '''
        CREATE TABLE 'Member' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT,
            'Title' TEXT,
            'PartyAffiliation' TEXT,
            'StateTerritory' TEXT,
            'URL' TEXT,
            'Description' TEXT,
            FOREIGN KEY(PartyAffiliation) REFERENCES Party(Id)
            );
    '''
	cur.execute(statement)


	conn.commit()
	conn.close()


# Insert Congress member data and build database relations
def insert_data(House_lsts, Senate_lsts):

	member_lsts = House_lsts + Senate_lsts

	all_titles = []
	for l in member_lsts:
		all_titles.append(l[1])

	distinct_titles = list(set(all_titles))
	try:
		distinct_titles.remove('')
	except:
		pass 

	states_territories = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 
		'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
        'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa',
        'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
        'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
        'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana',
        'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands',
        'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

	parties = {'D': 'Democrat', 'R': 'Republican'}

	conn = sqlite3.connect('congress_members.db')
	cur = conn.cursor()

	for party_abbrev in parties.keys():
		insertion = (party_abbrev, parties[party_abbrev])	
		statement = 'INSERT INTO Party VALUES (NULL, ?, ?)'
		cur.execute(statement, insertion)

	for title in distinct_titles:
		cur.execute('INSERT INTO Title VALUES (NULL, ?)', [title])	

	for state_territory_abbrev in states_territories.keys():
		insertion = (state_territory_abbrev, states_territories[state_territory_abbrev])	
		statement = 'INSERT INTO StateTerritory VALUES (NULL, ?, ?)'
		cur.execute(statement, insertion)

	for l in member_lsts: 
		insertion = (l[0], l[1], l[2], l[3], l[4], l[5])
		statement = 'INSERT INTO Member '
		statement += 'VALUES (NULL, ?, ?, ?, ?, ?, ?)'
		cur.execute(statement, insertion)

	party_dict = {}
	statement = 'SELECT Id, PartyAbbreviation FROM Party'
	cur.execute(statement)

	for row in cur:
		party_dict[row[0]] = row[1]

	for k in party_dict.keys():
		insertion = (k, party_dict[k])
		statement = 'UPDATE Member SET PartyAffiliation = ? WHERE PartyAffiliation = ?'
		cur.execute(statement, insertion)

	title_dict = {}
	statement = 'SELECT Id, TitleName FROM Title'
	cur.execute(statement)

	for row in cur:
		title_dict[row[0]] = row[1]

	for k in title_dict.keys():
		insertion = (k, title_dict[k])
		statement = 'UPDATE Member SET Title = ? WHERE Title = ?'
		cur.execute(statement, insertion)

	state_territory_dict = {}
	statement = 'SELECT Id, StateTerritoryAbbreviation FROM StateTerritory'
	cur.execute(statement)

	for row in cur:
		state_territory_dict[row[0]] = row[1]

	for k in state_territory_dict.keys():
		insertion = (k, state_territory_dict[k])
		statement = 'UPDATE Member SET StateTerritory = ? WHERE StateTerritory = ?'
		cur.execute(statement, insertion)

	conn.commit()
	conn.close()

# Put everything together to build Congress member database
def build_db():
	House_lsts = get_House()
	Senate_lsts = get_Senate()
	init_db()
	insert_data(House_lsts, Senate_lsts)

# Process user request by querying database
def process_request(state_territory_abbrev, sort=None):
	conn = sqlite3.connect('congress_members.db')
	cur = conn.cursor()
	
	statement = 'SELECT Member.Name, Title.TitleName, Party.PartyName, Member.URL, StateTerritory.StateTerritoryName FROM Member '
	statement += 'JOIN Party ON Member.PartyAffiliation=Party.Id '
	statement += 'JOIN Title ON Member.Title=Title.Id '
	statement += 'JOIN StateTerritory ON Member.StateTerritory=StateTerritory.Id '
	statement += 'WHERE StateTerritory.StateTerritoryAbbreviation="{}" '.format(state_territory_abbrev)

	if sort == 'democrat':
		statement += 'AND Party.PartyName="Democrat" '
		cur.execute(statement)
	elif sort == 'republican':
		statement += 'AND Party.PartyName="Republican" '
		cur.execute(statement)
	else:
		cur.execute(statement)

	results= cur.fetchall()

	rows = []
	for row in results:
		rows.append(list(row))

	for row in rows:
		row[3] = row[3].split('?')[1] 

	conn.close()

	return rows

# Query database to get member details
def get_member_details(ident):
	conn = sqlite3.connect('congress_members.db')
	cur = conn.cursor()

	statement = 'SELECT Member.Name, Party.PartyAbbreviation, StateTerritory.StateTerritoryAbbreviation, Member.Description FROM Member '
	statement += 'JOIN Party ON Member.PartyAffiliation=Party.Id '
	statement += 'JOIN StateTerritory ON Member.StateTerritory=StateTerritory.Id '
	statement += 'WHERE Member.URL LIKE "%{}" '.format(ident)


	cur.execute(statement)
	row = cur.fetchone()
	conn.close()

	return row

# Query database to get # of democrats vs. # of republicans
def get_count(state_territory_abbrev):
	conn = sqlite3.connect('congress_members.db')
	cur = conn.cursor()
	
	statement = 'SELECT COUNT(*) FROM Member '
	statement += 'JOIN StateTerritory ON Member.StateTerritory=StateTerritory.Id '
	statement += 'JOIN Party ON Member.PartyAffiliation=Party.Id '
	statement += 'WHERE StateTerritoryAbbreviation="{}" AND PartyAbbreviation="D" '.format(state_territory_abbrev)

	cur.execute(statement)
	d_num = cur.fetchone()[0]

	statement = 'SELECT COUNT(*) FROM Member '
	statement += 'JOIN StateTerritory ON Member.StateTerritory=StateTerritory.Id '
	statement += 'JOIN Party ON Member.PartyAffiliation=Party.Id '
	statement += 'WHERE StateTerritoryAbbreviation="{}" AND PartyAbbreviation="R" '.format(state_territory_abbrev)

	cur.execute(statement)
	r_num = cur.fetchone()[0]

	return (d_num, r_num)

# Unique identifier generator function
def params_unique_combination(baseurl, params_d, private_keys=['api-key', 'key']):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

# Make request to NYT API to get articles related to each state or territory (by passing state or territory name as query term)
def get_NYT_data(q):
    baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params_diction = {}
    params_diction["api-key"] = secrets.nyt_key
    params_diction["q"] = q
    params_diction["fl"] = "web_url,snippet,headline,pub_date"
    unique_ident = params_unique_combination(baseurl, params_diction)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        NYT_resp = requests.get(baseurl, params = params_diction)
        NYT_resp_text = NYT_resp.text
        CACHE_DICTION[unique_ident] = json.loads(NYT_resp_text)
        dumped_NYT_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME,"w")
        f.write(dumped_NYT_json_cache)
        f.close()
        return CACHE_DICTION[unique_ident]

# Create article instances
def create_article_insts(article_dict):
	article_insts = []
	for article in article_dict:
		if 'headline' in article and 'pub_date' in article and 'web_url' in article:
			inst = Article(article)
			article_insts.append(inst)
	return article_insts

# Get NYT data and create article instances
def get_article_lst(q):
	NYT_data = get_NYT_data(q)
	article_inst_lst = create_article_insts(NYT_data['response']['docs'])
	return article_inst_lst

# Plot num of democrats vs. num of republicans bar chart
def plot_bar(y1, y2):
	trace1 = go.Bar(
	    x=['Demorat'],
	    y=[y1],
	    name='Demorat',
	    marker=dict(
	    	color='rgb(41, 125, 198)')
	)
	trace2 = go.Bar(
	    x=['Republican'],
	    y=[y2],
	    name='Republican',
	    marker=dict(
	    	color='rgb(201, 25, 16)')
	)

	data = [trace1, trace2]
	layout = go.Layout(
	    title='Democrats VS. Republicans'
	)

	fig = go.Figure(data=data, layout=layout)
	div = offline.plot(fig, show_link=False, output_type='div', include_plotlyjs=False)
	return div

# Make request to Google API to get state or territory longitude and latitude 
def get_lon_lat(state_territory_name):
    baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params_diction = {}
    params_diction['key'] = secrets.google_key
    params_diction['query'] = state_territory_name
    params_diction['type'] = 'State or Territory'
    unique_ident = params_unique_combination(baseurl, params_diction)
    if unique_ident in CACHE_DICTION:
        # print('getting cached data')
        site_data = CACHE_DICTION[unique_ident]
    else:
        # print('getting new data')
        google_resp = requests.get(baseurl, params = params_diction)
        google_resp_text = google_resp.text
        CACHE_DICTION[unique_ident] = json.loads(google_resp_text)
        dumped_google_json_cache = json.dumps(CACHE_DICTION)
        f = open(CACHE_FNAME,'w')
        f.write(dumped_google_json_cache)
        f.close()
        site_data = CACHE_DICTION[unique_ident]
    lat = site_data['results'][0]['geometry']['location']['lat']
    lon = site_data['results'][0]['geometry']['location']['lng']
    return lon, lat

# Plot state or territory on map
def plot_map(lon, lat):

    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = [lon],
            lat = [lat],
            mode = 'markers',
            marker = dict(
                size = 12,
                symbol = 'star',
                color = 'red',
            ))]
    layout = dict(
            title = 'US States and Territories',
            geo = dict(
                scope='usa',
                projection=dict(type='albers usa'),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(100, 217, 217)",
                countrycolor = "rgb(217, 100, 217)",
                countrywidth = 3,
                subunitwidth = 3
            ),
        )
    fig = dict(data=data, layout=layout)
    div = offline.plot(fig, show_link=False, output_type='div', include_plotlyjs=False)
    return div

# Make request to Google API and plot state and territory on map
def plot_state_territory(state_territory_name):
	lon_lat_tuple = get_lon_lat(state_territory_name)
	div = plot_map(lon_lat_tuple[0],lon_lat_tuple[1])
	return div









