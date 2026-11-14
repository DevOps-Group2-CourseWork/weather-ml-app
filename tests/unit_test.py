import unittest
from app import app, classify_weather, load_model, feature_names
import pandas as pd

def make_input(values):
	return pd.DataFrame([values], columns=feature_names)

class TestUnit(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()
	
	def test_post_missing_field(self):
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
		# Set the test prerequisites
		model = load_model()

		# Check the model loaded and can make predictions
		self.assertIsNotNone(model, "Model failed to load")
		self.assertTrue(hasattr(model, 'predict'), "Loaded object has no predict method")

		# Check we're working with the correct model and our 9 inputs
		self.assertEqual(model.n_features_in_, 9, "Model should expect 9 input features")

		# Check the model can make a prediction on valid input. I've just used zeros here to check we're getting a valid output.
		prediction = model.predict(make_input([0] * 9))
		self.assertEqual(len(prediction), 1, "Model should return one prediction")



	def test_clear_classification_output(self):
		test_input = make_input([269.686,1002,78,0,23,0,0,0,0])
		class_result, _ = classify_weather(test_input) 
		# Ensure that 'clear' class is returned
		self.assertEqual(class_result, "clear")
		
	def test_rainy_classification_output(self):
		test_input = make_input([279.626,998,99,1,314,0.3,0,0,88])
		class_result, _ = classify_weather(test_input) 
		# Ensure that 'rainy' class is returned
		self.assertEqual(class_result, "rainy")
		

	def test_foggy_classification_output(self):
		test_input = make_input([289.47,1015,88,2,300,0,0,0,20])
		class_result, _ = classify_weather(test_input)
		# Ensure that 'foggy' class is returned
		self.assertEqual(class_result, "foggy")
		
if __name__ == '__main__':
	unittest.main()
