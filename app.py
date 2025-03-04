from flask import Flask, request, jsonify , Response
from repository import Repository  

app = Flask(__name__)
repo = Repository("tracks")  

@app.route("/tracks", methods=["POST"])
def add_track():
    try:
        title = request.form.get("title")
        artist = request.form.get("artist")
        file = request.files.get("file")  
    
        if not title or not artist or not file:
            return jsonify({"error": "Missing title, artist, or file"}), 400
        
        # if repo.find_track(title, artist):
        #     return jsonify({"error": "Track already exists"}), 409 
        
        audio_data = file.read()
        track_id = repo.insert(title, artist, audio_data)
        return jsonify({"message": "Track added", "track_id": track_id}), 201
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/tracks", methods=["GET"])
def get_tracks():
    try:
        tracks = repo.get()
        return jsonify(tracks), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/tracks", methods=["DELETE"])
def delete_track():
    try: 
        data = request.get_json()
        if not data or "title" not in data or "artist" not in data:
            return jsonify({"error": "Missing title or artist"}), 400

        title = data["title"]
        artist = data["artist"]

        if repo.delete_track(title, artist):
            return jsonify({"message": f"Track '{title}' by {artist} deleted"}), 200
        else:
            return jsonify({"error": f"Track '{title}' by {artist} not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/tracks/audio", methods=["POST"])
def stream_audio():
    try:
        data = request.get_json()
        if not data or "title" not in data or "artist" not in data:
            return jsonify({"error": "Missing title or artist"}), 400

        title = data["title"]
        artist = data["artist"]

    
        audio_data = repo.get_audio(title, artist)
        if not audio_data:
            return jsonify({"error": "Track not found"}), 404

    
        return Response(audio_data, mimetype="audio/wav")
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
