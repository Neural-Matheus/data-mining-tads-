import unittest
import json
from datetime import datetime, timedelta, timezone
from metrics import (
    calculate_min, calculate_max, calculate_mean, calculate_median, calculate_stddev,
    calculate_account_age, extract_metrics, generate_statistics, generate_csv, process_metrics
)
from locations import (
    process_locations, generate_locations_csv, process_locations_data
)

class TestMetricsFunctions(unittest.TestCase):
    def test_calculate_min(self):
        self.assertEqual(calculate_min([3, -1, 4, 1, 5]), -1)
        self.assertEqual(calculate_min([]), 0)

    def test_calculate_max(self):
        self.assertEqual(calculate_max([3, -1, 4, 1, 5]), 5)
        self.assertEqual(calculate_max([]), 0)

    def test_calculate_mean(self):
        self.assertEqual(calculate_mean([1, 2, 3, 4, 5]), 3)
        self.assertAlmostEqual(calculate_mean([1.5, 2.5, 3.5]), 2.5)
        self.assertEqual(calculate_mean([]), 0)

    def test_calculate_median(self):
        self.assertEqual(calculate_median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(calculate_median([1, 2, 3, 4]), 2.5)
        self.assertEqual(calculate_median([3]), 3)
        self.assertEqual(calculate_median([]), 0)
        self.assertEqual(calculate_median([5, 1, 3]), 3)

    def test_calculate_stddev(self):
        self.assertAlmostEqual(calculate_stddev([2, 4, 4, 4, 5, 5, 7, 9]), 2.0, places=2)
        self.assertEqual(calculate_stddev([]), 0)
        self.assertEqual(calculate_stddev([100]), 0)
        self.assertAlmostEqual(calculate_stddev([1.0, 2.0, 3.0]), 0.82, places=2)

    def test_calculate_account_age(self):
        reference = datetime(2025, 3, 29, tzinfo=timezone.utc)
        created_at = (reference - timedelta(days=365)).isoformat().replace('+00:00', 'Z')
        expected_age = 365 / 365.25
        self.assertAlmostEqual(calculate_account_age(created_at, reference), expected_age, places=2)

    def test_extract_metrics(self):
        reference = datetime(2025, 3, 29, tzinfo=timezone.utc)
        users = [
            {"followers_count": 10, "following_count": 5, "created_at": "2023-03-29T12:00:00Z"},
            {"followers_count": 20, "following_count": 10, "created_at": "2022-03-29T12:00:00Z"}
        ]
        metrics = extract_metrics(users, reference)
        self.assertEqual(metrics['followers_count'], [10, 20])
        self.assertEqual(metrics['following_count'], [5, 10])
        self.assertEqual(len(metrics['account_age']), 2)
        self.assertTrue(all(age >= 0 for age in metrics['account_age']))

    def test_generate_statistics(self):
        values = [1, 2, 3, 4, 5]
        stats = generate_statistics(values)
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 5)
        self.assertEqual(stats['avg'], 3.0)
        self.assertEqual(stats['median'], 3.0)
        self.assertGreater(stats['std'], 0)
        stats_empty = generate_statistics([])
        self.assertEqual(stats_empty, {'min': 0, 'max': 0, 'avg': 0, 'median': 0, 'std': 0})

    def test_generate_csv(self):
        stats = {
            'followers_count': {'min': 1, 'max': 10, 'avg': 5.5, 'median': 5.5, 'std': 3.5},
            'following_count': {'min': 2, 'max': 8, 'avg': 5.0, 'median': 5.0, 'std': 2.0}
        }
        csv_output = generate_csv(stats)
        self.assertTrue(csv_output.startswith("Metric,min,max,avg,median,std"))
        self.assertIn("followers_count,1,10,5.5,5.5,3.5", csv_output)
        self.assertIn("following_count,2,8,5.0,5.0,2.0", csv_output)

    def test_process_metrics(self):
        reference = datetime(2025, 3, 29, tzinfo=timezone.utc)
        users = [
            {"followers_count": 15, "following_count": 7, "created_at": "2023-03-29T12:00:00Z"},
            {"followers_count": 25, "following_count": 12, "created_at": "2022-03-29T12:00:00Z"},
            {"followers_count": 30, "following_count": 15, "created_at": "2020-03-29T12:00:00Z"}
        ]
        metrics_csv = process_metrics(users, reference)
        self.assertIn("Metric,min,max,avg,median,std", metrics_csv)
        self.assertIn("followers_count", metrics_csv)
        self.assertIn("following_count", metrics_csv)

class TestLocationsFunctions(unittest.TestCase):
    def test_process_locations(self):
        users = [
            {"location": "Brazil"},
            {"location": " brazil "},
            {"location": "USA"},
            {"location": ""},
            {"location": None},
            {}
        ]
        locations = process_locations(users)
        self.assertEqual(locations, [("brazil", 2), ("usa", 1)])

    def test_generate_locations_csv(self):
        locations = [("brazil", 2), ("usa", 1)]
        csv_output = generate_locations_csv(locations)
        self.assertTrue(csv_output.startswith("Location,Occurrences"))
        self.assertIn("brazil,2", csv_output)
        self.assertIn("usa,1", csv_output)

    def test_process_locations_data(self):
        users = [
            {"location": "USA"},
            {"location": "Brazil"},
            {"location": "USA"}
        ]
        locations_csv = process_locations_data(users)
        self.assertIn("Location,Occurrences", locations_csv)
        self.assertIn("usa,2", locations_csv)
        self.assertIn("brazil,1", locations_csv)

if __name__ == "__main__":
    unittest.main()
