import unittest
import os
from refactor_data import *
import get_data
from data_manipulation import *
from main import *
from plot import *
import pandas as pd


class TestSeaTemps(unittest.TestCase):
    def test_iterable(self):
        iter(get_data.SeaTemps())

    # make sure the website returns a status code
    def test_get_data(self):
        self.assertTrue(get_data.SeaTemps().response == 200)


# Tests if the values are refactored properly
class TestRefactor_Data(unittest.TestCase):
    def test_type_conversion(self):
        test1 = DisplaySeaTemps(1945, 0.47, 0.23, 0.65)
        self.assertEqual(1945, test1.year)
        self.assertEqual(0.47, test1.avg_anomaly)
        self.assertEqual(0.23, test1.lower_confidence)
        self.assertEqual(0.65, test1.upper_confidence)

    def test_hurricane_conversion(self):
        test2 = Storm(2005, 25, 15, 8)
        self.assertEqual(2005, test2.year)
        self.assertEqual(25, test2.storms)
        self.assertEqual(15, test2.hurricanes)
        self.assertEqual(8, test2.majors)


class Test_Data_Manipulation(unittest.TestCase):
    sea_test = SeaTemps()

    # Checks to make sure a Pandas dataframe is created
    def test_avg_per_decade(self):
        self.assertEqual(type(average_per_decade(self.sea_test.sea_values)), pd.DataFrame)
        self.assertEqual(type(avg_lower_upper_decade(self.sea_test.sea_values)), pd.DataFrame)
        self.assertEqual(type(merge(self.sea_test.sea_values)), pd.DataFrame)


class TestStormData(unittest.TestCase):
    def test_iterable(self):
        iter(get_data.StormData())

    def test_get_data(self):
        self.assertTrue(StormData().response == 200)

    def test_stormCSV(self):
        get_data.StormData().stormCSV()
        self.assertTrue(os.path.exists('storm-data.csv'))


class TestPlot(unittest.TestCase):
    def test_plot_standard_anomalies(self):
        plot_standard_anomalies(SeaTemps().sea_values)
        self.assertTrue(os.path.exists('sst_standard_anomalies.png'))

    def test_plot_standard_confidence(self):
        plot_standard_confidence(SeaTemps().sea_values)
        self.assertTrue(os.path.exists('sst_standard_confidence.png'))

    def test_graphStorm(self):
        graphStorm(StormData().hurricane_values)
        self.assertTrue(os.path.exists('stormsperyear.png'))

    def test_graph_severe_hurricanes(self):
        graph_severe_hurricanes(StormData().hurricane_values)
        self.assertTrue(os.path.exists('hurricanes_majperyear.png'))

    def test_combine_anomaly_storms(self):
        combine_anomaly_storms(StormData().hurricane_values, SeaTemps().sea_values)
        self.assertTrue(os.path.exists('Anomalies_TropicalStorms.png'))

    def test_combine_anomaly_majors(self):
        combine_anomaly_majors(StormData().hurricane_values, SeaTemps().sea_values)
        self.assertTrue(os.path.exists('Anomalies_MajorHurricanes.png'))


if __name__ == '__main__':
    unittest.main()
