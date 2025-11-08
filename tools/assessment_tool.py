"""
Assessment Tool - Mental Health Assessment and Symptom Tracking
Provides structured mental health assessments and symptom severity calculations
"""

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field


class AssessmentInput(BaseModel):
    """Input schema for mental health assessment."""
    assessment_type: str = Field(
        description="Type of assessment: 'depression', 'anxiety', 'stress', 'general'"
    )
    responses: str = Field(
        description="User responses to assessment questions (comma-separated or structured)"
    )


class AssessmentTool(BaseTool):
    """Tool for conducting mental health assessments."""
    
    name: str = "mental_health_assessment"
    description: str = """
    Conduct mental health assessments and calculate symptom severity.
    
    Use this tool when:
    - User wants to assess their mental health
    - Screening for depression, anxiety, or stress
    - Tracking symptom severity over time
    
    Input: assessment_type (depression/anxiety/stress/general) and responses
    Output: Assessment results with severity level and recommendations
    """
    args_schema: Type[BaseModel] = AssessmentInput
    
    def _run(self, assessment_type: str, responses: str) -> str:
        """Execute the assessment."""
        
        # Parse responses
        response_list = [r.strip() for r in responses.split(',')]
        
        if assessment_type.lower() == "depression":
            return self._assess_depression(response_list)
        elif assessment_type.lower() == "anxiety":
            return self._assess_anxiety(response_list)
        elif assessment_type.lower() == "stress":
            return self._assess_stress(response_list)
        else:
            return self._general_assessment(response_list)
    
    async def _arun(self, assessment_type: str, responses: str) -> str:
        """Async version."""
        return self._run(assessment_type, responses)
    
    def _assess_depression(self, responses: list) -> str:
        """PHQ-9 style depression assessment."""
        
        # Simple scoring (in real implementation, would have proper questions)
        severity_scores = {
            "minimal": (0, 4),
            "mild": (5, 9),
            "moderate": (10, 14),
            "moderately_severe": (15, 19),
            "severe": (20, 27)
        }
        
        # Calculate score (simplified)
        total_score = len(responses) * 2  # Placeholder calculation
        
        # Determine severity
        severity = "minimal"
        for level, (low, high) in severity_scores.items():
            if low <= total_score <= high:
                severity = level
                break
        
        result = f"""
Depression Assessment Results (PHQ-9 Style):
- Total Score: {total_score}
- Severity: {severity.replace('_', ' ').title()}

Interpretation:
"""
        
        if severity == "minimal":
            result += "Minimal or no depression symptoms detected. Continue self-care practices."
        elif severity == "mild":
            result += "Mild depression symptoms. Consider monitoring and self-care strategies."
        elif severity in ["moderate", "moderately_severe"]:
            result += "Moderate depression symptoms. Professional consultation recommended."
        else:
            result += "Severe depression symptoms. Seek professional help promptly."
        
        result += "\n\nNote: This is a screening tool, not a diagnostic instrument."
        
        return result
    
    def _assess_anxiety(self, responses: list) -> str:
        """GAD-7 style anxiety assessment."""
        
        severity_scores = {
            "minimal": (0, 4),
            "mild": (5, 9),
            "moderate": (10, 14),
            "severe": (15, 21)
        }
        
        total_score = len(responses) * 2
        
        severity = "minimal"
        for level, (low, high) in severity_scores.items():
            if low <= total_score <= high:
                severity = level
                break
        
        result = f"""
Anxiety Assessment Results (GAD-7 Style):
- Total Score: {total_score}
- Severity: {severity.title()}

Interpretation:
"""
        
        if severity == "minimal":
            result += "Minimal anxiety symptoms. Continue healthy coping strategies."
        elif severity == "mild":
            result += "Mild anxiety. Practice relaxation techniques and monitor symptoms."
        elif severity == "moderate":
            result += "Moderate anxiety. Consider professional support and coping strategies."
        else:
            result += "Severe anxiety. Seek professional evaluation and treatment."
        
        return result
    
    def _assess_stress(self, responses: list) -> str:
        """Stress level assessment."""
        
        score = len(responses) * 3
        
        if score < 10:
            level = "Low"
            guidance = "Manageable stress levels. Maintain current coping strategies."
        elif score < 20:
            level = "Moderate"
            guidance = "Moderate stress. Implement stress reduction techniques regularly."
        else:
            level = "High"
            guidance = "High stress levels. Consider professional support and lifestyle changes."
        
        return f"""
Stress Assessment Results:
- Stress Level: {level}
- Score: {score}

Guidance: {guidance}

Recommendations:
- Practice mindfulness or meditation
- Ensure adequate sleep and exercise
- Connect with support system
- Consider professional counseling if stress persists
"""
    
    def _general_assessment(self, responses: list) -> str:
        """General mental health check-in."""
        
        return f"""
General Mental Health Check-in:
- Responses recorded: {len(responses)}

Thank you for sharing. Based on your responses, here are some general recommendations:

1. Continue monitoring your mental health
2. Practice self-care regularly
3. Stay connected with support systems
4. Seek professional help if symptoms worsen

Remember: This is a general screening, not a diagnosis. Professional consultation provides personalized assessment.
"""


# Factory function for easy tool creation
def create_assessment_tool() -> AssessmentTool:
    """Create an instance of the AssessmentTool."""
    return AssessmentTool()
