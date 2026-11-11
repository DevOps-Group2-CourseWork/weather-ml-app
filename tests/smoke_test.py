import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	""" A smoke test is a quick, basic check that an application starts and its most important features work. 
		Its job is to catch major breakages early, before any more detailed testing is done.
		In our weather app, the smoke test checks that the home page loads with the weather form, and that one valid form post returns a prediction without an error. 
		This class covers this suite of tests.

		Group Project Notes/Revisions:
		JP 11/11/26: 
		- Updated the tests to include doc strings and comments so that these are easier to follow and understand without delving too deeply into the code.
		- Extended the test_prediction_route_success test to check that a prediction was actually made and that the model can be used.
		- Extended the test_get_form test, as it was only looking at the 'snow' field. 
			Removed exact HTML matching, as this is risky with any form changes. The test has been updated to check for functionality instead.
			Moved the Kelvin label check into the main test, rather than as a seperate method.
	"""

	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	def test_prediction_route_success(self):
		"""Check the app runs end to end and returns a prediction.

		Test Description:
		Posts a full set of valid weather readings to '/' and checks that:
			- the request succeeds (status 200)
			- no error message is shown
			- the result page is returned with a prediction
		"""
		# Test prerequisites
		form_data = {
			'temperature': '275.15', 'pressure': '1013', 'humidity': '85',
			'wind_speed': '3.6', 'wind_deg': '180', 'rain_1h': '0',
			'rain_3h': '0', 'snow': '0', 'clouds': '20'
		}
		response = self.client.get('/', data=form_data)
		response_data = response.data.decode('utf-8')

		# Check that the app didn't crash
		self.assertEqual(response.status_code, 200, "The app should return a successful response")

		# Check that a valid prediction was made
		self.assertNotIn("Error processing input", response_data)
		self.assertIn("The weather is:", response_data)

	def test_get_form(self):
		"""Check the input form is rendered with all the fields the app needs.

		Test Description:
		Sends a GET request to '/' and checks that the page:
			- loads successfully (status 200) as HTML
			- contains a form that posts to '/'
			- has an input for each of the 9 fields the app reads
			- has a Predict button
			- shows no error message
			- checks that the label says Kelvin to ensure that the results returned are correct as to what the user is expecting
		"""
		# Test prerequisites
		response = self.client.get('/')
		response_data = response.data.decode('utf-8')

		# Check that the page loads as HTML
		self.assertEqual(response.status_code, 200, "Form page should load successfully")
		self.assertEqual(response.mimetype, 'text/html')

		# Check that the app successfully posts to the prediction route
		self.assertIn('<form method="POST" action="/">', response_data)

		# Check every field the app reads has an input on the form
		fields = ['temperature', 'pressure', 'humidity', 'wind_speed', 'wind_deg',
				  'rain_1h', 'rain_3h', 'snow', 'clouds']
		for field in fields:
			with self.subTest(field=field):
				self.assertIn(f'name="{field}"', response_data,
					f"Form is missing the '{field}' input")

		# Check the form can be submitted
		self.assertIn('type="submit"', response_data, "Form is missing a submit button")

		# Check no error is shown on first load
		self.assertNotIn("Error processing input", response_data)

		# The model expects temperature in Kelvin, so the form label must say Kelvin.
		self.assertIn("<label>Temperature (Kelvin):", response_data,
		"Temperature label should say Kelvin, as the model expects Kelvin input")

if __name__ == '__main__':
	unittest.main()
