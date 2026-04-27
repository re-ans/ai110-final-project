"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import Recommender, UserProfile, Song
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main() -> None:
    """
    Main function to run the music recommender.
    """
    logging.info("Starting the music recommender system.")
    
    # Load songs from the CSV file
    try:
        songs_data = load_songs_from_csv("data/songs.csv")
        songs = [Song(**s) for s in songs_data]
        logging.info(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        logging.error("Error: The song data file was not found at 'data/songs.csv'.")
        return
    except Exception as e:
        logging.error(f"An error occurred while loading songs: {e}")
        return

    # Create a recommender instance
    recommender = Recommender(songs)

    # Example user profile
    user_profile = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    logging.info(f"User profile: {user_profile}")

    # Get recommendations
    try:
        recommendations = recommender.recommend(user_profile, k=5)
        logging.info(f"Generated {len(recommendations)} recommendations.")
    except Exception as e:
        logging.error(f"An error occurred during recommendation: {e}")
        return

    # Print recommendations
    print("\nTop recommendations:\n")
    if not recommendations:
        print("No recommendations found for the given profile.")
    else:
        for song, confidence in recommendations:
            explanation = recommender.explain_recommendation(user_profile, song)
            print(f"'{song.title}' by {song.artist}")
            print(f"  Confidence: {confidence:.2f}")
            print(f"  Reason: {explanation}")
            print()

    logging.info("Music recommender system finished.")


def load_songs_from_csv(csv_path: str):
    """
    Placeholder for the actual load_songs function.
    This will be replaced by the real implementation.
    """
    # This is a simplified version. The actual function is in recommender.py
    import csv
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs



if __name__ == "__main__":
    main()
