import requests
import unittest

BASE_URL = "http://localhost:5001/tracks"

class TestTrackCatalog(unittest.TestCase):

    def test_add_track_success(self):
        track = {"title": "Blinding Lights", "artist": "Weekend"}
        with open("/Users/rishik/Desktop/Catelogue/wavs/Blinding Lights.wav", "rb") as f:
            files = {"file": ("Blinding_Lights.wav", f, "audio/wav")}
            rsp = requests.post(BASE_URL, data=track, files=files)
        self.assertEqual(rsp.status_code, 201)
        self.assertIn("track_id", rsp.json())

    def test_add_track_missing_fields(self):
        track = {"title": "Incomplete"}  
        rsp = requests.post(BASE_URL, json=track)
        self.assertEqual(rsp.status_code, 400)
        self.assertIn("error", rsp.json())

    def test_get_tracks(self):
        rsp = requests.get(BASE_URL)
        self.assertEqual(rsp.status_code, 200)
        self.assertIsInstance(rsp.json(), list)

    def test_delete_track_success(self):
        track = {"title": "Song to Delete", "artist": "Test Artist"}
        with open("/Users/rishik/Desktop/Catelogue/wavs/Blinding Lights.wav", "rb") as f:
            files = {"file": ("Blinding_Lights.wav", f, "audio/wav")}
            add_rsp = requests.post(BASE_URL, data=track, files=files)
        self.assertEqual(add_rsp.status_code, 201)
        delete_rsp = requests.delete(BASE_URL, json={"title": "Song to Delete", "artist": "Test Artist"})
    
        self.assertEqual(delete_rsp.status_code, 200)
        self.assertIn("Track 'Song to Delete' by Test Artist deleted", delete_rsp.json()["message"])

    def test_delete_track_not_found(self):
        delete_rsp = requests.delete(BASE_URL, json={"title": "Nonexistent Song", "artist": "Unknown Artist"})
        self.assertEqual(delete_rsp.status_code, 404)
        self.assertIn("Track 'Nonexistent Song' by Unknown Artist not found", delete_rsp.json()["error"])

    def test_stream_audio_missing_fields(self):
        missing_artist = {"title": "Blinding Lights"}
        rsp = requests.post(f"{BASE_URL}/audio", json=missing_artist)
        self.assertEqual(rsp.status_code, 400)
        self.assertIn("error", rsp.json())
        missing_title = {"artist": "The Weeknd"}
        rsp = requests.post(f"{BASE_URL}/audio", json=missing_title)
        self.assertEqual(rsp.status_code, 400)
        self.assertIn("error", rsp.json())



    # def test_delete_track_not_found(self):
    #     delete_url = f"{BASE_URL}/99999"
    #     rsp = requests.delete(delete_url)
    #     self.assertEqual(rsp.status_code, 404)
    #     self.assertIn("Track not found", rsp.json()["error"])

if __name__ == "__main__":
    unittest.main()
