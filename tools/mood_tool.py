"""
Mood Tracker Tool - Mood Logging and Pattern Analysis
Helps users track moods, identify patterns, and monitor mental health over time
"""

from langchain.tools import BaseTool
from typing import Optional, Type, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
import json


class MoodInput(BaseModel):
    """Input schema for mood tracking."""
    action: str = Field(
        description="Action: 'log' (record mood) or 'analyze' (get insights)"
    )
    mood: Optional[str] = Field(
        default=None,
        description="Mood rating: 'great', 'good', 'okay', 'low', 'terrible'"
    )
    emotions: Optional[str] = Field(
        default=None,
        description="Specific emotions (comma-separated): anxious, sad, happy, angry, etc."
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional notes about mood"
    )


class MoodTrackerTool(BaseTool):
    """Tool for mood tracking and pattern analysis."""
    
    name: str = "mood_tracker"
    description: str = """
    Track moods and analyze patterns over time for mental health monitoring.
    
    Use this tool when:
    - User wants to log their current mood
    - Checking in on emotional state
    - Analyzing mood patterns and trends
    - Monitoring mental health progress
    
    Input: action (log/analyze), mood level, emotions, and optional notes
    Output: Confirmation for logging, insights for analysis
    """
    args_schema: Type[BaseModel] = MoodInput
    
    # In-memory mood storage (in production, would use database)
    mood_logs: List[Dict] = []
    
    def _run(
        self,
        action: str,
        mood: Optional[str] = None,
        emotions: Optional[str] = None,
        notes: Optional[str] = None
    ) -> str:
        """Track or analyze moods."""
        
        if action.lower() == "log":
            return self._log_mood(mood, emotions, notes)
        elif action.lower() == "analyze":
            return self._analyze_moods()
        else:
            return self._mood_check_in(mood)
    
    async def _arun(
        self,
        action: str,
        mood: Optional[str] = None,
        emotions: Optional[str] = None,
        notes: Optional[str] = None
    ) -> str:
        """Async version."""
        return self._run(action, mood, emotions, notes)
    
    def _log_mood(
        self,
        mood: Optional[str],
        emotions: Optional[str],
        notes: Optional[str]
    ) -> str:
        """Log a mood entry."""
        
        if not mood:
            return self._get_mood_logging_guide()
        
        # Create mood entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood.lower(),
            "emotions": [e.strip() for e in emotions.split(',')] if emotions else [],
            "notes": notes or "",
            "mood_score": self._mood_to_score(mood)
        }
        
        # Store entry (in production, save to database)
        self.mood_logs.append(entry)
        
        # Generate response
        emoji = self._mood_emoji(mood)
        
        result = f"""
{emoji} MOOD LOGGED {emoji}

**Date/Time:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Mood Level:** {mood.title()}
**Mood Score:** {entry['mood_score']}/10
"""
        
        if emotions:
            result += f"**Emotions:** {', '.join(entry['emotions'])}\n"
        
        if notes:
            result += f"**Notes:** {notes}\n"
        
        result += """
**TRACKING INSIGHTS:**
- Regular mood tracking helps identify patterns
- Notice what affects your mood (sleep, activities, people)
- Celebrate positive moods, learn from difficult ones
- Share patterns with therapist if in treatment

**WHAT'S NEXT:**
- Continue daily mood logging
- Use 'analyze' to see patterns
- Notice triggers and helpful activities
- Adjust self-care based on insights

Great job taking time to check in with yourself! 💙

**TIPS FOR BETTER TRACKING:**
- Log at same time daily (morning and evening ideal)
- Be honest with yourself
- Note what you were doing before logging
- Track sleep and activities too
"""
        
        return result
    
    def _analyze_moods(self) -> str:
        """Analyze mood patterns."""
        
        if not self.mood_logs:
            return """
📊 MOOD ANALYSIS

No mood entries logged yet. Start tracking your moods to see patterns!

**HOW TO START:**
1. Log your mood daily (morning and evening)
2. Note what you're feeling
3. Add brief notes about your day
4. After a week, check back for insights

**BENEFITS OF MOOD TRACKING:**
- Identify triggers and patterns
- Notice what helps vs. hurts mood
- Track treatment effectiveness
- Share data with healthcare providers
- Gain self-awareness

Start today - even one entry helps!
"""
        
        # Calculate statistics
        total_entries = len(self.mood_logs)
        avg_score = sum(e['mood_score'] for e in self.mood_logs) / total_entries
        
        # Count mood frequencies
        mood_counts = {}
        for entry in self.mood_logs:
            mood = entry['mood']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        # Find most common emotions
        all_emotions = []
        for entry in self.mood_logs:
            all_emotions.extend(entry['emotions'])
        
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get top emotions
        top_emotions = sorted(
            emotion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Generate insights
        result = f"""
📊 MOOD PATTERN ANALYSIS

**TRACKING SUMMARY:**
- Total Entries: {total_entries}
- Average Mood Score: {avg_score:.1f}/10
- Tracking Period: {self._get_tracking_period()}

**MOOD DISTRIBUTION:**
"""
        
        for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_entries) * 100
            emoji = self._mood_emoji(mood)
            result += f"{emoji} {mood.title()}: {count} times ({percentage:.0f}%)\n"
        
        if top_emotions:
            result += "\n**COMMON EMOTIONS:**\n"
            for emotion, count in top_emotions:
                result += f"- {emotion.title()}: {count} times\n"
        
        # Provide insights
        result += "\n**INSIGHTS:**\n"
        
        if avg_score >= 7:
            result += "✅ Overall mood is positive! Keep up healthy habits.\n"
        elif avg_score >= 5:
            result += "⚖️ Mood is moderate. Identify what helps boost it.\n"
        else:
            result += "⚠️ Mood is lower than optimal. Consider professional support.\n"
        
        result += """
**RECOMMENDATIONS:**
1. Continue daily tracking for better patterns
2. Note activities before good/bad moods
3. Identify mood triggers and helpers
4. Share this data with your therapist
5. Adjust self-care based on patterns

**WHAT TO TRACK NEXT:**
- Sleep hours (affects mood significantly)
- Exercise and movement
- Social interactions
- Stressful events
- Self-care activities

Keep tracking - patterns become clearer over time! 📈
"""
        
        return result
    
    def _mood_check_in(self, mood: Optional[str]) -> str:
        """Quick mood check-in."""
        
        if not mood:
            return """
💭 MOOD CHECK-IN

How are you feeling right now?

**Choose a mood level:**
- 😊 Great - Feeling wonderful, energetic, positive
- 🙂 Good - Feeling pleasant, content, stable
- 😐 Okay - Neutral, neither good nor bad
- 😔 Low - Feeling down, sad, unmotivated
- 😞 Terrible - Very difficult, distressed, struggling

**Or rate on scale 1-10:**
1-2: Terrible, 3-4: Low, 5-6: Okay, 7-8: Good, 9-10: Great

Share your mood to log it and get personalized support!
"""
        
        emoji = self._mood_emoji(mood)
        score = self._mood_to_score(mood)
        
        response = f"""
{emoji} Thank you for checking in!

**Current Mood:** {mood.title()} ({score}/10)
"""
        
        if score >= 8:
            response += """
**That's wonderful!** 🎉
- What's contributing to this positive mood?
- How can you sustain these good feelings?
- Consider what helped you get here

**CELEBRATE:**
Take a moment to appreciate feeling good. You deserve this!
"""
        elif score >= 6:
            response += """
**You're doing okay!** 👍
- This is a stable, manageable place
- What small thing could boost your mood today?
- Keep up your self-care routines

**SUGGESTION:**
Do one thing you enjoy today, even if small.
"""
        elif score >= 4:
            response += """
**Things feel tough right now.** 💙
- It's okay to not be okay
- What support do you need?
- Have you tried any coping strategies?

**HELPFUL ACTIONS:**
- Reach out to someone you trust
- Try a quick breathing exercise
- Do a small self-care activity
- Consider professional support if this continues
"""
        else:
            response += """
**You're really struggling.** 🆘
I'm concerned and want to help.

**IMMEDIATE SUPPORT:**
📞 Samaritans of Singapore: 1-767 (24/7)
📞 IMH Helpline: 6389-2222 (24/7)

**PLEASE:**
- Don't isolate yourself
- Reach out to someone today
- Consider crisis hotline support
- See a professional if thoughts worsen

You don't have to face this alone. Help is available.
"""
        
        response += """
**NEXT STEPS:**
- Would you like to log this mood for tracking?
- Need coping strategies or resources?
- Want to talk about what's affecting your mood?
"""
        
        return response
    
    def _mood_to_score(self, mood: str) -> int:
        """Convert mood to numerical score."""
        mood_scores = {
            "terrible": 2,
            "very bad": 3,
            "bad": 4,
            "low": 4,
            "poor": 4,
            "down": 5,
            "okay": 6,
            "fine": 6,
            "alright": 6,
            "good": 7,
            "well": 7,
            "great": 9,
            "excellent": 10,
            "amazing": 10
        }
        return mood_scores.get(mood.lower(), 5)
    
    def _mood_emoji(self, mood: str) -> str:
        """Get emoji for mood."""
        score = self._mood_to_score(mood)
        if score >= 8:
            return "😊"
        elif score >= 6:
            return "🙂"
        elif score >= 4:
            return "😐"
        elif score >= 2:
            return "😔"
        else:
            return "😞"
    
    def _get_tracking_period(self) -> str:
        """Get tracking time period."""
        if not self.mood_logs:
            return "No data"
        
        first = datetime.fromisoformat(self.mood_logs[0]['timestamp'])
        last = datetime.fromisoformat(self.mood_logs[-1]['timestamp'])
        days = (last - first).days + 1
        
        return f"{days} day{'s' if days != 1 else ''}"
    
    def _get_mood_logging_guide(self) -> str:
        """Get mood logging instructions."""
        
        return """
📝 HOW TO LOG YOUR MOOD

**MOOD LEVELS:**
- 😊 **Great** (9-10): Excellent mood, very positive
- 🙂 **Good** (7-8): Pleasant, content, stable
- 😐 **Okay** (5-6): Neutral, manageable
- 😔 **Low** (3-4): Down, sad, struggling
- 😞 **Terrible** (1-2): Very distressed, crisis

**WHAT TO INCLUDE:**
1. **Mood Level** (required): great, good, okay, low, terrible
2. **Specific Emotions** (optional): anxious, happy, sad, angry, calm, etc.
3. **Notes** (optional): What's affecting your mood, what you're doing

**EXAMPLE:**
"Log my mood as okay, feeling anxious and tired, had a stressful day at work"

**TRACKING TIPS:**
- Be honest with yourself
- Log at consistent times (morning/evening)
- Include context (sleep, events, activities)
- Notice patterns over time

Ready to log? Share your current mood!
"""


def create_mood_tracker_tool() -> MoodTrackerTool:
    """Create an instance of the MoodTrackerTool."""
    return MoodTrackerTool()
