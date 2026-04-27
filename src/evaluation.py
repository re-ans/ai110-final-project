"""
Evaluation script for the music recommender system.

This script runs a series of tests to evaluate the reliability and quality of the recommendations.
"""

import logging
from typing import List, Dict, Any
from src.recommender import Recommender, Song, UserProfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_evaluation():
    """
    Runs the full evaluation suite.
    """
    logging.info("Starting recommender system evaluation.")

    # Load test data
    songs = load_test_songs()
    recommender = Recommender(songs)

    # Define test cases
    test_cases = [
        {
            "name": "Pop lover",
            "profile": UserProfile(favorite_genre="Pop", favorite_mood="Happy", target_energy=0.8, likes_acoustic=False),
            "expected_top_genre": "Pop",
        },
        {
            "name": "Lofi listener",
            "profile": UserProfile(favorite_genre="Lofi", favorite_mood="Chill", target_energy=0.3, likes_acoustic=True),
            "expected_top_genre": "Lofi",
        },
        {
            "name": "Mismatched preferences",
            "profile": UserProfile(favorite_genre="Rock", favorite_mood="Energetic", target_energy=0.9, likes_acoustic=False),
            "expected_top_genre": None,  # Expect no strong recommendation
        }
    ]

    results = []
    for test in test_cases:
        logging.info(f"Running test case: {test['name']}")
        recommendations = recommender.recommend(test['profile'], k=1)
        
        if recommendations:
            top_rec, confidence = recommendations[0]
            is_pass = top_rec.genre.lower() == test['expected_top_genre'].lower() if test['expected_top_genre'] else False
            results.append({
                "test_case": test['name'],
                "pass": is_pass,
                "confidence": confidence,
                "details": f"Recommended '{top_rec.title}' with confidence {confidence:.2f}"
            })
        else:
            # If no recommendation, it's a pass if none was expected
            is_pass = test['expected_top_genre'] is None
            results.append({
                "test_case": test['name'],
                "pass": is_pass,
                "confidence": 0,
                "details": "No recommendation returned."
            })

    # Print summary
    print("\n--- Evaluation Summary ---")
    passed_count = sum(1 for r in results if r['pass'])
    total_count = len(results)
    print(f"Passed {passed_count}/{total_count} test cases.")

    for r in results:
        status = "✅ Pass" if r['pass'] else "❌ Fail"
        print(f"  - {r['test_case']}: {status} ({r['details']})")
    
    logging.info("Evaluation finished.")

def load_test_songs() -> List[Song]:
    """
    Loads a small, fixed set of songs for testing.
    """
    return [
        Song(id=1, title="Sunshine Pop", artist="The Upbeats", genre="Pop", mood="Happy", energy=0.85, tempo_bpm=128, valence=0.9, danceability=0.7, acousticness=0.1),
        Song(id=2, title="Midnight Lofi", artist="Chill Beats", genre="Lofi", mood="Chill", energy=0.2, tempo_bpm=80, valence=0.4, danceability=0.5, acousticness=0.9),
        Song(id=3, title="Acoustic Morning", artist="The Folk", genre="Acoustic", mood="Calm", energy=0.4, tempo_bpm=110, valence=0.6, danceability=0.6, acousticness=0.95),
    ]

if __name__ == "__main__":
    run_evaluation()
