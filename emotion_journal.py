#!/usr/bin/env python3
"""
Emotion Journal - Daily Emotion Tracking and Analysis
Main CLI Application
"""

import sys
from datetime import datetime
from emotion_tracker import EmotionTracker, EmotionEntry
from pattern_analyzer import PatternAnalyzer
from solution_engine import SolutionEngine


class EmotionJournalCLI:
    """Command-line interface for the emotion journal"""

    def __init__(self):
        """Initialize the application"""
        self.tracker = EmotionTracker()
        self.analyzer = PatternAnalyzer(self.tracker)
        self.solutions = SolutionEngine(self.tracker)
        self.running = True

    def clear_screen(self):
        """Clear the terminal screen"""
        print("\n" * 2)

    def print_header(self, text: str):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def print_menu(self):
        """Display main menu"""
        self.print_header("EMOTION JOURNAL - Main Menu")
        print("\n1.  Log New Emotion")
        print("2.  View Recent Entries")
        print("3.  View Statistics")
        print("4.  Analyze Patterns")
        print("5.  Get Solutions & Recommendations")
        print("6.  View Emotion Trends")
        print("7.  Emergency Resources")
        print("8.  Exit")
        print("\n" + "-" * 60)

    def log_emotion(self):
        """Log a new emotion entry"""
        self.print_header("Log New Emotion")

        # Display emotion options
        print("\nAvailable Emotions:")
        for i, emotion in enumerate(EmotionEntry.EMOTION_TYPES, 1):
            print(f"{i:2d}. {emotion}")

        # Get emotion
        while True:
            try:
                choice = input("\nSelect emotion number (or type name): ").strip()

                # Check if it's a number
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(EmotionEntry.EMOTION_TYPES):
                        emotion = EmotionEntry.EMOTION_TYPES[idx]
                        break
                # Check if it's a valid emotion name
                elif choice in EmotionEntry.EMOTION_TYPES:
                    emotion = choice
                    break
                else:
                    print("Invalid choice. Please try again.")
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")

        # Get intensity
        while True:
            try:
                intensity = int(input("\nIntensity (1-10): ").strip())
                if 1 <= intensity <= 10:
                    break
                print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")

        # Get trigger
        trigger = input("\nWhat triggered this emotion? (optional): ").strip()

        # Get notes
        notes = input("\nAdditional notes? (optional): ").strip()

        # Save entry
        entry = self.tracker.add_entry(emotion, intensity, trigger, notes)

        print("\n" + "=" * 60)
        print("  Entry logged successfully!")
        print("=" * 60)
        print(f"\nEmotion: {emotion}")
        print(f"Intensity: {intensity}/10")
        print(f"Time: {datetime.fromisoformat(entry.timestamp).strftime('%Y-%m-%d %I:%M %p')}")

        # Get immediate solutions if negative emotion
        if intensity >= 6:
            print("\n" + "-" * 60)
            print("  Quick Solutions for Right Now")
            print("-" * 60)
            solutions = self.solutions.get_solutions(emotion, intensity)
            if "immediate" in solutions:
                for i, solution in enumerate(solutions["immediate"][:3], 1):
                    print(f"{i}. {solution}")

        input("\nPress Enter to continue...")

    def view_recent_entries(self):
        """View recent emotion entries"""
        self.print_header("Recent Entries")

        days = self._get_days_input()
        entries = self.tracker.get_entries(days)

        if not entries:
            print("\nNo entries found.")
            input("\nPress Enter to continue...")
            return

        print(f"\nShowing last {len(entries)} entries (past {days} days):\n")

        # Show most recent first
        for entry in reversed(entries[-10:]):
            dt = datetime.fromisoformat(entry.timestamp)
            print("-" * 60)
            print(f"Date/Time: {dt.strftime('%Y-%m-%d %I:%M %p')}")
            print(f"Emotion:   {entry.emotion} (Intensity: {entry.intensity}/10)")
            if entry.trigger:
                print(f"Trigger:   {entry.trigger}")
            if entry.notes:
                print(f"Notes:     {entry.notes}")

        print("-" * 60)
        print(f"\nTotal entries in period: {len(entries)}")
        input("\nPress Enter to continue...")

    def view_statistics(self):
        """View emotion statistics"""
        self.print_header("Emotion Statistics")

        days = self._get_days_input()
        stats = self.tracker.get_emotion_stats(days)

        if stats.get("total_entries", 0) == 0:
            print("\nNo entries found.")
            input("\nPress Enter to continue...")
            return

        print(f"\nPeriod: Last {days} days")
        print(f"Total Entries: {stats['total_entries']}\n")

        print("-" * 60)
        print("Emotion Frequency:")
        print("-" * 60)
        for emotion, count in sorted(stats["emotion_counts"].items(),
                                     key=lambda x: x[1], reverse=True):
            avg_intensity = stats["emotion_avg_intensity"][emotion]
            bar = "█" * int(count)
            print(f"{emotion:15s} {count:3d} entries  (avg: {avg_intensity:.1f}/10)  {bar}")

        print("\n" + "=" * 60)
        print(f"Most Common: {stats['most_common_emotion']}")
        print("=" * 60)

        input("\nPress Enter to continue...")

    def analyze_patterns(self):
        """Analyze emotion patterns"""
        self.print_header("Pattern Analysis")

        print("\nSelect Analysis Type:")
        print("1. Time of Day Patterns")
        print("2. Weekly Cycles")
        print("3. Trigger Patterns")
        print("4. Emotion Streaks")
        print("5. Back to Main Menu")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            self._show_time_patterns()
        elif choice == "2":
            self._show_weekly_cycles()
        elif choice == "3":
            self._show_trigger_patterns()
        elif choice == "4":
            self._show_emotion_streaks()

    def _show_time_patterns(self):
        """Show time of day patterns"""
        self.print_header("Time of Day Patterns")

        days = self._get_days_input()
        patterns = self.analyzer.find_time_patterns(days)

        if "message" in patterns:
            print(f"\n{patterns['message']}")
        else:
            for period, data in patterns.items():
                print(f"\n{period}:")
                for entry in data:
                    print(f"  {entry['hour']:02d}:00 - {entry['emotion']} "
                          f"({entry['count']} times, avg intensity: {entry['avg_intensity']})")

        input("\nPress Enter to continue...")

    def _show_weekly_cycles(self):
        """Show weekly cycle patterns"""
        self.print_header("Weekly Patterns")

        weeks = int(input("\nNumber of weeks to analyze (default 4): ").strip() or "4")
        patterns = self.analyzer.find_weekly_cycles(weeks)

        if "message" in patterns:
            print(f"\n{patterns['message']}")
        else:
            print(f"\nAnalyzing {weeks} weeks of data:\n")
            for day, data in patterns.items():
                print(f"{day:10s}: {data['most_common_emotion']:15s} "
                      f"({data['occurrences']} times, avg: {data['avg_intensity']:.1f}/10)")

        input("\nPress Enter to continue...")

    def _show_trigger_patterns(self):
        """Show trigger patterns"""
        self.print_header("Trigger Patterns")

        days = self._get_days_input()
        patterns = self.analyzer.find_trigger_patterns(days)

        if not patterns:
            print("\nNo trigger patterns found. Try logging triggers with your emotions!")
        else:
            print(f"\nTop triggers for negative emotions (last {days} days):\n")
            for i, pattern in enumerate(patterns[:5], 1):
                print(f"{i}. '{pattern['trigger']}'")
                print(f"   Occurrences: {pattern['occurrences']}")
                print(f"   Primary emotion: {pattern['primary_emotion']}")
                print(f"   Avg intensity: {pattern['avg_intensity']}/10")
                print()

        input("\nPress Enter to continue...")

    def _show_emotion_streaks(self):
        """Show emotion streaks"""
        self.print_header("Emotion Streaks")

        days = self._get_days_input()
        streaks = self.analyzer.detect_emotion_streaks(days)

        if not streaks:
            print("\nNo significant emotion streaks detected (3+ consecutive days).")
        else:
            print(f"\nEmotion streaks (3+ consecutive days) in last {days} days:\n")
            for streak in streaks:
                print(f"{streak['emotion']:15s} - {streak['length']} days")
                print(f"   From {streak['start_date']} to {streak['end_date']}")
                print()

        input("\nPress Enter to continue...")

    def get_solutions(self):
        """Get personalized solutions"""
        self.print_header("Solutions & Recommendations")

        print("\nSelect Option:")
        print("1. Get solutions for a specific emotion")
        print("2. Get personalized recommendations based on patterns")
        print("3. Back to Main Menu")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            self._get_emotion_solutions()
        elif choice == "2":
            self._get_personalized_solutions()

    def _get_emotion_solutions(self):
        """Get solutions for specific emotion"""
        self.print_header("Emotion Solutions")

        # Display emotions
        print("\nSelect Emotion:")
        for i, emotion in enumerate(EmotionEntry.EMOTION_TYPES, 1):
            print(f"{i:2d}. {emotion}")

        try:
            choice = int(input("\nEmotion number: ").strip())
            if 1 <= choice <= len(EmotionEntry.EMOTION_TYPES):
                emotion = EmotionEntry.EMOTION_TYPES[choice - 1]

                intensity = int(input("Current intensity (1-10): ").strip())
                solutions = self.solutions.get_solutions(emotion, intensity)

                print(f"\n{solutions['message']}\n")

                if "immediate" in solutions:
                    print("IMMEDIATE ACTIONS:")
                    for i, sol in enumerate(solutions["immediate"], 1):
                        print(f"  {i}. {sol}")

                if "long_term" in solutions:
                    print("\nLONG-TERM STRATEGIES:")
                    for i, sol in enumerate(solutions["long_term"], 1):
                        print(f"  {i}. {sol}")

                if "activities" in solutions:
                    print("\nRECOMMENDED ACTIVITIES:")
                    for i, sol in enumerate(solutions["activities"], 1):
                        print(f"  {i}. {sol}")

                if "strategies" in solutions:
                    print("\nRECOMMENDED STRATEGIES:")
                    for i, sol in enumerate(solutions["strategies"], 1):
                        print(f"  {i}. {sol}")
        except (ValueError, IndexError):
            print("\nInvalid choice.")

        input("\nPress Enter to continue...")

    def _get_personalized_solutions(self):
        """Get personalized solutions"""
        self.print_header("Personalized Recommendations")

        days = self._get_days_input()
        recommendations = self.solutions.get_personalized_solutions(days)

        print(f"\n{recommendations['message']}\n")

        if "top_emotions_to_address" in recommendations:
            for item in recommendations["top_emotions_to_address"]:
                print(f"\n{'='*60}")
                print(f"Emotion: {item['emotion']}")
                print(f"Frequency: {item['frequency']} times")
                print(f"Average Intensity: {item['avg_intensity']}/10")
                print(f"Focus: {item['focus_area'].upper()}")
                print(f"{'='*60}")

                recs = item["recommendations"]
                if "immediate" in recs:
                    print("\nImmediate Actions:")
                    for i, rec in enumerate(recs["immediate"], 1):
                        print(f"  {i}. {rec}")

                if "long_term" in recs:
                    print("\nLong-term Strategies:")
                    for i, rec in enumerate(recs["long_term"], 1):
                        print(f"  {i}. {rec}")

        input("\nPress Enter to continue...")

    def view_trends(self):
        """View emotion trends"""
        self.print_header("Emotion Trends")

        days = self._get_days_input()
        trends = self.analyzer.get_emotion_trends(days)

        if "message" in trends:
            print(f"\n{trends['message']}")
        else:
            print(f"\nAnalyzing trends over {days} days:\n")

            print(f"Overall Sentiment: {trends['overall_sentiment'].upper()}")
            print(f"\nPositive Emotions Change: {trends['positive_change']:+d}")
            print(f"Negative Emotions Change: {trends['negative_change']:+d}")
            print(f"Intensity Change: {trends['intensity_change']:+.2f}")

            print(f"\n{'='*60}")
            print("First Half vs Second Half:")
            print(f"{'='*60}")

            first = trends["first_period"]
            second = trends["second_period"]

            print(f"\nFirst Period:")
            print(f"  Positive: {first['positive_count']}")
            print(f"  Negative: {first['negative_count']}")
            print(f"  Avg Intensity: {first['avg_intensity']:.2f}")

            print(f"\nSecond Period:")
            print(f"  Positive: {second['positive_count']}")
            print(f"  Negative: {second['negative_count']}")
            print(f"  Avg Intensity: {second['avg_intensity']:.2f}")

        input("\nPress Enter to continue...")

    def show_emergency_resources(self):
        """Show emergency mental health resources"""
        self.print_header("EMERGENCY RESOURCES")

        resources = self.solutions.get_emergency_resources()

        print(f"\n{resources['message']}\n")
        print(f"Crisis Hotline (US): {resources['crisis_hotline']}")
        print(f"Crisis Text Line: {resources['crisis_text']}")
        print(f"International: {resources['international']}")
        print("\nThese services are available 24/7 and are confidential.")

        input("\nPress Enter to continue...")

    def _get_days_input(self, default: int = 30) -> int:
        """Get number of days from user input"""
        try:
            days = input(f"\nNumber of days to analyze (default {default}): ").strip()
            return int(days) if days else default
        except ValueError:
            return default

    def run(self):
        """Run the main application loop"""
        print("\n" + "=" * 60)
        print("  Welcome to Emotion Journal")
        print("  Track, Analyze, and Improve Your Emotional Well-being")
        print("=" * 60)

        while self.running:
            try:
                self.print_menu()
                choice = input("\nChoice: ").strip()

                if choice == "1":
                    self.log_emotion()
                elif choice == "2":
                    self.view_recent_entries()
                elif choice == "3":
                    self.view_statistics()
                elif choice == "4":
                    self.analyze_patterns()
                elif choice == "5":
                    self.get_solutions()
                elif choice == "6":
                    self.view_trends()
                elif choice == "7":
                    self.show_emergency_resources()
                elif choice == "8":
                    print("\nThank you for using Emotion Journal!")
                    print("Take care of yourself!\n")
                    self.running = False
                else:
                    print("\nInvalid choice. Please select 1-8.")
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nExiting... Take care!")
                self.running = False
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    app = EmotionJournalCLI()
    app.run()


if __name__ == "__main__":
    main()
