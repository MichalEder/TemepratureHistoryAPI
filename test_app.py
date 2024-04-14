import unittest
from main import app

class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_temperature_in_date_valid(self):
        response = self.app.get("/api/v1/10/19881025")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('temperature_in_date', response.json)

    def test_temperature_in_date_invalid_date_format_length(self):
        response = self.app.get("/api/v1/10/123455")
        self.assertEqual(response.status_code, 400)

    def test_temperature_in_date_invalid_date_format_with_characters(self):
        response = self.app.get("/api/v1/10/dfs951")
        self.assertEqual(response.status_code, 400)

    def test_temperature_in_date_nonexistent_station(self):
        response = self.app.get("/api/v1/99999/19881025")
        self.assertEqual(response.status_code, 404)

    def test_temperature_in_date_invalid_station(self):
        response = self.app.get("/api/v1/ab/19881025")
        self.assertEqual(response.status_code, 400)

    def test_all_data_valid(self):
        response = self.app.get("/api/v1/10")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_all_data_nonexistent_station(self):
        response = self.app.get("/api/v1/99")
        self.assertEqual(response.status_code, 404)

    def test_all_data_invalid_station(self):
        response = self.app.get("/api/v1/ab")
        self.assertEqual(response.status_code, 400)

    def test_annual_data_valid(self):
        response = self.app.get("/api/v1/annual/10/1988")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_annual_data_invalid_station(self):
        response = self.app.get("/api/v1/annual/ab/1988")
        self.assertEqual(response.status_code, 400)

    def test_annual_data_nonexistent_station(self):
        response = self.app.get("/api/v1/annual/99999/1988")
        self.assertEqual(response.status_code, 404)

    def test_annual_invalid_date_length(self):
        response = self.app.get("/api/v1/annual/10/19888")
        self.assertEqual(response.status_code, 400)

    def test_annual_invalid_date_format(self):
        response = self.app.get("/api/v1/annual/10/198a")
        self.assertEqual(response.status_code, 400)

    def test_visualization_valid(self):
        response = self.app.get("/visualization/10/1990")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/png")

    def test_visualization_invalid_station(self):
        response = self.app.get("/visualization/aa/1990")
        self.assertEqual(response.status_code, 400)

    def test_visualization_nonexistent_station(self):
        response = self.app.get("/visualization/1000/1990")
        self.assertEqual(response.status_code, 404)

    def test_visualization_date_length(self):
        response = self.app.get("/visualization/10/19900")
        self.assertEqual(response.status_code, 400)

    def test_visualization_date_format(self):
        response = self.app.get("/visualization/10/199a")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()