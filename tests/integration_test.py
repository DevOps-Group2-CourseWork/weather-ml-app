import unittest
import re
from app import app, weather_classes  # Import your Flask app instance # Imported the weather classes too so that these can easily be reused for the tests.


class TestModelAppIntegration(unittest.TestCase):
	""" Integration tests allow us to check that the functions within the app work collectively. 
		The goal is to check the app and model work together to return a valid prediction.
		This class covers these tests.

		Group Project Notes/Revisions:
		JP 11/11/26: 
		- Updated the tests to include doc strings and comments so that these are easier to follow and understand without delving too deeply into the code.
		- Added __init__.py file to recognise the folder as a package. This is so the tests can be picked up through the CI pipeline and out of the box Visual Studio testing tools.
		- Updated response.data test to check the prediction itself, not the label, as exact HTML matching is risky if the form is ever updated intentionally. 
			Added a more robust check that just a 200 status check, as this can be returned even if there is an error with the prediction.
		- Updated Prediction time tests to also check for negative numbers.
	"""

	def setUp(self):
		app.testing = True
		self.client = app.test_client()
		
	def test_model_app_integration(self):
		"""Integration tests allow us to check that the functions within the app work collectively. 
		The goal is to check the app and model work together to return a valid prediction.

		Test Description:
		Posts a full set of valid weather readings (temperature in Kelvin,
		pressure in hPa, wind speed in m/s, rain and snow in mm, humidity and
		clouds in %) to '/' and checks that the result page:
			- loads successfully (status 200)
			- shows no "Error processing input" message
			- shows a prediction value after "The weather is:"
			- shows a prediction time in ms that isn't negative
			- shows a prediction that is one of the known weather_classes
		"""
		# Valid test input that should work with the trained model
		form_data = {
			'temperature': '275.15',   # Kelvin
			'pressure': '1013',        # hPa
			'humidity': '85',          # %
			'wind_speed': '3.6',       # m/s
			'wind_deg': '180',         # degrees
			'rain_1h': '0',            # mm
			'rain_3h': '0',            # mm
			'snow': '0',               # mm
			'clouds': '20'             # %
		}

		# Set the test prerequisites
		response = self.client.post('/', data=form_data)
		response_data = response.data.decode('utf-8')
	
		# Ensure that the result page (response.data) should include a weather prediction
		# Here, we're checking if a valid response was received (200) and that this contains a valid prediction
		self.assertEqual(response.status_code, 200)
		self.assertNotIn("Error processing input", response_data)
		match = re.search(r'The weather is:</strong>\s*(\w+)', response_data)
		self.assertIsNotNone(match, "Prediction value not found on result page")
	
		# Ensure that the result page should include a prediction time
		# First, get the prediction time
		time_match = re.search(r'Prediction time:</strong>\s*(\d+(?:\.\d+)?)\s*ms', response_data)
		# Then check that the result isn't negative and is a valid
		self.assertIsNotNone(time_match, "Result page should include a prediction time in ms")
		latency = float(time_match.group(1))
		self.assertGreaterEqual(latency, 0, "Prediction time should not be negative")
				
		# Ensure that classification is in valid classes, provide an error message if not.
		self.assertIn(match.group(1), weather_classes) # Expecting a match from the weather classes here. Replaced with one line and imported the values from the class above instead of having to rewrite these all.

if __name__ == '__main__':
	unittest.main()
