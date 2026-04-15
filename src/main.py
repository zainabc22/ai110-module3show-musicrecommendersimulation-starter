"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Taste Profile: The Late Night Focus Listener ---
    # Prefers quiet, acoustic lo-fi for late-night study or work sessions.
    # Low energy target keeps the mood grounded without tipping into silence.
    # Neutral-positive valence avoids both euphoria and melancholy.
    user_prefs = {
        "favorite_genre":      "lofi",   # primary genre identity
        "favorite_mood":       "chill",  # situational mood right now
        "target_energy":       0.38,     # low-to-mid; calm but not ambient
        "likes_acoustic":      True,     # prefers organic over electronic textures
        "target_valence":      0.58,     # neutral-positive; steady not euphoric
        "target_danceability": 0.60,     # moderate rhythm is fine
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()

test