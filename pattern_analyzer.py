"""
Pattern Analyzer Module
Detects patterns and cycles in emotional data
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Tuple
from emotion_tracker import EmotionEntry, EmotionTracker


class PatternAnalyzer:
    """Analyzes emotion patterns and cycles"""

    def __init__(self, tracker: EmotionTracker):
        """
        Initialize analyzer

        Args:
            tracker: EmotionTracker instance
        """
        self.tracker = tracker

    def find_time_patterns(self, days: int = 30) -> Dict:
        """
        Find patterns based on time of day

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with time-based patterns
        """
        entries = self.tracker.get_entries(days)

        if not entries:
            return {"message": "Not enough data to analyze"}

        # Group by hour of day
        hour_emotions = defaultdict(list)

        for entry in entries:
            dt = datetime.fromisoformat(entry.timestamp)
            hour = dt.hour
            hour_emotions[hour].append((entry.emotion, entry.intensity))

        # Find most common emotion per time period
        time_patterns = {}
        for hour, emotions in hour_emotions.items():
            emotion_counts = defaultdict(int)
            total_intensity = defaultdict(float)

            for emotion, intensity in emotions:
                emotion_counts[emotion] += 1
                total_intensity[emotion] += intensity

            most_common = max(emotion_counts.items(), key=lambda x: x[1])
            avg_intensity = total_intensity[most_common[0]] / most_common[1]

            period = self._get_time_period(hour)
            if period not in time_patterns:
                time_patterns[period] = []

            time_patterns[period].append({
                "hour": hour,
                "emotion": most_common[0],
                "count": most_common[1],
                "avg_intensity": round(avg_intensity, 2)
            })

        return time_patterns

    def _get_time_period(self, hour: int) -> str:
        """Get time period name from hour"""
        if 5 <= hour < 12:
            return "Morning (5AM-12PM)"
        elif 12 <= hour < 17:
            return "Afternoon (12PM-5PM)"
        elif 17 <= hour < 21:
            return "Evening (5PM-9PM)"
        else:
            return "Night (9PM-5AM)"

    def find_trigger_patterns(self, days: int = 30) -> List[Dict]:
        """
        Find common triggers for negative emotions

        Args:
            days: Number of days to analyze

        Returns:
            List of trigger patterns
        """
        entries = self.tracker.get_entries(days)

        negative_emotions = ["Sad", "Anxious", "Angry", "Fearful", "Frustrated",
                            "Lonely", "Stressed", "Overwhelmed"]

        trigger_emotion_map = defaultdict(lambda: defaultdict(int))
        trigger_intensity_map = defaultdict(list)

        for entry in entries:
            if entry.emotion in negative_emotions and entry.trigger:
                trigger = entry.trigger.lower().strip()
                if trigger:
                    trigger_emotion_map[trigger][entry.emotion] += 1
                    trigger_intensity_map[trigger].append(entry.intensity)

        # Compile results
        patterns = []
        for trigger, emotions in trigger_emotion_map.items():
            total_occurrences = sum(emotions.values())
            avg_intensity = sum(trigger_intensity_map[trigger]) / len(trigger_intensity_map[trigger])
            most_common_emotion = max(emotions.items(), key=lambda x: x[1])

            patterns.append({
                "trigger": trigger,
                "occurrences": total_occurrences,
                "primary_emotion": most_common_emotion[0],
                "avg_intensity": round(avg_intensity, 2),
                "all_emotions": dict(emotions)
            })

        # Sort by occurrences
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)
        return patterns

    def find_weekly_cycles(self, weeks: int = 4) -> Dict:
        """
        Find patterns across days of the week

        Args:
            weeks: Number of weeks to analyze

        Returns:
            Dictionary with weekly patterns
        """
        days = weeks * 7
        entries = self.tracker.get_entries(days)

        if not entries:
            return {"message": "Not enough data to analyze"}

        # Group by day of week
        day_emotions = defaultdict(list)
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]

        for entry in entries:
            dt = datetime.fromisoformat(entry.timestamp)
            day_of_week = dt.weekday()
            day_emotions[day_of_week].append((entry.emotion, entry.intensity))

        # Analyze each day
        weekly_patterns = {}
        for day_num in range(7):
            day_name = day_names[day_num]
            emotions = day_emotions[day_num]

            if not emotions:
                continue

            emotion_counts = defaultdict(int)
            emotion_intensities = defaultdict(list)

            for emotion, intensity in emotions:
                emotion_counts[emotion] += 1
                emotion_intensities[emotion].append(intensity)

            most_common = max(emotion_counts.items(), key=lambda x: x[1])
            avg_intensity = sum(emotion_intensities[most_common[0]]) / len(emotion_intensities[most_common[0]])

            weekly_patterns[day_name] = {
                "most_common_emotion": most_common[0],
                "occurrences": most_common[1],
                "avg_intensity": round(avg_intensity, 2),
                "total_entries": len(emotions)
            }

        return weekly_patterns

    def detect_emotion_streaks(self, days: int = 30) -> List[Dict]:
        """
        Detect consecutive days with similar emotions

        Args:
            days: Number of days to analyze

        Returns:
            List of emotion streaks
        """
        entries = self.tracker.get_entries(days)

        if not entries:
            return []

        # Group by date
        date_emotions = defaultdict(list)
        for entry in entries:
            dt = datetime.fromisoformat(entry.timestamp)
            date = dt.date()
            date_emotions[date].append(entry.emotion)

        # Find dominant emotion per day
        daily_dominant = {}
        for date, emotions in date_emotions.items():
            emotion_counts = defaultdict(int)
            for emotion in emotions:
                emotion_counts[emotion] += 1
            dominant = max(emotion_counts.items(), key=lambda x: x[1])[0]
            daily_dominant[date] = dominant

        # Detect streaks
        if not daily_dominant:
            return []

        sorted_dates = sorted(daily_dominant.keys())
        streaks = []
        current_streak = {
            "emotion": daily_dominant[sorted_dates[0]],
            "start_date": sorted_dates[0],
            "end_date": sorted_dates[0],
            "length": 1
        }

        for i in range(1, len(sorted_dates)):
            current_date = sorted_dates[i]
            prev_date = sorted_dates[i - 1]
            current_emotion = daily_dominant[current_date]

            # Check if consecutive and same emotion
            if (current_date - prev_date).days == 1 and current_emotion == current_streak["emotion"]:
                current_streak["end_date"] = current_date
                current_streak["length"] += 1
            else:
                # Save streak if 3+ days
                if current_streak["length"] >= 3:
                    streaks.append(current_streak.copy())

                # Start new streak
                current_streak = {
                    "emotion": current_emotion,
                    "start_date": current_date,
                    "end_date": current_date,
                    "length": 1
                }

        # Add final streak if qualifying
        if current_streak["length"] >= 3:
            streaks.append(current_streak)

        # Convert dates to strings
        for streak in streaks:
            streak["start_date"] = streak["start_date"].isoformat()
            streak["end_date"] = streak["end_date"].isoformat()

        return streaks

    def get_emotion_trends(self, days: int = 30) -> Dict:
        """
        Get overall trends in emotions

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with trend information
        """
        entries = self.tracker.get_entries(days)

        if len(entries) < 2:
            return {"message": "Not enough data to analyze trends"}

        # Split into first half and second half
        mid_point = len(entries) // 2
        first_half = entries[:mid_point]
        second_half = entries[mid_point:]

        def get_stats(entry_list):
            positive = ["Happy", "Excited", "Calm", "Grateful", "Hopeful", "Content"]
            negative = ["Sad", "Anxious", "Angry", "Fearful", "Frustrated",
                       "Lonely", "Stressed", "Overwhelmed"]

            pos_count = sum(1 for e in entry_list if e.emotion in positive)
            neg_count = sum(1 for e in entry_list if e.emotion in negative)
            avg_intensity = sum(e.intensity for e in entry_list) / len(entry_list)

            return {
                "positive_count": pos_count,
                "negative_count": neg_count,
                "avg_intensity": avg_intensity,
                "total": len(entry_list)
            }

        first_stats = get_stats(first_half)
        second_stats = get_stats(second_half)

        # Calculate trends
        positive_trend = second_stats["positive_count"] - first_stats["positive_count"]
        negative_trend = second_stats["negative_count"] - first_stats["negative_count"]
        intensity_trend = second_stats["avg_intensity"] - first_stats["avg_intensity"]

        return {
            "first_period": first_stats,
            "second_period": second_stats,
            "positive_change": positive_trend,
            "negative_change": negative_trend,
            "intensity_change": round(intensity_trend, 2),
            "overall_sentiment": "improving" if positive_trend > 0 else "declining" if positive_trend < 0 else "stable"
        }
