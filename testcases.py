from model import *
import unittest

class TestScrapingAndCrawling(unittest.TestCase):

	def test_House(self):
		# Test if all 477 members' info is obtained and if member info list is populated correctly
	    House_lst = get_House()
	    self.assertEqual(len(House_lst), 477)
	    self.assertEqual(House_lst[0][0], 'Ralph Abraham')
	    self.assertEqual(House_lst[0][1], 'U.S. Representative')
	    self.assertEqual(House_lst[0][2], 'R')
	    self.assertEqual(House_lst[0][3], 'LA')
	    self.assertEqual(House_lst[0][4], 'https://www.c-span.org/person/?76236')
	    self.assertEqual(House_lst[0][5], 'Ralph Lee Abraham, Jr. is an American physician and former veterinarian from Mangham, Louisiana, who won election on December 6, 2014, as a Republican to represent LA-5 in the United States House of Representatives. Wikipedia*')
	
	def test_Senate(self):
		# Test if all 108 members' info is obtained and if member info list is populated correctly
		Senate_lst = get_Senate()
		self.assertEqual(len(Senate_lst), 108)
		self.assertEqual(Senate_lst[0][0], 'Lamar Alexander')
		self.assertEqual(Senate_lst[0][1], 'U.S. Senator')
		self.assertEqual(Senate_lst[0][2], 'R')
		self.assertEqual(Senate_lst[0][3], 'TN')
		self.assertEqual(Senate_lst[0][4], 'https://www.c-span.org/person/?5')
		self.assertEqual(Senate_lst[0][5], 'Andrew Lamar Alexander Jr. is the senior United States Senator from Tennessee, and a member of the Republican Party. Wikipedia*')
		
class TestDatabase(unittest.TestCase):

	def test_member_table(self):
		# Test if Member table has the correct amount of entries
		conn = sqlite3.connect('congress_members.db')
		cur = conn.cursor()

		statement = 'SELECT Name FROM Member'
		cur.execute(statement)
		results = cur.fetchall()
		self.assertEqual(len(results), 585)
		self.assertIn(('Elizabeth Warren',), results)

		conn.close()

	def test_join(self):
		# Test if tables can be joined correctly
		conn = sqlite3.connect('congress_members.db')
		cur = conn.cursor()

		statement = '''
				SELECT Member.Name, Party.PartyName, Title.TitleName, 
					   StateTerritory.StateTerritoryName 
				FROM Member
				JOIN Party ON Member.PartyAffiliation=Party.Id
				JOIN Title ON Member.Title=Title.Id
				JOIN StateTerritory ON Member.StateTerritory=StateTerritory.Id
		'''
		cur.execute(statement)
		results = cur.fetchall()
		self.assertIn(('Alma Adams', 'Democrat', 'U.S. Representative', 'North Carolina'), results)
		self.assertIn(('Barbara Boxer', 'Democrat', 'U.S. Senator (Former)', 'California'), results)

		conn.close()

class TestDataProcessing(unittest.TestCase):

	def test_data_processing(self):
		rows_all = process_request('MI')
		self.assertEqual(len(rows_all), 17)
		self.assertIn(['Justin Amash', 'U.S. Representative', 'Republican', '1033767', 'Michigan'], rows_all)
		rows_republican = process_request('MI', 'democrat')
		self.assertEqual(len(rows_republican), 7)

		details = get_member_details('62502')
		self.assertEqual(('Karen Bass', 'D', 'CA', 'Karen Ruth Bass is an American Democrat politician. She represents California\'s 37th congressional district in the United States House of Representatives; she was first elected in 2010. Wikipedia*'), details)

		count = get_count('MD')
		self.assertEqual((12, 1), count)
		
class TestNYTSearch(unittest.TestCase):

	def test_NYT_data(self):
		# Test if at least one article is returned from search
		m_data = get_NYT_data('Michigan')
		self.assertGreaterEqual(len(m_data['response']['docs']), 1)
		c_data = get_NYT_data('California')
		self.assertGreaterEqual(len(c_data['response']['docs']), 1)	

	def test_article_insts(self):
		# Test if at least one article inst is generated 
		m_articles = get_article_lst('Michigan')
		self.assertGreaterEqual(len(m_articles), 1)
		self.assertIsInstance(m_articles[0], Article)


class TestPlot(unittest.TestCase):

    def test_bar_chart(self):
        # Test if plot_bar function would return a string     
        div = plot_bar(2,9)
        self.assertIsInstance(div, str)
        # And if the string contains 'div'
        self.assertIn('div', div)

    def test_map(self):
    	# Test if plot_state_territory would return a string
    	m_div = plot_state_territory('Michigan')
    	c_div = plot_state_territory('California')
    	self.assertIsInstance(m_div, str)
    	self.assertIsInstance(c_div, str)
    	# And if the string contains 'div'
    	self.assertIn('div', m_div)
    	self.assertIn('div', c_div)

if __name__ == '__main__':
    unittest.main()