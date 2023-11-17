import unittest
from datetime import datetime
import app

class TestSymbolValidation(unittest.TestCase):

    def test_valid_symbol(self):
        symbol = "AAPL"  # Example valid symbol
        self.assertTrue(app.validate_symbol(symbol))

    def test_invalid_symbol_length(self):
        symbol = "GOOGLEINC"  # Invalid: exceeds 7 characters
        self.assertFalse(app.validate_symbol(symbol))

    def test_invalid_symbol_lowercase(self):
        symbol = "msft"  # Invalid: lowercase characters
        self.assertFalse(app.validate_symbol(symbol))



class TestChartTypeValidation(unittest.TestCase):

    def test_valid_chart_type(self):
        chart_type = "1"  # Example valid chart type
        self.assertTrue(app.validate_chart_type(chart_type))

    def test_invalid_chart_type(self):
        chart_type = "3"  # Invalid: not 1 or 2
        self.assertFalse(app.validate_chart_type(chart_type))

   

class TestTimeSeriesValidation(unittest.TestCase):

    def test_valid_time_series(self):
        time_series = "3"  # Example valid time series
        self.assertTrue(app.validate_time_series(time_series))

    def test_invalid_time_series(self):
        time_series = "5"  # Invalid: not in the range 1-4
        self.assertFalse(app.validate_time_series(time_series))



class TestStartDateValidation(unittest.TestCase):

    def test_valid_start_date(self):
        start_date = "2023-01-01"  # Example valid start date
        self.assertTrue(app.validate_start_date(start_date))

    def test_invalid_start_date_format(self):
        start_date = "01-01-2023"  # Invalid format: not YYYY-MM-DD
        self.assertFalse(app.validate_start_date(start_date))



class TestEndDateValidation(unittest.TestCase):

    def test_valid_end_date(self):
        end_date = "2023-12-31"  # Example valid end date
        self.assertTrue(app.validate_end_date(end_date))

    def test_invalid_end_date_range(self):
        end_date = "2023-01-01"  # Invalid: before start date
        self.assertFalse(app.validate_end_date(end_date))


if __name__ == '__main__':
    unittest.main()
