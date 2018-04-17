from model import *
import unittest


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