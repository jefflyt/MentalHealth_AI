"""
Breathing Exercise Tool - Guided Breathing and Relaxation
Provides timed breathing exercises for anxiety and stress relief
"""

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import time


class BreathingInput(BaseModel):
    """Input schema for breathing exercise."""
    exercise_type: str = Field(
        description="Type of breathing: 'box', '478', 'deep', 'calming', 'quick'"
    )
    duration: Optional[int] = Field(
        default=3,
        description="Number of breathing cycles (1-10)"
    )


class BreathingExerciseTool(BaseTool):
    """Tool for guided breathing exercises."""
    
    name: str = "breathing_exercise"
    description: str = """
    Guide users through breathing exercises for stress and anxiety relief.
    
    Use this tool when:
    - User feels anxious or stressed
    - Panic attack or heightened anxiety
    - Need grounding or calming technique
    - Physical symptoms of stress
    
    Input: exercise_type and optional duration
    Output: Step-by-step breathing instructions
    """
    args_schema: Type[BaseModel] = BreathingInput
    
    def _run(
        self,
        exercise_type: str,
        duration: Optional[int] = 3
    ) -> str:
        """Provide breathing exercise instructions."""
        
        # Limit duration to reasonable range
        cycles = max(1, min(duration or 3, 10))
        
        if exercise_type.lower() == "box":
            return self._box_breathing(cycles)
        elif exercise_type.lower() == "478" or exercise_type.lower() == "4-7-8":
            return self._breathing_478(cycles)
        elif exercise_type.lower() == "deep":
            return self._deep_breathing(cycles)
        elif exercise_type.lower() == "calming":
            return self._calming_breath(cycles)
        else:
            return self._quick_calm(cycles)
    
    async def _arun(
        self,
        exercise_type: str,
        duration: Optional[int] = 3
    ) -> str:
        """Async version."""
        return self._run(exercise_type, duration)
    
    def _box_breathing(self, cycles: int) -> str:
        """Box breathing (4-4-4-4) instructions."""
        
        return f"""
📦 BOX BREATHING EXERCISE

This technique is used by Navy SEALs for stress management.

**HOW TO DO IT:**
1. Sit comfortably with your back straight
2. Place one hand on your belly
3. Follow this pattern for {cycles} cycles:

**THE PATTERN:**
🌬️ BREATHE IN (nose) - Count to 4
⏸️ HOLD - Count to 4
💨 BREATHE OUT (mouth) - Count to 4
⏸️ HOLD - Count to 4

**FULL CYCLE:**
→ Breathe in: 1, 2, 3, 4
→ Hold: 1, 2, 3, 4
→ Breathe out: 1, 2, 3, 4
→ Hold: 1, 2, 3, 4

**Repeat {cycles} times**

**TIPS:**
- Focus on the counting
- Make breath smooth and controlled
- If dizzy, breathe normally
- Notice your belly rising and falling

**BENEFITS:**
- Reduces anxiety and stress
- Improves focus and concentration
- Activates relaxation response
- Brings you into the present moment

Take your time. This is YOUR moment of calm.
"""
    
    def _breathing_478(self, cycles: int) -> str:
        """4-7-8 breathing technique instructions."""
        
        return f"""
🌙 4-7-8 BREATHING TECHNIQUE

Developed by Dr. Andrew Weil, this is called "relaxing breath."

**PREPARATION:**
1. Sit with back straight
2. Touch tip of tongue to ridge behind upper front teeth
3. Keep it there throughout exercise
4. Exhale completely through mouth (whoosh sound)

**THE PATTERN:** (Repeat {cycles} times)
🌬️ BREATHE IN (nose quietly) - Count to 4
⏸️ HOLD breath - Count to 7
💨 BREATHE OUT (mouth with whoosh) - Count to 8

**FULL CYCLE:**
1. Close mouth, inhale through nose: 1, 2, 3, 4
2. Hold breath: 1, 2, 3, 4, 5, 6, 7
3. Exhale through mouth (whoosh): 1, 2, 3, 4, 5, 6, 7, 8

**Repeat {cycles} cycles**

**KEY POINTS:**
- Ratio is important (4:7:8), not speed
- Keep tip of tongue in position
- Exhalation should be audible
- Practice twice daily

**WHEN TO USE:**
- Before sleep (natural tranquilizer)
- When feeling anxious
- Before stressful situations
- To manage anger or frustration

**BENEFITS:**
- Reduces anxiety quickly
- Helps with sleep
- Manages stress responses
- Promotes deep relaxation

This powerful technique gets better with practice.
"""
    
    def _deep_breathing(self, cycles: int) -> str:
        """Deep belly breathing instructions."""
        
        return f"""
🫁 DEEP BELLY BREATHING

Also called diaphragmatic breathing - the foundation of all breathing exercises.

**SETUP:**
1. Sit or lie down comfortably
2. Place one hand on chest, one on belly
3. Relax your shoulders

**THE PATTERN:** (Repeat {cycles} times)

**INHALE (5 seconds):**
- Breathe in slowly through your nose
- Feel your belly rise (hand on belly moves up)
- Chest should stay relatively still
- Fill lungs completely
- Count: 1, 2, 3, 4, 5

**PAUSE (2 seconds):**
- Hold breath gently
- Count: 1, 2

**EXHALE (7 seconds):**
- Breathe out slowly through mouth
- Feel belly fall (hand moves down)
- Empty lungs completely
- Count: 1, 2, 3, 4, 5, 6, 7

**Repeat {cycles} times**

**FOCUS POINTS:**
- Belly should move more than chest
- Breathe slowly and deeply
- Don't force the breath
- Notice the pause between breaths

**MENTAL TECHNIQUE:**
- Inhale: Think "I am"
- Exhale: Think "relaxed"
- Or visualize breathing in calm, breathing out tension

**BENEFITS:**
- Activates parasympathetic nervous system
- Lowers heart rate and blood pressure
- Reduces stress hormones
- Improves oxygen flow
- Promotes overall relaxation

**WHEN TO USE:**
- Daily practice (morning/evening)
- During stress or anxiety
- Before challenging situations
- To improve sleep

Practice makes perfect. Even 2-3 minutes makes a difference.
"""
    
    def _calming_breath(self, cycles: int) -> str:
        """Extended exhale calming breath."""
        
        return f"""
🕊️ CALMING BREATH (Extended Exhale)

Extended exhalation activates the body's natural calming response.

**WHY IT WORKS:**
Longer exhale stimulates vagus nerve → activates relaxation response

**THE PATTERN:** (Repeat {cycles} times)

🌬️ BREATHE IN (nose) - Count to 4
💨 BREATHE OUT (mouth/nose) - Count to 6-8

**DETAILED STEPS:**
1. Get comfortable, relax shoulders
2. Inhale through nose: 1, 2, 3, 4
3. Exhale slowly: 1, 2, 3, 4, 5, 6 (or up to 8)
4. Natural pause before next breath

**Repeat {cycles} times**

**PROGRESSIVE RELAXATION:**
With each exhale, release tension:
- Cycle 1: Release jaw and face
- Cycle 2: Relax shoulders and neck  
- Cycle 3: Let go of belly tension
- Continue: Scan body for tension

**VISUALIZATION:**
- Inhale: Cool, fresh air (blue light)
- Exhale: Warm, releasing stress (gray mist)

**BENEFITS:**
- Quick anxiety relief
- Lowers stress response
- Eases physical tension
- Promotes mental clarity

**BEST FOR:**
- Acute anxiety moments
- Before difficult conversations
- Managing anger or frustration
- Transitioning between activities

The exhale is your power. Let it carry away your worries.
"""
    
    def _quick_calm(self, cycles: int) -> str:
        """Quick calming breath for immediate relief."""
        
        return f"""
⚡ QUICK CALM BREATHING

For immediate stress relief - can be done anywhere, anytime.

**SUPER SIMPLE:**
1. Take a deep breath in through your nose (3 seconds)
2. Blow it out slowly through your mouth (5 seconds)
3. Repeat {cycles} times

**ENHANCED VERSION:**
- Inhale: Imagine breathing in peace and calm
- Exhale: Imagine blowing out stress and tension
- With each breath, feel yourself settling

**THE PRACTICE:**
1️⃣ Deep breath in (nose): 1, 2, 3
2️⃣ Slow breath out (mouth): 1, 2, 3, 4, 5
3️⃣ Repeat {cycles} times

**BODY AWARENESS:**
Notice:
- Cool air entering your nose
- Chest and belly expanding
- Warm air leaving your mouth
- Shoulders dropping with each exhale
- Mind starting to settle

**WHEN TO USE:**
- Feeling overwhelmed RIGHT NOW
- Before important meetings
- During panic or anxiety
- In crowded spaces
- When you can't do a longer practice

**ANYWHERE, ANYTIME:**
- At your desk
- In the car (not while driving!)
- Before presentations
- During conflicts
- In the bathroom (private moment)

Even ONE deep breath can help. Don't underestimate simple breathing.

**REMEMBER:**
You can always control your breath. It's your portable calm tool.
"""


def create_breathing_exercise_tool() -> BreathingExerciseTool:
    """Create an instance of the BreathingExerciseTool."""
    return BreathingExerciseTool()
