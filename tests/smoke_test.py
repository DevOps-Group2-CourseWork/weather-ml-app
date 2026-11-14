import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	def test_prediction_route_success(self):
		# Test prerequisites
		form_data = {
			'temperature': '275.15', 'pressure': '1013', 'humidity': '85',
			'wind_speed': '3.6', 'wind_deg': '180', 'rain_1h': '0',
			'rain_3h': '0', 'snow': '0', 'clouds': '20'
		}
		response = self.client.post('/', data=form_data)
		response_data = response.data.decode('utf-8')

		# Check that the app didn't crash
		self.assertEqual(response.status_code, 200, "The app should return a successful response")

		# Check that a valid prediction was made
		self.assertNotIn("Error processing input", response_data)
		self.assertIn("The weather is:", response_data)

	def test_get_form(self):
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
