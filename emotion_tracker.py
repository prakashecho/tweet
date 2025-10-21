"""
Emotion Tracker Module
Handles emotion logging and data storage
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class EmotionEntry:
    """Represents a single emotion journal entry"""

    EMOTION_TYPES = [
        "Happy", "Sad", "Anxious", "Angry", "Fearful", "Disgusted",
        "Surprised", "Excited", "Calm", "Frustrated", "Lonely",
        "Grateful", "Hopeful", "Stressed", "Content", "Overwhelmed"
    ]

    def __init__(self, emotion: str, intensity: int, trigger: str = "",
                 notes: str = "", timestamp: Optional[str] = None):
        """
        Initialize an emotion entry

        Args:
            emotion: Type of emotion (from EMOTION_TYPES)
            intensity: Intensity level (1-10)
            trigger: What triggered this emotion
            notes: Additional notes
            timestamp: ISO format timestamp (auto-generated if None)
        """
        self.emotion = emotion
        self.intensity = max(1, min(10, intensity))  # Clamp between 1-10
        self.trigger = trigger
        self.notes = notes
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert entry to dictionary"""
        return {
            "emotion": self.emotion,
            "intensity": self.intensity,
            "trigger": self.trigger,
            "notes": self.notes,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'EmotionEntry':
        """Create entry from dictionary"""
        return cls(
            emotion=data["emotion"],
            intensity=data["intensity"],
            trigger=data.get("trigger", ""),
            notes=data.get("notes", ""),
            timestamp=data["timestamp"]
        )


class EmotionTracker:
    """Manages emotion entries and data persistence"""

    def __init__(self, data_file: str = "data/emotions.json"):
        """
        Initialize tracker

        Args:
            data_file: Path to JSON file for storing emotions
        """
        self.data_file = data_file
        self.entries: List[EmotionEntry] = []
        self._ensure_data_directory()
        self.load_entries()

    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def add_entry(self, emotion: str, intensity: int, trigger: str = "",
                  notes: str = "") -> EmotionEntry:
        """
        Add a new emotion entry

        Args:
            emotion: Type of emotion
            intensity: Intensity level (1-10)
            trigger: What triggered this emotion
            notes: Additional notes

        Returns:
            The created EmotionEntry
        """
        entry = EmotionEntry(emotion, intensity, trigger, notes)
        self.entries.append(entry)
        self.save_entries()
        return entry

    def load_entries(self):
        """Load entries from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = [EmotionEntry.from_dict(e) for e in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading entries: {e}")
                self.entries = []
        else:
            self.entries = []

    def save_entries(self):
        """Save entries to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            data = [entry.to_dict() for entry in self.entries]
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_entries(self, days: Optional[int] = None) -> List[EmotionEntry]:
        """
        Get emotion entries

        Args:
            days: Number of days to look back (None for all entries)

        Returns:
            List of EmotionEntry objects
        """
        if days is None:
            return self.entries

        cutoff = datetime.now().timestamp() - (days * 86400)
        return [
            entry for entry in self.entries
            if datetime.fromisoformat(entry.timestamp).timestamp() >= cutoff
        ]

    def get_emotion_stats(self, days: Optional[int] = None) -> Dict:
        """
        Get statistics about emotions

        Args:
            days: Number of days to analyze (None for all time)

        Returns:
            Dictionary with emotion statistics
        """
        entries = self.get_entries(days)

        if not entries:
            return {"total_entries": 0}

        emotion_counts = {}
        emotion_intensities = {}

        for entry in entries:
            emotion = entry.emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            if emotion not in emotion_intensities:
                emotion_intensities[emotion] = []
            emotion_intensities[emotion].append(entry.intensity)

        # Calculate averages
        emotion_avg_intensity = {
            emotion: sum(intensities) / len(intensities)
            for emotion, intensities in emotion_intensities.items()
        }

        return {
            "total_entries": len(entries),
            "emotion_counts": emotion_counts,
            "emotion_avg_intensity": emotion_avg_intensity,
            "most_common_emotion": max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None
        }
