#!/usr/bin/env python3
"""
Test script for Emotion Journal
Tests core functionality without user interaction
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from emotion_tracker import EmotionTracker, EmotionEntry
from pattern_analyzer import PatternAnalyzer
from solution_engine import SolutionEngine

def cleanup_test_data():
    """Remove test data directory"""
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")

def test_emotion_tracker():
    """Test emotion tracking functionality"""
    print("Testing Emotion Tracker...")

    tracker = EmotionTracker("test_data/emotions.json")

    # Add some test entries
    tracker.add_entry("Happy", 8, "Got good news", "Feeling great!")
    tracker.add_entry("Anxious", 6, "Work deadline", "Need to finish project")
    tracker.add_entry("Calm", 7, "Meditation", "Morning meditation session")

    # Check entries were saved
    assert len(tracker.entries) == 3, "Should have 3 entries"

    # Test statistics
    stats = tracker.get_emotion_stats()
    assert stats["total_entries"] == 3, "Stats should show 3 entries"
    assert "Happy" in stats["emotion_counts"], "Should track Happy emotion"

    print("  ✓ Emotion tracking works correctly")
    return tracker

def test_pattern_analyzer(tracker):
    """Test pattern analysis"""
    print("\nTesting Pattern Analyzer...")

    # Add more entries with different times and days
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        entry = EmotionEntry("Stressed", 7, "Work", "", date.isoformat())
        tracker.entries.append(entry)

    tracker.save_entries()

    analyzer = PatternAnalyzer(tracker)

    # Test time patterns
    time_patterns = analyzer.find_time_patterns(30)
    assert isinstance(time_patterns, dict), "Should return patterns dict"

    # Test weekly cycles
    weekly = analyzer.find_weekly_cycles(4)
    assert isinstance(weekly, dict), "Should return weekly patterns"

    # Test trigger patterns
    triggers = analyzer.find_trigger_patterns(30)
    assert isinstance(triggers, list), "Should return trigger list"
    assert len(triggers) > 0, "Should find triggers"

    # Test emotion trends
    trends = analyzer.get_emotion_trends(30)
    assert isinstance(trends, dict), "Should return trends"

    print("  ✓ Pattern analysis works correctly")
    return analyzer

def test_solution_engine(tracker):
    """Test solution recommendations"""
    print("\nTesting Solution Engine...")

    engine = SolutionEngine(tracker)

    # Test solutions for negative emotion
    solutions = engine.get_solutions("Anxious", 8)
    assert "message" in solutions, "Should have message"
    assert "immediate" in solutions or "strategies" in solutions, "Should have solutions"

    # Test solutions for positive emotion
    positive_solutions = engine.get_solutions("Happy", 7)
    assert "strategies" in positive_solutions or "message" in positive_solutions, "Should have positive reinforcement"

    # Test personalized solutions
    personalized = engine.get_personalized_solutions(7)
    assert "message" in personalized, "Should have personalized message"

    # Test emergency resources
    resources = engine.get_emergency_resources()
    assert "crisis_hotline" in resources, "Should have crisis resources"

    print("  ✓ Solution engine works correctly")
    return engine

def test_data_persistence():
    """Test that data persists across sessions"""
    print("\nTesting Data Persistence...")

    # Create tracker and add entry
    tracker1 = EmotionTracker("test_data/persistence.json")
    tracker1.add_entry("Grateful", 9, "Test", "Testing persistence")

    # Create new tracker instance and load
    tracker2 = EmotionTracker("test_data/persistence.json")
    assert len(tracker2.entries) == 1, "Should load saved entry"
    assert tracker2.entries[0].emotion == "Grateful", "Should preserve emotion"

    print("  ✓ Data persistence works correctly")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("  Emotion Journal - Test Suite")
    print("=" * 60)

    try:
        # Clean up any existing test data
        cleanup_test_data()

        # Run tests
        tracker = test_emotion_tracker()
        analyzer = test_pattern_analyzer(tracker)
        engine = test_solution_engine(tracker)
        test_data_persistence()

        print("\n" + "=" * 60)
        print("  ✓ All tests passed successfully!")
        print("=" * 60)

        # Show some test statistics
        print("\nTest Statistics:")
        print(f"  Total entries created: {len(tracker.entries)}")
        print(f"  Emotions tracked: {len(tracker.get_emotion_stats()['emotion_counts'])}")

        return True

    except AssertionError as e:
        print(f"\n  ✗ Test failed: {e}")
        return False

    except Exception as e:
        print(f"\n  ✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up test data
        cleanup_test_data()
        print("\n  Test data cleaned up")

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
