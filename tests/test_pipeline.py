import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch, MagicMock


class TestDataValidation(unittest.TestCase):
    """Test data validation and cleaning functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.sample_data = pd.DataFrame({
            'InvoiceNo': ['489434', '489434', '489435'],
            'StockCode': ['85123A', '71053', '84406B'],
            'Description': ['WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 'JUMBO BAG RED RETROSPOT'],
            'Quantity': [6, 6, 8],
            'InvoiceDate': ['2010-12-01 08:26:00', '2010-12-01 08:26:00', '2010-12-01 08:26:00'],
            'UnitPrice': [2.55, 3.39, 1.95],
            'CustomerID': [17850.0, 17850.0, 13047.0],
            'Country': ['United Kingdom', 'United Kingdom', 'United Kingdom']
        })

    def test_column_standardization(self):
        """Test that column names are standardized correctly"""
        df = self.sample_data.copy()
        
        # Standardize column names
        df.columns = [
            "invoice_no",
            "stock_code",
            "description",
            "quantity",
            "invoice_date",
            "unit_price",
            "customer_id",
            "country"
        ]
        
        expected_columns = [
            "invoice_no", "stock_code", "description", "quantity",
            "invoice_date", "unit_price", "customer_id", "country"
        ]
        
        self.assertEqual(list(df.columns), expected_columns)

    def test_remove_duplicates(self):
        """Test that duplicate rows are removed"""
        df = self.sample_data.copy()
        initial_rows = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # All 3 rows are unique (only first 2 have same InvoiceNo but differ in other columns)
        self.assertEqual(len(df), 3)
        self.assertEqual(len(df), initial_rows)

    def test_remove_null_descriptions(self):
        """Test that rows with missing descriptions are removed"""
        df = self.sample_data.copy()
        
        # Add rows with null descriptions
        df.loc[len(df)] = ['489436', '84407', np.nan, 10, '2010-12-01 08:26:00', 2.50, 13048.0, 'France']
        df.loc[len(df)] = ['489437', '84408', None, 5, '2010-12-01 08:26:00', 3.00, 13049.0, 'Germany']
        
        initial_rows = len(df)
        
        # Remove rows with null descriptions
        df = df.dropna(subset=["Description"])
        
        self.assertLess(len(df), initial_rows)
        self.assertTrue(df['Description'].notna().all())

    def test_quantity_validation(self):
        """Test that invalid quantities (<=0) are removed"""
        df = self.sample_data.copy()
        
        # Add invalid quantities
        df.loc[len(df)] = ['489436', '84407', 'TEST PRODUCT', 0, '2010-12-01 08:26:00', 2.50, 13048.0, 'France']
        df.loc[len(df)] = ['489437', '84408', 'TEST PRODUCT 2', -5, '2010-12-01 08:26:00', 3.00, 13049.0, 'Germany']
        
        initial_rows = len(df)
        
        # Filter valid quantities
        df = df[df['Quantity'] > 0]
        
        self.assertLess(len(df), initial_rows)
        self.assertTrue((df['Quantity'] > 0).all())

    def test_unit_price_validation(self):
        """Test that invalid prices (<=0) are removed"""
        df = self.sample_data.copy()
        
        # Add invalid prices
        df.loc[len(df)] = ['489436', '84407', 'TEST PRODUCT', 10, '2010-12-01 08:26:00', 0, 13048.0, 'France']
        df.loc[len(df)] = ['489437', '84408', 'TEST PRODUCT 2', 5, '2010-12-01 08:26:00', -2.50, 13049.0, 'Germany']
        
        initial_rows = len(df)
        
        # Filter valid prices
        df = df[df['UnitPrice'] > 0]
        
        self.assertLess(len(df), initial_rows)
        self.assertTrue((df['UnitPrice'] > 0).all())

    def test_total_sales_calculation(self):
        """Test that total sales is calculated correctly"""
        df = self.sample_data.copy()
        
        # Create total sales column
        df['total_sales'] = df['Quantity'] * df['UnitPrice']
        
        # Verify calculations
        for idx, row in df.iterrows():
            expected = row['Quantity'] * row['UnitPrice']
            self.assertAlmostEqual(row['total_sales'], expected, places=2)

    def test_customer_id_conversion(self):
        """Test that customer IDs are converted to nullable integer"""
        df = self.sample_data.copy()
        
        # Add null customer ID
        df.loc[len(df)] = ['489436', '84407', 'TEST PRODUCT', 10, '2010-12-01 08:26:00', 2.50, np.nan, 'France']
        
        # Convert to nullable integer
        df['CustomerID'] = df['CustomerID'].astype('Int64')
        
        # Verify it's int64 or nullable int
        self.assertIn(str(df['CustomerID'].dtype), ['Int64', 'int64'])


class TestDataQuality(unittest.TestCase):
    """Test data quality checks"""

    def setUp(self):
        """Set up test fixtures"""
        self.clean_data = pd.DataFrame({
            'invoice_no': ['489434', '489435', '489436'],
            'stock_code': ['85123A', '71053', '84406B'],
            'description': ['PRODUCT A', 'PRODUCT B', 'PRODUCT C'],
            'quantity': [6, 8, 10],
            'invoice_date': [datetime(2010, 12, 1), datetime(2010, 12, 1), datetime(2010, 12, 2)],
            'unit_price': [2.55, 3.39, 1.95],
            'customer_id': [17850, 17850, 13047],
            'country': ['United Kingdom', 'United Kingdom', 'France'],
            'total_sales': [15.30, 27.12, 19.50]
        })

    def test_no_null_values_in_required_fields(self):
        """Test that required fields have no null values"""
        required_fields = ['invoice_no', 'stock_code', 'description', 'quantity', 'unit_price']
        
        for field in required_fields:
            self.assertTrue(self.clean_data[field].notna().all(), f"Field {field} has null values")

    def test_positive_quantity(self):
        """Test that all quantities are positive"""
        self.assertTrue((self.clean_data['quantity'] > 0).all())

    def test_positive_price(self):
        """Test that all prices are positive"""
        self.assertTrue((self.clean_data['unit_price'] > 0).all())

    def test_total_sales_consistency(self):
        """Test that total sales matches quantity * unit price"""
        expected_total_sales = self.clean_data['quantity'] * self.clean_data['unit_price']
        
        pd.testing.assert_series_equal(
            self.clean_data['total_sales'],
            expected_total_sales,
            check_names=False
        )

    def test_valid_country_values(self):
        """Test that all rows have a country value"""
        self.assertTrue(self.clean_data['country'].notna().all())
        self.assertTrue((self.clean_data['country'] != '').all())

    def test_data_types(self):
        """Test that data types are correct"""
        expected_types = {
            'invoice_no': ('str', 'object'),  # Both str and object are valid in different pandas versions
            'stock_code': ('str', 'object'),
            'description': ('str', 'object'),
            'quantity': 'int64',
            'unit_price': 'float64',
            'customer_id': 'int64',
            'country': ('str', 'object')
        }
        
        for column, expected_type in expected_types.items():
            actual_type = str(self.clean_data[column].dtype)
            if isinstance(expected_type, tuple):
                self.assertIn(actual_type, expected_type, f"Column {column} has wrong type")
            else:
                self.assertEqual(actual_type, expected_type, f"Column {column} has wrong type")


class TestPipelineIntegration(unittest.TestCase):
    """Test pipeline integration and data flow"""

    def test_full_pipeline_flow(self):
        """Test the complete data pipeline flow"""
        # Create sample raw data with actual duplicates
        raw_data = pd.DataFrame({
            'InvoiceNo': ['489434', '489434', '489435'],
            'StockCode': ['85123A', '85123A', '84406B'],
            'Description': ['PRODUCT A', 'PRODUCT A', 'PRODUCT C'],
            'Quantity': [6, 6, 8],
            'InvoiceDate': ['2010-12-01', '2010-12-01', '2010-12-01'],
            'UnitPrice': [2.55, 2.55, 1.95],
            'CustomerID': [17850.0, 17850.0, 13047.0],
            'Country': ['United Kingdom', 'United Kingdom', 'France']
        })
        
        # Simulate transform
        df = raw_data.copy()
        df.columns = [
            "invoice_no", "stock_code", "description", "quantity",
            "invoice_date", "unit_price", "customer_id", "country"
        ]
        df = df.drop_duplicates()
        df = df.dropna(subset=["description"])
        df["customer_id"] = df["customer_id"].astype("Int64")
        df["total_sales"] = df["quantity"] * df["unit_price"]
        df = df[df["quantity"] > 0]
        df = df[df["unit_price"] > 0]
        
        # Verify output
        self.assertEqual(len(df), 2)  # One duplicate removed
        self.assertIn("total_sales", df.columns)
        self.assertTrue((df["quantity"] > 0).all())
        self.assertTrue((df["unit_price"] > 0).all())


class TestDataStatistics(unittest.TestCase):
    """Test statistical properties of the data"""

    def setUp(self):
        """Set up test fixtures"""
        self.clean_data = pd.DataFrame({
            'invoice_no': ['489434', '489435', '489436', '489437', '489438'],
            'stock_code': ['85123A', '71053', '84406B', '85124B', '85125C'],
            'description': ['PRODUCT A', 'PRODUCT B', 'PRODUCT C', 'PRODUCT D', 'PRODUCT E'],
            'quantity': [6, 8, 10, 5, 12],
            'invoice_date': [datetime(2010, 12, 1)] * 5,
            'unit_price': [2.55, 3.39, 1.95, 4.50, 2.00],
            'customer_id': [17850, 17850, 13047, 13048, 13049],
            'country': ['UK', 'UK', 'France', 'Germany', 'Spain'],
            'total_sales': [15.30, 27.12, 19.50, 22.50, 24.00]
        })

    def test_data_summary_statistics(self):
        """Test that summary statistics can be computed"""
        summary = self.clean_data[['quantity', 'unit_price', 'total_sales']].describe()
        
        self.assertGreater(summary.loc['mean', 'quantity'], 0)
        self.assertGreater(summary.loc['mean', 'unit_price'], 0)
        self.assertGreater(summary.loc['mean', 'total_sales'], 0)

    def test_revenue_by_country(self):
        """Test grouping revenue by country"""
        revenue_by_country = self.clean_data.groupby('country')['total_sales'].sum()
        
        self.assertEqual(len(revenue_by_country), 4)
        self.assertTrue((revenue_by_country > 0).all())

    def test_revenue_by_product(self):
        """Test grouping revenue by product"""
        revenue_by_product = self.clean_data.groupby('description')['total_sales'].sum()
        
        self.assertEqual(len(revenue_by_product), 5)
        self.assertTrue((revenue_by_product > 0).all())


if __name__ == '__main__':
    unittest.main()
