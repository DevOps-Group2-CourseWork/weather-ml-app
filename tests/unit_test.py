import unittest
from app import app, classify_weather, load_model, weather_classes # Imported the weather classes too so that these can easily be reused for the tests.
import numpy as np

class TestUnit(unittest.TestCase):
	""" Unit tests allow us to check small, self-contained pieces of code to confirm we're getting the expected results for the given input. 
		This class covers these tests.

		Group Project Notes/Revisions:
		JP 11/11/26: 
		- Updated the tests to include doc strings and comments so that these are easier to follow and understand without delving too deeply into the code.
		- Updated missing wind speed test to be more specific. A 200 status code can be returned even if there is an issue with the results, so this was extended.
		- Corrected the model loading tests to use unit tests, rather than plain asserts. Extended this to also included a tighter model check and that it can actually make predictions.
	"""
	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	def test_post_missing_field(self):
		"""Check a form post with a missing required field shows an error message.

		Test Description:
		This test posts a set of weather readings with 'wind_speed' left out to '/' and
		checks that the app handles it without crashing:
			- returns status 200, as the error is caught and the form is shown again
			- shows the "Error processing input" message
			- shows the input form again
			- does not show a prediction
		"""
		form_data = {
			'temperature': '270.277',
			'pressure': '1006',
			'humidity': '84',
			# 'wind_speed' is missing
			'wind_deg': '274',
			'rain_1h': '0',
			'rain_3h': '0',
			'snow': '0',
			'clouds': '9'
		}
		
		# Set the test prerequisites
		response = self.client.post('/', data=form_data)
		response_data = response.data.decode('utf-8')

		# Check that the response has 200 status code with a valid error message
		self.assertEqual(response.status_code, 200)
		self.assertIn("Error processing input", response_data)

		# Check that the user is sent back to the form successfully
		self.assertIn('<form method="POST" action="/">', response_data)

		# Check that no prediction was made
		self.assertNotIn("The weather is:", response_data)

	def test_model_can_be_loaded(self):
		"""Check the model loads correctly and is ready to classify weather.

		Test Description:
		Loads the model from 'model/model.pkl' and checks that it:
			- loads successfully and has a predict method
			- expects the 9 input features the app sends
			- returns one prediction for a single row of 9 inputs
		"""
		# Set the test prerequisites
		model = load_model()

		# Check the model loaded and can make predictions
		self.assertIsNotNone(model, "Model failed to load")
		self.assertTrue(hasattr(model, 'predict'), "Loaded object has no predict method")

		# Check we're working with the correct model and our 9 inputs
		self.assertEqual(model.n_features_in_, 9, "Model should expect 9 input features")

		# Check the model can make a prediction on valid input. I've just used zeros here to check we're getting a valid output.
		prediction = model.predict(np.zeros((1, 9)))
		self.assertEqual(len(prediction), 1, "Model should return one prediction")


	def test_clear_classification_output(self):
		"""Check clear weather readings are classified as 'clear'.

		Test Description:
		Passes a set of clear weather readings (269.686 K, 1002 hPa,
		78% humidity, no wind, rain, snow or cloud) to classify_weather
		and checks that:
			- the predicted class is 'clear'
		"""
		test_input = np.array([269.686,1002,78,0,23,0,0,0,0]).reshape(1,-1)
		class_result, _ = classify_weather(test_input) 

		# Ensure that 'clear' class is returned
		self.assertEqual(class_result, "clear")
		
	def test_rainy_classification_output(self):
		"""Check rainy weather readings are classified as 'rainy'.

		Test Description:
		Passes a set of rainy weather readings (279.626 K, 998 hPa,
		99% humidity, 0.3 mm rain in the last hour, 88% cloud) to
		classify_weather and checks that:
			- the predicted class is 'rainy'
		"""
		test_input = np.array([279.626,998,99,1,314,0.3,0,0,88]).reshape(1,-1)
		class_result, _ = classify_weather(test_input) 

		# Ensure that 'rainy' class is returned
		self.assertEqual(class_result, "rainy")
		

	def test_foggy_classification_output(self):
		"""Check foggy weather readings are classified as 'foggy'.

		Test Description:
		Passes a set of foggy weather readings (289.47 K, 1015 hPa,
		88% humidity, light wind, no rain or snow, 20% cloud) to
		classify_weather and checks that:
			- the predicted class is 'foggy'
		"""

		test_input = np.array([289.47,1015,88,2,300,0,0,0,20]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)

		# Ensure that 'foggy' class is returned
		self.assertEqual(class_result, "foggy")
		
if __name__ == '__main__':
	unittest.main()
