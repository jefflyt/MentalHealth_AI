"""
Resource Finder Tool - Singapore Mental Health Resources
Helps users find mental health services, hotlines, and support groups in Singapore
"""

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field


class ResourceInput(BaseModel):
    """Input schema for resource finder."""
    resource_type: str = Field(
        description="Type of resource: 'hotline', 'therapy', 'support_group', 'emergency', 'youth', 'general'"
    )
    location: Optional[str] = Field(
        default="Singapore",
        description="Location (defaults to Singapore)"
    )
    demographic: Optional[str] = Field(
        default=None,
        description="Specific demographic: 'youth', 'elderly', 'adult', 'family'"
    )


class ResourceFinderTool(BaseTool):
    """Tool for finding mental health resources in Singapore."""
    
    name: str = "find_mental_health_resources"
    description: str = """
    Find mental health services, hotlines, and support resources in Singapore.
    
    Use this tool when:
    - User needs therapist or counseling services
    - Looking for crisis hotlines
    - Seeking support groups
    - Finding emergency mental health services
    - Youth-specific or demographic-specific resources
    
    Input: resource_type, optional location and demographic
    Output: List of relevant resources with contact information
    """
    args_schema: Type[BaseModel] = ResourceInput
    
    def _run(
        self,
        resource_type: str,
        location: Optional[str] = "Singapore",
        demographic: Optional[str] = None
    ) -> str:
        """Find mental health resources."""
        
        if resource_type.lower() == "hotline":
            return self._get_hotlines(demographic)
        elif resource_type.lower() == "therapy":
            return self._get_therapy_services(demographic)
        elif resource_type.lower() == "support_group":
            return self._get_support_groups(demographic)
        elif resource_type.lower() == "emergency":
            return self._get_emergency_resources()
        elif resource_type.lower() == "youth":
            return self._get_youth_resources()
        else:
            return self._get_general_resources()
    
    async def _arun(
        self,
        resource_type: str,
        location: Optional[str] = "Singapore",
        demographic: Optional[str] = None
    ) -> str:
        """Async version."""
        return self._run(resource_type, location, demographic)
    
    def _get_hotlines(self, demographic: Optional[str]) -> str:
        """Get crisis hotlines."""
        
        hotlines = """
🆘 Singapore Mental Health Hotlines:

**24/7 Emergency Hotlines:**
- Samaritans of Singapore (SOS): 1-767
  Available 24/7 for anyone in crisis
  
- Institute of Mental Health (IMH) Helpline: 6389-2222
  24/7 mental health crisis helpline

- Singapore Association for Mental Health (SAMH): 1800-283-7019
  Available 9am-1am daily
"""
        
        if demographic == "youth":
            hotlines += """
**Youth-Specific Hotlines:**
- CHAT (Community Health Assessment Team): 6493-6500/6501
  WhatsApp: 9898-4584
  For young people aged 16-30
  
- Tinkle Friend (for children): 1800-2744-788
  Available 2:30pm-5pm on school days
"""
        
        hotlines += """
**Other Support Lines:**
- Care Corner Counselling Hotline: 1800-353-5800
  Mon-Fri: 10am-10pm, Sat: 10am-5pm

- TOUCHline (Counselling): 1800-377-2252
  Mon-Fri: 9am-6pm
"""
        
        return hotlines
    
    def _get_therapy_services(self, demographic: Optional[str]) -> str:
        """Get therapy and counseling services."""
        
        services = """
🏥 Singapore Mental Health Services:

**Public Mental Health Services:**
- Institute of Mental Health (IMH)
  Tel: 6389-2000
  Address: 10 Buangkok View, Singapore 539747
  
- Polyclinics - Mental Health Services
  Available at most Singapore polyclinics
  Subsidized rates with referral

**Community Mental Health Services:**
- Community Health Assessment Team (CHAT)
  Multiple locations across Singapore
  Tel: 6493-6500/6501
  For youth aged 16-30
"""
        
        if demographic == "youth":
            services += """
**Youth Services:**
- REACH (Response, Early Intervention, Assessment in Community Mental Health)
  School-based mental health support
  
- eC2 (Enhanced Community Care)
  Community mental health support
  Tel: 6389-2200
"""
        
        services += """
**Private Counseling Centers:**
- Singapore Counselling Centre: 6337-6061
- Shan You Counselling Centre: 6741-0178
- Eagles Mediation & Counselling Centre: 1800-333-3616

**Online Counseling:**
- CPH eConsult (IMH): 6389-2200
  Mon-Fri: 9am-5pm
"""
        
        return services
    
    def _get_support_groups(self, demographic: Optional[str]) -> str:
        """Get support groups information."""
        
        groups = """
🤝 Singapore Mental Health Support Groups:

**Peer Support Groups:**
- Singapore Association for Mental Health (SAMH)
  Various peer support groups
  Tel: 1800-283-7019
  
- Club HEAL
  Recovery-focused peer support
  Tel: 6899-3463

- Silver Ribbon Singapore
  Fighting mental health stigma
  Tel: 6385-3714
"""
        
        if demographic == "youth":
            groups += """
**Youth Support Groups:**
- Youth CHAT Support Groups
  Peer support for young adults
  
- Campus PSY
  University student mental health support
"""
        
        groups += """
**Family Support:**
- REACH Family Support Programme
  Support for families of persons with mental health conditions
  
- Caregivers Alliance Limited (CAL)
  Support for caregivers
  Tel: 6460-4400

**Online Communities:**
- Limitless (by SAMH)
  Online peer support community
  Visit: www.limitless.sg
"""
        
        return groups
    
    def _get_emergency_resources(self) -> str:
        """Get emergency mental health resources."""
        
        return """
🚨 EMERGENCY Mental Health Resources:

**IMMEDIATE CRISIS:**
If you or someone is in immediate danger:
- Call 995 (Ambulance/Police)
- Go to nearest hospital Emergency Department

**24/7 Crisis Helplines:**
- Samaritans of Singapore: 1-767
- IMH Mental Health Helpline: 6389-2222
- Police (Non-emergency): 1800-255-0000

**Emergency Departments with Psychiatric Services:**
- Singapore General Hospital (SGH) A&E: 6222-3322
- National University Hospital (NUH) A&E: 6779-5555
- Tan Tock Seng Hospital (TTSH) A&E: 6256-6011

**After-Hours Mental Health Care:**
- IMH Emergency Service (24/7)
  Address: 10 Buangkok View, Singapore 539747
  Tel: 6389-2000

Remember: In a mental health crisis, seek immediate professional help. These services are available 24/7.
"""
    
    def _get_youth_resources(self) -> str:
        """Get youth-specific resources."""
        
        return """
👥 Singapore Youth Mental Health Resources:

**CHAT (Community Health Assessment Team):**
- Tel: 6493-6500/6501
- WhatsApp: 9898-4584
- Email: chat@mentalhealth.sg
- For ages 16-30
- Free and confidential assessment

**School-Based Services:**
- School Counselors (available in all schools)
- REACH Programme (school mental health)

**Youth-Friendly Hotlines:**
- Tinkle Friend: 1800-2744-788 (for children)
- eC2 Helpline: 6389-2200

**Youth Support Programs:**
- Campus PSY (university students)
- Youth Corps Singapore mental health programs
- Limitless online community

**Online Resources:**
- mindline.sg - Youth mental health information
- CHAT website - Resources and self-assessment tools

All services are confidential and youth-friendly.
"""
    
    def _get_general_resources(self) -> str:
        """Get general mental health resources."""
        
        return """
📚 General Mental Health Resources in Singapore:

**Main Organizations:**
- Institute of Mental Health (IMH): 6389-2000
- Singapore Association for Mental Health (SAMH): 1800-283-7019
- Silver Ribbon Singapore: 6385-3714

**Information & Support:**
- Health Hub (Singapore): www.healthhub.sg
- mindline.sg - Mental health information portal
- IMH Mental Health Helpline: 6389-2222 (24/7)

**Community Services:**
- Social Service Offices (SSOs) - Mental health support
- Family Service Centres (FSCs) - Counseling services
- Community Health Assessment Team (CHAT)

**Workplace Support:**
- Workplace counseling services
- Employee Assistance Programmes (EAP)

**Financial Assistance:**
- ComCare (for low-income)
- Medifund (medical bill assistance)
- VWOs offering subsidized services

For personalized recommendations, please share more about your specific needs.
"""


def create_resource_finder_tool() -> ResourceFinderTool:
    """Create an instance of the ResourceFinderTool."""
    return ResourceFinderTool()
