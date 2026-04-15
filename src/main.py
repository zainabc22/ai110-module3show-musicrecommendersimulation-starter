"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
import sys

# Allow running as: python -m src.main  OR  python src/main.py
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs

# Resolve data/songs.csv relative to the project root (one level up from src/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_CSV = os.path.join(_PROJECT_ROOT, "data", "songs.csv")


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    # --- Taste Profile: The Pop/Happy Listener ---
    # Upbeat, high-energy pop fan who wants feel-good, danceable tracks.
    user_prefs = {
        "favorite_genre":      "pop",    # primary genre identity
        "favorite_mood":       "happy",  # situational mood right now
        "target_energy":       0.80,     # high energy; energetic and upbeat
        "likes_acoustic":      False,    # prefers produced over organic textures
        "target_valence":      0.80,     # high positivity; feel-good tracks
        "target_danceability": 0.80,     # highly danceable
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 52
    print("\n" + "=" * width)
    print(f"{'TOP RECOMMENDATIONS':^{width}}")
    print(f"{'genre: ' + user_prefs['favorite_genre'] + '  |  mood: ' + user_prefs['favorite_mood']:^{width}}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  |  {song['artist']}")
        print(f"    Score : {score:.2f} / 4.00")
        print(f"    Why   :")
        for reason in explanation.split(", "):
            print(f"            * {reason}")
        print("-" * width)


if __name__ == "__main__":
    main()