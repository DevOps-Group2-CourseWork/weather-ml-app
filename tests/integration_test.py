import unittest
import re
from app import app, weather_classes  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

	def setUp(self):
		app.testing = True
		self.client = app.test_client()
		
	def test_model_app_integration(self):
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
		self.assertEqual(response.status_code, 200)
		self.assertNotIn("Error processing input", response_data)
		match = re.search(r'The weather is:</strong>\s*(\w+)', response_data)
		self.assertIsNotNone(match, "Prediction value not found on result page")
	
		# Ensure that the result page should include a prediction time
		time_match = re.search(r'Prediction time:</strong>\s*(\d+(?:\.\d+)?)\s*ms', response_data)
		self.assertIsNotNone(time_match, "Result page should include a prediction time in ms")
		latency = float(time_match.group(1))
		self.assertGreaterEqual(latency, 0, "Prediction time should not be negative")
				
		# Ensure that classification is in valid classes.
		self.assertIn(match.group(1), weather_classes)

if __name__ == '__main__':
	unittest.main()
