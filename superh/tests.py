import unittest
from unittest.mock import patch
import json
from req import get_tallest_hero_by_gender_and_work

# сам не профи в тестировании апи, но слышал, что через моки нужно делать, поэтому вот

class TestTallestHeroFunction(unittest.TestCase):

    sample_data = [
        {
            "id": 1,
            "name": "Hero1",
            "appearance": {"gender": "Male", "height": ["6'0", "183 cm"]},
            "work": {"occupation": "Engineer"}
        },
        {
            "id": 2,
            "name": "Hero2",
            "appearance": {"gender": "Female", "height": ["5'8", "173 cm"]},
            "work": {"occupation": ""}
        },
        {
            "id": 3,
            "name": "Hero3",
            "appearance": {"gender": "Male", "height": ["6'5", "196 cm"]},
            "work": {"occupation": ""}
        },
        {
            "id": 4,
            "name": "Hero4",
            "appearance": {"gender": "Female", "height": ["6'0", "183 cm"]},
            "work": {"occupation": "Scientist"}
        }
    ]

    @patch('requests.get')
    def test_male_with_job(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: self.sample_data

        hero = get_tallest_hero_by_gender_and_work('Male', True)
        self.assertIsNotNone(hero)
        self.assertEqual(hero['name'], 'Hero1')  # Hero1 - мужик с работой, рост 183

    @patch('requests.get')
    def test_male_without_job(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: self.sample_data

        hero = get_tallest_hero_by_gender_and_work('Male', False)
        self.assertIsNotNone(hero)
        self.assertEqual(hero['name'], 'Hero3')  # Hero3 - мужик без работы, рост 196

    @patch('requests.get')
    def test_female_with_job(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: self.sample_data

        hero = get_tallest_hero_by_gender_and_work('Female', True)
        self.assertIsNotNone(hero)
        self.assertEqual(hero['name'], 'Hero4')  # Hero4 - женщина с работой, рост 183

    @patch('requests.get')
    def test_female_without_job(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: self.sample_data

        hero = get_tallest_hero_by_gender_and_work('Female', False)
        self.assertIsNotNone(hero)
        self.assertEqual(hero['name'], 'Hero2')  # Hero2 - женщина без работы, рост 173

    @patch('requests.get')
    def test_no_hero_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: self.sample_data

        # Пол, которого нет в выборке
        hero = get_tallest_hero_by_gender_and_work('Other', True)
        self.assertIsNone(hero)

    @patch('requests.get')
    def test_empty_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: []

        hero = get_tallest_hero_by_gender_and_work('Male', True)
        self.assertIsNone(hero)

if __name__ == '__main__':
    unittest.main()
