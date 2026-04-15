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


def print_recommendations(user_prefs: dict, songs: list, label: str, k: int = 5) -> None:
    """Run the recommender for a single taste profile and print the results."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 52
    print("\n" + "=" * width)
    print(f"{'TOP RECOMMENDATIONS':^{width}}")
    print(f"{label:^{width}}")
    print(f"{'genre: ' + user_prefs['favorite_genre'] + '  |  mood: ' + user_prefs['favorite_mood']:^{width}}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  |  {song['artist']}")
        print(f"    Score : {score:.2f} / 4.00")
        print(f"    Why   :")
        for reason in explanation.split(", "):
            print(f"            * {reason}")
        print("-" * width)


def main() -> None:
    songs = load_songs(SONGS_CSV)
    print(f"Loaded songs: {len(songs)}")

    # ------------------------------------------------------------------ #
    # Taste Profile 1 — High-Energy Pop                                   #
    # Upbeat pop fan who wants feel-good, danceable, produced tracks.     #
    # ------------------------------------------------------------------ #
    high_energy_pop = {
        "favorite_genre":      "pop",    # primary genre identity
        "favorite_mood":       "happy",  # wants feel-good vibes
        "target_energy":       0.85,     # very high energy
        "likes_acoustic":      False,    # prefers polished, produced sound
        "target_valence":      0.85,     # highly positive / joyful
        "target_danceability": 0.85,     # made for the dance floor
    }

    # ------------------------------------------------------------------ #
    # Taste Profile 2 — Chill Lofi                                        #
    # Low-key listener who studies or winds down with mellow, acoustic    #
    # beats and a calm, focused atmosphere.                               #
    # ------------------------------------------------------------------ #
    chill_lofi = {
        "favorite_genre":      "lofi",   # laid-back lo-fi hip-hop
        "favorite_mood":       "chill",  # relaxed and unhurried
        "target_energy":       0.35,     # low energy; soft and calm
        "likes_acoustic":      True,     # warm, organic textures preferred
        "target_valence":      0.55,     # mildly positive; not sad, not euphoric
        "target_danceability": 0.55,     # gentle groove, not made to dance
    }

    # ------------------------------------------------------------------ #
    # Taste Profile 3 — Deep Intense Rock                                 #
    # Hard-rock/metal listener who craves high-octane, raw, aggressive    #
    # tracks with driving tempo and emotional intensity.                  #
    # ------------------------------------------------------------------ #
    deep_intense_rock = {
        "favorite_genre":      "rock",   # guitar-driven rock
        "favorite_mood":       "intense",# high-stakes, adrenaline-fuelled
        "target_energy":       0.90,     # maximum energy
        "likes_acoustic":      False,    # wants distorted, electric sound
        "target_valence":      0.40,     # darker emotional tone
        "target_danceability": 0.60,     # rhythmic but not pop-danceable
    }

    # Run recommendations for each profile
    print_recommendations(high_energy_pop,   songs, label="High-Energy Pop")
    print_recommendations(chill_lofi,        songs, label="Chill Lofi")
    print_recommendations(deep_intense_rock, songs, label="Deep Intense Rock")

    # ================================================================== #
    # ADVERSARIAL / EDGE-CASE PROFILES                                   #
    # Each one is designed to expose a specific weakness in score_song.  #
    # ================================================================== #

    # ------------------------------------------------------------------ #
    # Edge Case 1 — The Sad Headbanger                                   #
    # Wants maximum energy BUT a sad mood.                               #
    # There is only ONE sad song in the catalog (Last Exit South,        #
    # country, energy=0.38). Its energy is the opposite of the target.  #
    # Expected bug: the mood match (+1.0) is overwhelmed by the energy   #
    # penalty — the one sad song likely never surfaces in the top 5.    #
    # ------------------------------------------------------------------ #
    sad_headbanger = {
        "favorite_genre":      "metal",  # wants raw, heavy sound
        "favorite_mood":       "sad",    # but emotionally in a low place
        "target_energy":       0.95,     # max energy — directly conflicts with sad mood
        "likes_acoustic":      False,
        "target_valence":      0.10,     # very dark / low positivity
        "target_danceability": 0.50,
    }

    # ------------------------------------------------------------------ #
    # Edge Case 2 — The Ghost Genre                                      #
    # Requests a genre that does not exist in the catalog ("k-pop").     #
    # The +2.0 genre bonus never fires for any song.                    #
    # Expected bug: scoring silently degrades to mood+energy only,       #
    # with no warning — top results share nothing with k-pop.           #
    # ------------------------------------------------------------------ #
    ghost_genre = {
        "favorite_genre":      "k-pop",  # not in catalog — bonus never fires
        "favorite_mood":       "happy",
        "target_energy":       0.75,
        "likes_acoustic":      False,
        "target_valence":      0.80,
        "target_danceability": 0.80,
    }

    # ------------------------------------------------------------------ #
    # Edge Case 3a & 3b — The Silent Fields Trap                         #
    # These two profiles are IDENTICAL in every field score_song reads   #
    # (genre, mood, energy) but completely opposite in the three fields  #
    # score_song IGNORES (likes_acoustic, target_valence,                #
    # target_danceability).                                              #
    # Expected bug: both profiles produce byte-for-byte identical        #
    # results, proving those three fields are dead weight in scoring.   #
    # ------------------------------------------------------------------ #
    silent_fields_a = {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":       0.40,
        "likes_acoustic":      True,   # <-- loves acoustic
        "target_valence":      0.90,   # <-- wants very positive
        "target_danceability": 0.90,   # <-- wants very danceable
    }

    silent_fields_b = {
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":       0.40,
        "likes_acoustic":      False,  # <-- hates acoustic
        "target_valence":      0.10,   # <-- wants very dark
        "target_danceability": 0.10,   # <-- wants non-danceable
    }

    # ------------------------------------------------------------------ #
    # Edge Case 4 — Genre Hijacks Mood                                   #
    # Asks for lofi + angry mood at high energy.                        #
    # No lofi song in the catalog is "angry" — they are all chill/       #
    # focused. But the +2.0 genre bonus is so dominant that lofi songs  #
    # still occupy the top 3 spots despite being low-energy and calm.   #
    # ------------------------------------------------------------------ #
    genre_hijacks_mood = {
        "favorite_genre":      "lofi",    # lofi songs are all calm
        "favorite_mood":       "angry",   # no lofi song is angry
        "target_energy":       0.90,      # high energy — opposite of lofi
        "likes_acoustic":      True,
        "target_valence":      0.20,
        "target_danceability": 0.50,
    }

    print_recommendations(sad_headbanger,    songs, label="Edge Case 1 — Sad Headbanger")
    print_recommendations(ghost_genre,       songs, label="Edge Case 2 — Ghost Genre (k-pop)")
    print_recommendations(silent_fields_a,   songs, label="Edge Case 3a — Silent Fields (acoustic lover)")
    print_recommendations(silent_fields_b,   songs, label="Edge Case 3b — Silent Fields (acoustic hater)")
    print_recommendations(genre_hijacks_mood, songs, label="Edge Case 4 — Genre Hijacks Mood")


if __name__ == "__main__":
    main()