"""
Solution Engine Module
Provides personalized solutions and coping strategies for different emotions
"""

from typing import List, Dict
from emotion_tracker import EmotionTracker


class SolutionEngine:
    """Recommends solutions for managing emotions"""

    # Solutions database organized by emotion type
    SOLUTIONS = {
        "Sad": {
            "immediate": [
                "Take a short walk outside to get fresh air and natural light",
                "Call or message a friend or family member",
                "Listen to uplifting music or a favorite playlist",
                "Practice gratitude by listing 3 things you're thankful for",
                "Watch a comforting movie or TV show"
            ],
            "long_term": [
                "Consider speaking with a therapist or counselor",
                "Establish a regular exercise routine",
                "Join a social group or club aligned with your interests",
                "Keep a gratitude journal",
                "Practice mindfulness meditation daily"
            ],
            "activities": [
                "Creative expression (drawing, painting, writing)",
                "Cook or bake something you enjoy",
                "Organize or declutter a small space",
                "Take a relaxing bath or shower",
                "Read an engaging book"
            ]
        },
        "Anxious": {
            "immediate": [
                "Practice deep breathing: 4 counts in, hold 4, 4 counts out",
                "Use the 5-4-3-2-1 grounding technique (5 things you see, 4 you touch, etc.)",
                "Progressive muscle relaxation from head to toe",
                "Step outside for fresh air",
                "Splash cold water on your face"
            ],
            "long_term": [
                "Develop a regular meditation practice",
                "Limit caffeine and alcohol intake",
                "Maintain a consistent sleep schedule",
                "Consider cognitive behavioral therapy (CBT)",
                "Regular exercise, especially cardio"
            ],
            "activities": [
                "Yoga or gentle stretching",
                "Journal your worries and fears",
                "Listen to calming music or nature sounds",
                "Practice guided meditation",
                "Engage in a repetitive, calming activity (knitting, coloring)"
            ]
        },
        "Angry": {
            "immediate": [
                "Take 10 deep breaths before responding",
                "Remove yourself from the triggering situation",
                "Do physical exercise (run, punch a pillow, do push-ups)",
                "Write down your feelings without filtering",
                "Count backwards from 100 by 7s"
            ],
            "long_term": [
                "Learn and practice assertive communication",
                "Identify anger triggers and patterns",
                "Consider anger management therapy",
                "Develop a regular exercise routine",
                "Practice forgiveness and letting go"
            ],
            "activities": [
                "High-intensity workout or sports",
                "Punch a punching bag or do kickboxing",
                "Clean or organize aggressively",
                "Creative destruction (tear paper, break sticks)",
                "Scream into a pillow in private"
            ]
        },
        "Stressed": {
            "immediate": [
                "Make a prioritized to-do list",
                "Take a 5-minute break to breathe deeply",
                "Do a quick physical activity (jumping jacks, walk)",
                "Drink water and have a healthy snack",
                "Say 'no' to one non-essential commitment"
            ],
            "long_term": [
                "Learn time management and organization skills",
                "Set healthy boundaries in work and relationships",
                "Regular exercise and adequate sleep",
                "Practice saying 'no' to overcommitment",
                "Develop a daily relaxation routine"
            ],
            "activities": [
                "Yoga or tai chi",
                "Listen to calming music",
                "Take a warm bath",
                "Practice progressive muscle relaxation",
                "Spend time in nature"
            ]
        },
        "Lonely": {
            "immediate": [
                "Call or video chat with someone you care about",
                "Join an online community related to your interests",
                "Go to a public place (cafe, library, park)",
                "Reach out to an old friend",
                "Pet therapy - visit animals or volunteer at a shelter"
            ],
            "long_term": [
                "Join clubs, classes, or groups that interest you",
                "Volunteer for causes you care about",
                "Develop deeper existing relationships",
                "Consider therapy to address underlying issues",
                "Build a regular social routine"
            ],
            "activities": [
                "Attend local community events",
                "Take a class (cooking, art, dance)",
                "Join a gym or fitness class",
                "Participate in online forums or gaming communities",
                "Start a hobby that involves others"
            ]
        },
        "Overwhelmed": {
            "immediate": [
                "Stop and take 5 deep breaths",
                "Write down everything on your mind",
                "Pick just ONE thing to focus on right now",
                "Ask for help with specific tasks",
                "Take a short break - even 5 minutes helps"
            ],
            "long_term": [
                "Learn to delegate and ask for help",
                "Practice time blocking and task batching",
                "Simplify your life - remove unnecessary commitments",
                "Regular self-care and rest days",
                "Therapy to develop coping strategies"
            ],
            "activities": [
                "Brain dump everything into a journal",
                "Create a priority matrix (urgent/important)",
                "Take a nature walk",
                "Practice mindfulness meditation",
                "Gentle yoga or stretching"
            ]
        },
        "Fearful": {
            "immediate": [
                "Ground yourself with the 5-4-3-2-1 technique",
                "Remind yourself you are safe right now",
                "Call someone you trust",
                "Focus on your breathing",
                "Identify if the fear is rational or anxiety-based"
            ],
            "long_term": [
                "Gradually expose yourself to fears in safe ways",
                "Consider therapy, especially for phobias",
                "Learn about your specific fears",
                "Build confidence through small challenges",
                "Practice relaxation techniques regularly"
            ],
            "activities": [
                "Write about your fears",
                "Learn facts about what scares you",
                "Practice visualization of positive outcomes",
                "Meditation and mindfulness",
                "Talk to others who've overcome similar fears"
            ]
        },
        "Frustrated": {
            "immediate": [
                "Step away from the frustrating situation",
                "Do something physical to release energy",
                "Take a break and return with fresh perspective",
                "Talk to someone about what's frustrating you",
                "Reframe the situation - what can you learn?"
            ],
            "long_term": [
                "Develop problem-solving skills",
                "Practice patience through meditation",
                "Set realistic expectations",
                "Learn to accept what you can't control",
                "Build resilience through small challenges"
            ],
            "activities": [
                "Physical exercise",
                "Puzzle or problem-solving games",
                "Creative outlet (art, music, writing)",
                "Clean or organize",
                "Learn a new skill (shifts perspective)"
            ]
        }
    }

    # Positive emotions get reinforcement strategies
    POSITIVE_REINFORCEMENT = {
        "Happy": [
            "Capture this moment - write about why you're happy",
            "Share your happiness with others",
            "Do something kind for someone else",
            "Take a photo or create a memory",
            "Note what led to this happiness for future reference"
        ],
        "Grateful": [
            "Write a thank you note to someone",
            "Keep a gratitude journal",
            "Share your gratitude with the person involved",
            "Perform an act of kindness",
            "Reflect on what you're grateful for"
        ],
        "Excited": [
            "Channel your energy into the exciting activity",
            "Share your excitement with others",
            "Make plans to sustain this feeling",
            "Document this moment",
            "Stay present and enjoy the feeling"
        ],
        "Calm": [
            "Note what helped you achieve this calmness",
            "Enjoy and savor this peaceful moment",
            "Practice extending this feeling",
            "Create a routine that promotes calm",
            "Use this time for reflection or meditation"
        ],
        "Content": [
            "Appreciate this moment of contentment",
            "Reflect on what contributed to this feeling",
            "Share time with loved ones",
            "Journal about your current state",
            "Use this as baseline for future comparison"
        ],
        "Hopeful": [
            "Write down what you're hopeful about",
            "Make concrete plans toward your hopes",
            "Share your hopes with supportive people",
            "Take one small action toward your goal",
            "Visualize your hoped-for outcome"
        ]
    }

    def __init__(self, tracker: EmotionTracker):
        """
        Initialize solution engine

        Args:
            tracker: EmotionTracker instance
        """
        self.tracker = tracker

    def get_solutions(self, emotion: str, intensity: int = 5) -> Dict[str, List[str]]:
        """
        Get solutions for a specific emotion

        Args:
            emotion: Type of emotion
            intensity: Intensity level (1-10)

        Returns:
            Dictionary with categorized solutions
        """
        # Check for positive emotions
        if emotion in self.POSITIVE_REINFORCEMENT:
            return {
                "type": "positive_reinforcement",
                "message": f"Great that you're feeling {emotion.lower()}! Here are ways to sustain and amplify this feeling:",
                "strategies": self.POSITIVE_REINFORCEMENT[emotion]
            }

        # Get solutions for negative emotions
        if emotion not in self.SOLUTIONS:
            return {
                "type": "general",
                "message": f"No specific solutions for {emotion}, but here are general wellness tips:",
                "strategies": self._get_general_solutions()
            }

        solutions = self.SOLUTIONS[emotion]

        # For high intensity, prioritize immediate actions
        if intensity >= 7:
            return {
                "type": "immediate_focus",
                "message": f"Your {emotion.lower()} is quite intense. Focus on these immediate actions:",
                "immediate": solutions["immediate"],
                "activities": solutions["activities"][:3]
            }
        else:
            return {
                "type": "balanced",
                "message": f"Here are strategies to help with feeling {emotion.lower()}:",
                "immediate": solutions["immediate"][:3],
                "long_term": solutions["long_term"][:3],
                "activities": solutions["activities"][:3]
            }

    def get_personalized_solutions(self, days: int = 7) -> Dict:
        """
        Get personalized solutions based on recent patterns

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with personalized recommendations
        """
        entries = self.tracker.get_entries(days)

        if not entries:
            return {
                "message": "Start logging emotions to get personalized solutions!",
                "solutions": []
            }

        # Find most common negative emotions
        negative_emotions = {}
        for entry in entries:
            if entry.emotion in self.SOLUTIONS:
                if entry.emotion not in negative_emotions:
                    negative_emotions[entry.emotion] = {
                        "count": 0,
                        "total_intensity": 0
                    }
                negative_emotions[entry.emotion]["count"] += 1
                negative_emotions[entry.emotion]["total_intensity"] += entry.intensity

        if not negative_emotions:
            return {
                "message": "You've been experiencing mostly positive emotions!",
                "recommendation": "Keep doing what you're doing, and consider journaling about what's working well.",
                "solutions": []
            }

        # Sort by frequency
        sorted_emotions = sorted(
            negative_emotions.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )

        # Get solutions for top 3 emotions
        personalized = []
        for emotion, data in sorted_emotions[:3]:
            avg_intensity = data["total_intensity"] / data["count"]
            solutions = self.get_solutions(emotion, int(avg_intensity))

            personalized.append({
                "emotion": emotion,
                "frequency": data["count"],
                "avg_intensity": round(avg_intensity, 2),
                "focus_area": "immediate" if avg_intensity >= 7 else "long_term",
                "recommendations": solutions
            })

        return {
            "message": f"Based on the last {days} days, here are personalized solutions:",
            "top_emotions_to_address": personalized
        }

    def _get_general_solutions(self) -> List[str]:
        """Get general wellness solutions"""
        return [
            "Practice daily meditation or mindfulness",
            "Maintain regular sleep schedule (7-9 hours)",
            "Exercise regularly (30 minutes, 5 days/week)",
            "Eat a balanced, nutritious diet",
            "Stay hydrated throughout the day",
            "Limit screen time before bed",
            "Spend time in nature regularly",
            "Maintain social connections",
            "Pursue hobbies and interests",
            "Consider professional help if needed"
        ]

    def get_emergency_resources(self) -> Dict[str, str]:
        """Get emergency mental health resources"""
        return {
            "crisis_hotline": "988 (Suicide & Crisis Lifeline - US)",
            "crisis_text": "Text 'HELLO' to 741741 (Crisis Text Line)",
            "international": "https://findahelpline.com",
            "message": "If you're in crisis, please reach out to these resources. You're not alone."
        }
