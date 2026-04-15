from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse a CSV file of songs and return each row as a dict with typed numeric fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (+2.0 genre, +1.0 mood, +0–1.0 energy) and return (score, reasons)."""
    score = 0.0
    reasons = []

    # +2.0 for genre match
    if song.get("genre", "").lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append(f"genre match (+2.0): {song['genre']}")

    # +1.0 for mood match
    if song.get("mood", "").lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.0
        reasons.append(f"mood match (+1.0): {song['mood']}")

    # Up to +1.0 for energy similarity: 1.0 - |song.energy - target_energy|
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_points = round(1.0 - abs(float(song.get("energy", 0.5)) - target_energy), 2)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points}): song={song.get('energy')} | target={target_energy}")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    # Score every song in the catalog using score_song as the judge
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() returns a NEW list ranked highest-to-lowest; the original is untouched
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return ranked[:k]
