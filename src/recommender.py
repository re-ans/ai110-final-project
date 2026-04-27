import csv
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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Tuple[Song, float]]:
        """Score all songs and return top k sorted by score."""
        scored_songs = []
        for song in self.songs:
            score, _ = self._score_song_obj(user, song)
            scored_songs.append((song, score))
        
        # Sort by score descending and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Normalize scores to be between 0 and 1 for confidence
        max_score = scored_songs[0][1] if scored_songs else 1.0
        
        recommendations = []
        for song, score in scored_songs[:k]:
            confidence = score / max_score if max_score > 0 else 0
            recommendations.append((song, confidence))
            
        return recommendations

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song was recommended."""
        _, reasons = self._score_song_obj(user, song)
        return " + ".join(reasons) if reasons else "Matches your taste profile"
    
    def _score_song_obj(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Internal scoring for Song objects."""
        score = 0.0
        reasons = []
        
        # Genre match (weight: 2.0)
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"genre match ({song.genre})")
        
        # Mood match (weight: 1.5)
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append(f"mood match ({song.mood})")
        
        # Energy proximity (weight: 1.5)
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0, 1.5 * (1.0 - energy_diff))
        score += energy_score
        reasons.append(f"energy {song.energy:.2f} (target: {user.target_energy})")
        
        # Acoustic preference (weight: 0.5)
        if user.likes_acoustic and song.acousticness > 0.5:
            score += 0.5
            reasons.append("acoustic match")
        elif not user.likes_acoustic and song.acousticness <= 0.5:
            score += 0.5
            reasons.append("produced sound")
        
        return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns list of dictionaries.
    Converts numeric fields to appropriate types.
    """
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to float
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences.
    Returns (score, explanation_string).
    """
    score = 0.0
    reasons = []
    
    # Genre match (weight: 2.0)
    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 2.0
        reasons.append(f"genre match ({song['genre']})")
    
    # Mood match (weight: 1.5)
    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 1.5
        reasons.append(f"mood match ({song['mood']})")
    
    # Energy proximity (weight: 1.5)
    target_energy = user_prefs.get('energy', 0.5)
    energy_diff = abs(song['energy'] - target_energy)
    energy_score = max(0, 1.5 * (1.0 - energy_diff))
    score += energy_score
    reasons.append(f"energy {song['energy']:.2f}")
    
    # Acoustic preference (weight: 0.5)
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if likes_acoustic and song['acousticness'] > 0.5:
        score += 0.5
        reasons.append("acoustic match")
    elif not likes_acoustic and song['acousticness'] <= 0.5:
        score += 0.5
        reasons.append("produced sound")
    
    explanation = " + ".join(reasons)
    return score, explanation

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs and returns top k recommendations sorted by score.
    Returns list of (song_dict, score, explanation) tuples.
    """
    if not songs:
        return []
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]
