import requests
import unittest

BASE_URL = "http://localhost:5001/tracks"

class TestTrackCatalog(unittest.TestCase):

    def test_add_track_success(self):
        track = {"title": "Bohemian Rhapsody", "artist": "Queen"}
        headers = {"Content-Type": "application/json"}
        rsp = requests.post(BASE_URL, json=track, headers=headers)
        self.assertEqual(rsp.status_code, 201)
        self.assertIn("track_id", rsp.json())

    def test_add_track_missing_fields(self):
        """Test adding a track (Failure - Missing Fields)"""
        track = {"title": "Incomplete"}  # Missing artist
        headers = {"Content-Type": "application/json"}
        
        rsp = requests.post(BASE_URL, json=track, headers=headers)
        self.assertEqual(rsp.status_code, 400)
        self.assertIn("error", rsp.json())

    def test_get_tracks(self):
        """Test retrieving all tracks"""
        rsp = requests.get(BASE_URL)
        self.assertEqual(rsp.status_code, 200)
        self.assertIsInstance(rsp.json(), list)

    def test_find_track_success(self):
        """Test finding an existing track"""
        find_url = f"{BASE_URL}/find?title=Bohemian Rhapsody&artist=Queen"
        rsp = requests.get(find_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertIn("track_id", rsp.json())

    def test_find_track_not_found(self):
        """Test searching for a non-existent track"""
        find_url = f"{BASE_URL}/find?title=Fake Song&artist=Unknown"
        rsp = requests.get(find_url)
        self.assertEqual(rsp.status_code, 404)
        self.assertIn("Track not found", rsp.json()["message"])

    def test_delete_track_success(self):
        """Test deleting a track"""
        track = {"title": "Song to Delete", "artist": "Artist"}
        headers = {"Content-Type": "application/json"}
        add_rsp = requests.post(BASE_URL, json=track, headers=headers)

        track_id = add_rsp.json()["track_id"]
        delete_url = f"{BASE_URL}/{track_id}"
        
        rsp = requests.delete(delete_url)
        self.assertEqual(rsp.status_code, 200)
        self.assertIn("Track deleted", rsp.json()["message"])

    def test_delete_track_not_found(self):
        """Test deleting a non-existent track"""
        delete_url = f"{BASE_URL}/99999"
        rsp = requests.delete(delete_url)
        self.assertEqual(rsp.status_code, 404)
        self.assertIn("Track not found", rsp.json()["error"])

if __name__ == "__main__":
    unittest.main()
