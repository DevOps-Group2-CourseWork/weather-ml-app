import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	def test_prediction_route_success(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_get_form(self):
		response = self.client.get('/')
		self.assertEqual(response.mimetype, 'text/html')
		response_data = response.data.decode('utf-8')
		self.assertIn("<title>Weather Classification Input</title>",
				 response_data)
		self.assertIn("<h1>Weather Classification:</h1>", response_data)
		self.assertIn('<form method="POST" action="/">', response_data)
		self.assertIn('<input type="number" step="any" name="snow">', response_data)
		self.assertIn('<button type="submit">Predict</button>', response_data)
		self.assertIn("</form>", response_data)

	# The model expects temperature in Kelvin, so the form label must say Kelvin.
	def test_temperature_label_is_kelvin(self):
		response = self.client.get('/')
		response_data = response.data.decode('utf-8')
		self.assertIn("<label>Temperature (Kelvin):", response_data,
				"Temperature label should say Kelvin, as the model expects Kelvin input")

if __name__ == '__main__':
	unittest.main()
