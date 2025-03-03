from flask import Flask, request, jsonify
from repository import Repository  

app = Flask(__name__)
repo = Repository("tracks")  

@app.route("/tracks", methods=["POST"])
def add_track():
    title = request.form.get("title")
    artist = request.form.get("artist")
    file = request.files.get("file")  
    
    if not title or not artist or not file:
        return jsonify({"error": "Missing title, artist, or file"}), 400
    audio_data = file.read()
    track_id = repo.insert(title, artist, audio_data)
    return jsonify({"message": "Track added", "track_id": track_id}), 201


@app.route("/tracks", methods=["GET"])
def get_tracks():
    tracks = repo.get()
    return jsonify(tracks), 200

# @app.route("/tracks/<int:track_id>", methods=["DELETE"])
# def delete_track(track_id):
#     if repo.delete_track(track_id):
#         return jsonify({"message": "Track deleted"}), 200
#     else:
#         return jsonify({"error": "Track not found"}), 404

# @app.route("/tracks/find", methods=["GET"])
# def find_track():
#     title = request.args.get("title")
#     artist = request.args.get("artist")
#     if not title or not artist:
#         return jsonify({"error": "Missing title or artist"}), 400
#     track_id = repo.find_track(title, artist)
#     if track_id:
#         return jsonify({
#             "message": "Track found in catalog",
#             "track_id": track_id,
#         }), 200
#     else:
#         return jsonify({
#             "message": "Track not found in catalog",
#         }), 404

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
