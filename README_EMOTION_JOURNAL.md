# Emotion Journal

A comprehensive Python application for tracking daily emotions, identifying patterns and cycles, and receiving personalized solutions to improve emotional well-being.

## Features

### 1. Emotion Tracking
- Log emotions with intensity levels (1-10)
- Record triggers and additional notes
- Support for 16 different emotion types
- Automatic timestamping
- Persistent JSON storage

### 2. Pattern Analysis
- **Time of Day Patterns**: Discover when you experience certain emotions
- **Weekly Cycles**: Identify patterns across different days of the week
- **Trigger Analysis**: Find common triggers for negative emotions
- **Emotion Streaks**: Detect consecutive days with similar emotions
- **Trend Analysis**: Track if emotions are improving or declining over time

### 3. Personalized Solutions
- Immediate action steps for current emotions
- Long-term strategies for emotional well-being
- Activity recommendations
- Personalized recommendations based on your patterns
- Emergency mental health resources

### 4. Statistics & Insights
- Emotion frequency tracking
- Average intensity calculations
- Most common emotions
- Positive vs negative emotion trends

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup

1. Clone or download the repository

2. Navigate to the project directory:
```bash
cd emotion-journal
```

3. Run the application:
```bash
python3 emotion_journal.py
```

Or make it executable:
```bash
chmod +x emotion_journal.py
./emotion_journal.py
```

## Usage

### Main Menu Options

1. **Log New Emotion** - Record how you're feeling right now
2. **View Recent Entries** - See your emotion history
3. **View Statistics** - Get insights about your emotional patterns
4. **Analyze Patterns** - Deep dive into patterns and cycles
5. **Get Solutions & Recommendations** - Receive personalized help
6. **View Emotion Trends** - Track improvement over time
7. **Emergency Resources** - Access crisis support information
8. **Exit** - Close the application

### Quick Start Guide

#### Logging Your First Emotion

```
1. Select "1" from the main menu
2. Choose your emotion from the list
3. Rate intensity (1-10)
4. Optionally add trigger and notes
5. Receive immediate solutions if needed
```

#### Analyzing Patterns

```
1. Log emotions for at least a week
2. Select "4. Analyze Patterns"
3. Choose analysis type:
   - Time of day patterns
   - Weekly cycles
   - Trigger patterns
   - Emotion streaks
```

#### Getting Personalized Solutions

```
1. Select "5. Get Solutions & Recommendations"
2. Choose personalized recommendations
3. Review solutions for your most common emotions
```

## Supported Emotions

- **Positive**: Happy, Excited, Calm, Grateful, Hopeful, Content
- **Negative**: Sad, Anxious, Angry, Fearful, Frustrated, Lonely, Stressed, Overwhelmed
- **Neutral**: Surprised, Disgusted

## Data Storage

All emotion entries are stored in `data/emotions.json`. This file is automatically created on first use and contains all your journaled emotions in JSON format.

### Data Structure

```json
[
  {
    "emotion": "Happy",
    "intensity": 8,
    "trigger": "Got promoted at work",
    "notes": "Feeling great today!",
    "timestamp": "2025-10-21T14:30:00.000000"
  }
]
```

## Solution Categories

### Immediate Actions
Quick steps you can take right now to address intense emotions

### Long-term Strategies
Sustainable practices for lasting emotional well-being

### Recommended Activities
Specific activities tailored to different emotional states

### Positive Reinforcement
Strategies to amplify and sustain positive emotions

## Examples

### Example 1: Daily Tracking

Log emotions daily to build a comprehensive picture:
- Morning: Rate your mood after waking up
- Afternoon: Log emotions after work/school
- Evening: Reflect on the day before bed

### Example 2: Trigger Awareness

When logging emotions, always add triggers:
- "Deadline stress"
- "Argument with friend"
- "Exercise session"
- "Good news from family"

This helps identify patterns and develop coping strategies.

### Example 3: Weekly Review

Every Sunday:
1. View statistics for the past 7 days
2. Analyze patterns
3. Review personalized solutions
4. Set intentions for the coming week

## Privacy & Security

- All data is stored locally on your device
- No data is sent to external servers
- No account or login required
- You have full control over your data

## Tips for Best Results

1. **Be Consistent**: Log emotions at least once daily
2. **Be Honest**: Accurate tracking leads to better insights
3. **Add Context**: Include triggers and notes
4. **Review Regularly**: Check patterns weekly
5. **Take Action**: Try the recommended solutions
6. **Be Patient**: Patterns emerge over time (2-4 weeks)

## Crisis Support

If you're experiencing a mental health crisis, the app provides quick access to:
- 988 Suicide & Crisis Lifeline (US)
- Crisis Text Line (Text HELLO to 741741)
- International helplines

**Remember**: This app is a tool for self-reflection and wellness, not a substitute for professional mental health care.

## File Structure

```
emotion-journal/
├── emotion_journal.py      # Main CLI application
├── emotion_tracker.py      # Data models and storage
├── pattern_analyzer.py     # Pattern detection algorithms
├── solution_engine.py      # Solution recommendation system
├── data/
│   └── emotions.json       # Your emotion data (auto-created)
└── README_EMOTION_JOURNAL.md  # This file
```

## Advanced Features

### Pattern Detection Algorithms

- **Time-based clustering**: Groups emotions by hour/day
- **Frequency analysis**: Identifies most common emotions
- **Intensity tracking**: Monitors emotion strength over time
- **Streak detection**: Finds consecutive day patterns
- **Trend analysis**: Compares periods to show improvement

### Solution Engine

- Over 100 curated coping strategies
- Context-aware recommendations
- Intensity-based prioritization
- Personalized based on your patterns

## Contributing

This is an open-source project. Contributions, suggestions, and feedback are welcome!

## License

This project is provided as-is for personal use and wellness tracking.

## Disclaimer

This application is designed to support emotional well-being and self-reflection. It is not a replacement for professional mental health services. If you are experiencing severe emotional distress, please consult a mental health professional.

---

**Take care of your mental health. You deserve to feel good.**
