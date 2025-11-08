"""
Crisis Hotline Tool - Quick Access to Crisis Support
Provides immediate crisis hotline information and safety resources
"""

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field


class CrisisInput(BaseModel):
    """Input schema for crisis hotline tool."""
    urgency: str = Field(
        description="Urgency level: 'immediate', 'high', 'moderate'"
    )
    crisis_type: Optional[str] = Field(
        default="general",
        description="Type of crisis: 'suicide', 'self_harm', 'severe_distress', 'general'"
    )


class CrisisHotlineTool(BaseTool):
    """Tool for immediate crisis support information."""
    
    name: str = "get_crisis_hotlines"
    description: str = """
    Get immediate crisis hotline information and emergency mental health resources.
    
    Use this tool when:
    - User is in crisis or severe distress
    - Suicidal ideation expressed
    - Self-harm risk detected
    - Immediate support needed
    
    Input: urgency level and optional crisis type
    Output: Crisis hotlines and immediate safety resources
    """
    args_schema: Type[BaseModel] = CrisisInput
    
    def _run(
        self,
        urgency: str,
        crisis_type: Optional[str] = "general"
    ) -> str:
        """Get crisis hotlines based on urgency."""
        
        if urgency.lower() == "immediate":
            return self._immediate_crisis_response()
        elif crisis_type and crisis_type.lower() == "suicide":
            return self._suicide_prevention_resources()
        elif crisis_type and crisis_type.lower() == "self_harm":
            return self._self_harm_resources()
        else:
            return self._general_crisis_resources()
    
    async def _arun(
        self,
        urgency: str,
        crisis_type: Optional[str] = "general"
    ) -> str:
        """Async version."""
        return self._run(urgency, crisis_type)
    
    def _immediate_crisis_response(self) -> str:
        """Immediate crisis intervention information."""
        
        return """
🚨 IMMEDIATE CRISIS SUPPORT 🚨

If you or someone is in IMMEDIATE DANGER:

**CALL NOW:**
📞 995 - Emergency Ambulance/Police
📞 1-767 - Samaritans of Singapore (24/7)
📞 6389-2222 - IMH Mental Health Helpline (24/7)

**SAFETY FIRST:**
1. Remove immediate means of harm
2. Stay with the person (or call someone to be with you)
3. Don't leave them alone
4. Seek immediate professional help

**Go to Nearest Emergency Department:**
- Singapore General Hospital A&E: 6222-3322
- National University Hospital A&E: 6779-5555  
- Tan Tock Seng Hospital A&E: 6256-6011
- IMH Emergency: 6389-2000 (24/7)

**OR:**
Call 995 for immediate ambulance assistance.

YOU ARE NOT ALONE. HELP IS AVAILABLE NOW.

This is a mental health crisis. Professional intervention is critical.
Please reach out to these services immediately.
"""
    
    def _suicide_prevention_resources(self) -> str:
        """Suicide prevention specific resources."""
        
        return """
🆘 SUICIDE PREVENTION RESOURCES 🆘

You are not alone. Help is available right now.

**24/7 CRISIS HOTLINES:**
📞 Samaritans of Singapore (SOS): 1-767
   - Available 24 hours, every day
   - Confidential emotional support
   - Call anytime you need to talk

📞 IMH Mental Health Helpline: 6389-2222
   - 24/7 professional support
   - Immediate crisis intervention
   
📞 Singapore Association for Mental Health: 1800-283-7019
   - Available 9am-1am daily

**FOR YOUTH (16-30):**
📞 CHAT: 6493-6500/6501
📱 WhatsApp: 9898-4584

**IMMEDIATE DANGER:**
📞 Call 995 (Emergency)
🏥 Go to nearest hospital Emergency Department

**SAFETY PLAN:**
1. Call a crisis hotline NOW
2. Remove means of self-harm
3. Contact trusted person
4. Go to safe environment
5. Seek emergency medical care

**REMEMBER:**
- Suicidal thoughts are temporary
- Pain is temporary, suicide is permanent
- You matter, your life has value
- Recovery is possible with help

**Resources:**
- IMH Emergency Service (24/7): 6389-2000
- Samaritans Befriending Centres: Multiple locations

Crisis support is available RIGHT NOW. Please reach out.
You deserve help. You deserve to live.
"""
    
    def _self_harm_resources(self) -> str:
        """Self-harm specific resources."""
        
        return """
💙 SELF-HARM SUPPORT RESOURCES 💙

If you're struggling with self-harm urges or behaviors:

**IMMEDIATE SUPPORT:**
📞 Samaritans of Singapore: 1-767 (24/7)
📞 IMH Helpline: 6389-2222 (24/7)
📞 SAMH: 1800-283-7019 (9am-1am)

**FOR YOUTH:**
📞 CHAT: 6493-6500/6501
📱 WhatsApp: 9898-4584

**COPING STRATEGIES:**
When you feel the urge to self-harm:
1. Call a crisis hotline immediately
2. Use ice cubes (hold in hand)
3. Draw on skin with red marker instead
4. Squeeze stress ball intensely
5. Do intense physical exercise
6. Take a cold shower
7. Reach out to trusted person

**DISTRACTION TECHNIQUES:**
- Count backwards from 100 by 7s
- Name 5 things you can see/hear/touch
- Play loud music
- Write in a journal
- Use grounding techniques

**PROFESSIONAL HELP:**
- IMH Emergency: 6389-2000 (24/7)
- Nearest hospital Emergency Department
- School counselor or therapist

**REMEMBER:**
- Self-harm is a sign you need support
- You're not "bad" or "attention-seeking"
- Recovery is possible with help
- Healthier coping strategies can be learned

**IF BLEEDING OR INJURED:**
📞 Call 995 or go to Emergency Department immediately

You deserve support and care. Please reach out now.
"""
    
    def _general_crisis_resources(self) -> str:
        """General crisis support resources."""
        
        return """
🆘 CRISIS SUPPORT RESOURCES 🆘

**24/7 HELPLINES:**
📞 Samaritans of Singapore (SOS): 1-767
   - 24/7 emotional support
   - Confidential listening service
   
📞 IMH Mental Health Helpline: 6389-2222
   - 24/7 professional crisis support
   
📞 SAMH Helpline: 1800-283-7019
   - Available 9am-1am daily

**FOR SPECIFIC DEMOGRAPHICS:**

Youth (16-30):
📞 CHAT: 6493-6500/6501
📱 WhatsApp: 9898-4584

Children:
📞 Tinkle Friend: 1800-2744-788
   (2:30pm-5pm school days)

**OTHER SUPPORT:**
📞 Care Corner: 1800-353-5800
   (Mon-Fri 10am-10pm, Sat 10am-5pm)
   
📞 TOUCHline: 1800-377-2252
   (Mon-Fri 9am-6pm)

**EMERGENCY SERVICES:**
📞 995 - Emergency Ambulance/Police
🏥 Hospital Emergency Departments (24/7)
🏥 IMH Emergency Service: 6389-2000

**WHEN TO SEEK EMERGENCY HELP:**
- Thoughts of harming yourself or others
- Unable to care for yourself
- Severe emotional distress
- Psychotic symptoms
- Risk of immediate harm

**SAFETY PLANNING:**
1. Contact crisis hotline
2. Reach out to trusted person
3. Remove access to harmful items
4. Go to safe environment
5. Seek professional evaluation

You don't have to face this alone. Support is available now.
"""


def create_crisis_hotline_tool() -> CrisisHotlineTool:
    """Create an instance of the CrisisHotlineTool."""
    return CrisisHotlineTool()
