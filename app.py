from flask import Flask, request, jsonify
from repository import Repository  

app = Flask(__name__)
repo = Repository("tracks")  

@app.route("/tracks", methods=["POST"])
def add_track():
    data = request.get_json()
    title = data.get("title")
    artist = data.get("artist")

    if not title or not artist:
        return jsonify({"error": "Missing title or artist"}), 400

    track_id = repo.insert(title, artist)

    return jsonify({"message": "Track added", "track_id": track_id}), 201


@app.route("/tracks", methods=["GET"])
def get_tracks():
    tracks = repo.get()
    return jsonify(tracks), 200

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
