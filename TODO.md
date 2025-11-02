# 📋 Mental Health AI - Knowledge Base Enhancement TODO

> Roadmap for expanding and improving the RAG knowledge base

---

## 🎯 Current Status

- **Current Chunks:** ~252 chunks in ChromaDB
- **Current Categories:** 8 categories
- **Current Files:** ~20 text files
- **Target:** 1,000+ chunks for comprehensive coverage

---

## 🔥 Phase 1: Critical Priorities (Do First)

### 1. Singapore-Specific Resources 🇸🇬

**Priority:** CRITICAL - Most users need local information

**Files to Create:**

- [ ] `data/knowledge/singapore_resources/mental_health_services.txt`
  - Public services (IMH, polyclinics with mental health services)
  - Private psychiatrists and psychologists (with locations)
  - Community mental health teams
  - Support groups in Singapore
  - Addresses, phone numbers, operating hours
  - Costs and subsidies

- [ ] `data/knowledge/singapore_resources/youth_services.txt`
  - CHAT (Community Health Assessment Team) - detailed info
  - School counseling services
  - Youth mental health programs
  - University counseling centers (NUS, NTU, SMU)
  - Youth-specific hotlines and resources

- [ ] `data/knowledge/singapore_resources/workplace_resources.txt`
  - Employee Assistance Programs (EAP)
  - Workplace mental health policies
  - Work stress management resources
  - Burnout prevention programs
  - When and how to take medical leave

- [ ] `data/knowledge/singapore_resources/financial_assistance.txt`
  - Medisave coverage for mental health
  - Community Health Assist Scheme (CHAS)
  - Financial aid for treatment
  - Insurance coverage information
  - Subsidized care options

- [ ] `data/knowledge/singapore_resources/cultural_considerations.txt`
  - Mental health stigma in Asian cultures
  - Culturally sensitive approaches
  - Family involvement in treatment
  - Traditional vs modern treatment views
  - Language considerations (English, Mandarin, Malay, Tamil)

---

### 2. Specific Mental Health Conditions 🧠

**Priority:** HIGH - Common user queries

**Files to Create:**

- [ ] `data/knowledge/conditions/depression.txt`
  - Types: Major depression, persistent depressive disorder, postpartum, seasonal (SAD)
  - Symptoms and warning signs
  - Causes and risk factors
  - Treatment options (therapy, medication, lifestyle)
  - Self-help strategies
  - When to seek professional help
  - Singapore-specific resources

- [ ] `data/knowledge/conditions/anxiety_disorders.txt`
  - Generalized Anxiety Disorder (GAD)
  - Panic Disorder and panic attacks
  - Social Anxiety Disorder
  - Specific phobias
  - OCD (Obsessive-Compulsive Disorder)
  - Symptoms for each type
  - Treatment approaches
  - Coping techniques

- [ ] `data/knowledge/conditions/panic_disorder.txt`
  - What is a panic attack vs panic disorder
  - Physical symptoms (heart racing, sweating, trembling)
  - Panic attack vs heart attack differences
  - Grounding techniques
  - Breathing exercises
  - Long-term management

- [ ] `data/knowledge/conditions/bipolar_disorder.txt`
  - Manic and depressive episodes
  - Warning signs
  - Treatment (medication + therapy)
  - Singapore resources

- [ ] `data/knowledge/conditions/ptsd.txt`
  - What is PTSD
  - Trauma symptoms
  - Treatment approaches
  - Support in Singapore

- [ ] `data/knowledge/conditions/eating_disorders.txt`
  - Anorexia, bulimia, binge eating
  - Warning signs
  - Treatment resources in Singapore

- [ ] `data/knowledge/conditions/adhd_adults.txt`
  - Adult ADHD symptoms
  - Diagnosis process in Singapore
  - Treatment options
  - Coping strategies

---

### 3. Crisis & Emergency Information 🚨

**Priority:** CRITICAL - Safety-critical content

**Files to Create:**

- [ ] `data/knowledge/emergency/suicide_prevention.txt`
  - Detailed warning signs
  - Risk factors and protective factors
  - How to help someone considering suicide
  - What to say and what not to say
  - Safety planning steps
  - Aftermath of suicide attempt
  - Bereavement support

- [ ] `data/knowledge/emergency/self_harm.txt`
  - Understanding self-harm behavior
  - Why people self-harm
  - Harm reduction strategies
  - Treatment approaches
  - How to support someone who self-harms
  - When to seek emergency help

- [ ] `data/knowledge/emergency/psychotic_episode.txt`
  - Recognizing psychosis symptoms
  - What to do during an episode
  - How to communicate with someone in psychosis
  - Getting emergency help
  - Follow-up care

- [ ] `data/knowledge/emergency/severe_anxiety_panic.txt`
  - Panic attack vs medical emergency
  - When to call 995 vs when to self-manage
  - Immediate grounding techniques
  - Supporting someone having a panic attack

- [ ] `data/knowledge/emergency/domestic_violence.txt`
  - Recognizing abuse patterns
  - Safety planning
  - Resources in Singapore (AWARE, TRANS SAFE Centre)
  - Legal protections and restraining orders

---

### 4. Common FAQs ❓

**Priority:** HIGH - Frequently asked questions

**Files to Create:**

- [ ] `data/knowledge/faqs/therapy_questions.txt`
  - What is therapy/counseling?
  - Types of therapy (CBT, DBT, psychodynamic, etc.)
  - What to expect in first session
  - How to find a therapist in Singapore
  - Cost considerations and subsidies
  - Online vs in-person therapy
  - How long does therapy take?
  - Confidentiality in therapy

- [ ] `data/knowledge/faqs/medication_questions.txt`
  - When is medication needed?
  - Common psychiatric medications (antidepressants, anti-anxiety, etc.)
  - How long to take medication
  - Side effects and management
  - Stigma around medication
  - Medication + therapy combination
  - Stopping medication safely

- [ ] `data/knowledge/faqs/crisis_faqs.txt`
  - What constitutes a mental health crisis?
  - When to go to emergency department
  - What happens at A&E for mental health
  - Involuntary admission process in Singapore
  - Supporting a family member in crisis

- [ ] `data/knowledge/faqs/workplace_mental_health.txt`
  - Should I disclose mental health at work?
  - Workplace accommodations
  - Dealing with work-related stress
  - When to take medical leave
  - Return to work strategies
  - Employment rights

---

## ⭐ Phase 2: Important Enhancements

### 5. Life Stage Specific Content 👶👴

**Files to Create:**

- [ ] `data/knowledge/life_stages/children_mental_health.txt`
  - Common childhood mental health issues
  - School-related stress and bullying
  - Developmental concerns
  - Resources for parents
  - Child psychiatry services in Singapore

- [ ] `data/knowledge/life_stages/adolescent_mental_health.txt`
  - Teen depression and anxiety
  - Academic pressure in Singapore education system
  - Identity and self-esteem issues
  - Peer pressure and social media
  - PSLE/O-Level/A-Level stress management

- [ ] `data/knowledge/life_stages/young_adults.txt`
  - University and career stress
  - Relationship issues
  - Quarter-life crisis
  - NS (National Service) mental health
  - Life transitions

- [ ] `data/knowledge/life_stages/adults.txt`
  - Work-life balance
  - Parenting stress
  - Midlife challenges
  - Relationship and marriage issues
  - Sandwich generation stress

- [ ] `data/knowledge/life_stages/elderly_mental_health.txt`
  - Depression in seniors
  - Cognitive decline vs depression
  - Social isolation and loneliness
  - Grief and loss
  - Resources for elderly in Singapore

- [ ] `data/knowledge/life_stages/pregnancy_postpartum.txt`
  - Prenatal anxiety and depression
  - Postpartum depression (PPD)
  - Postpartum psychosis
  - Support resources in Singapore
  - When to seek help

---

### 6. Practical Self-Help Techniques 🛠️

**Files to Create:**

- [ ] `data/knowledge/self_help/mindfulness_meditation.txt`
  - Basic mindfulness techniques
  - Guided meditation scripts
  - Mindfulness apps and resources
  - Daily practice tips
  - Body scan meditation
  - Mindful breathing

- [ ] `data/knowledge/self_help/cognitive_behavioral_techniques.txt`
  - Thought challenging and restructuring
  - Behavioral activation
  - Exposure therapy basics
  - Journaling exercises
  - Thought records
  - Evidence for/against thoughts

- [ ] `data/knowledge/self_help/sleep_hygiene.txt`
  - Sleep schedule optimization
  - Bedroom environment setup
  - Pre-sleep routines
  - Dealing with insomnia
  - Sleep and mental health connection
  - When to see a sleep specialist

- [ ] `data/knowledge/self_help/exercise_mental_health.txt`
  - Mental health benefits of exercise
  - Exercise recommendations
  - Overcoming barriers to exercise
  - Mind-body exercises (yoga, tai chi)
  - Exercise resources in Singapore

- [ ] `data/knowledge/self_help/nutrition_mental_health.txt`
  - Foods that support mental health
  - Foods to limit
  - Eating patterns and mood
  - Hydration importance
  - Singapore healthy eating guidelines

- [ ] `data/knowledge/self_help/social_connection.txt`
  - Building support networks
  - Maintaining healthy relationships
  - Dealing with loneliness
  - Support groups in Singapore
  - Community activities

- [ ] `data/knowledge/self_help/stress_management.txt`
  - Time management techniques
  - Boundary setting
  - Progressive muscle relaxation
  - Problem-solving strategies
  - Learning to say no
  - Work-life balance

---

### 7. Treatment Information 💊

**Files to Create:**

- [ ] `data/knowledge/treatment/antidepressants.txt`
  - SSRIs, SNRIs, tricyclics
  - How antidepressants work
  - Common side effects
  - What to expect (timeline)
  - Discontinuation syndrome
  - Pregnancy and antidepressants

- [ ] `data/knowledge/treatment/anti_anxiety_medications.txt`
  - Benzodiazepines
  - Buspirone
  - Beta-blockers
  - Usage guidelines
  - Dependency concerns

- [ ] `data/knowledge/treatment/mood_stabilizers.txt`
  - Lithium
  - Anticonvulsants for mood
  - Monitoring requirements

- [ ] `data/knowledge/treatment/therapy_types.txt`
  - CBT (Cognitive Behavioral Therapy) - detailed
  - DBT (Dialectical Behavior Therapy)
  - ACT (Acceptance Commitment Therapy)
  - Psychodynamic therapy
  - Interpersonal therapy
  - Family therapy
  - Group therapy
  - Which therapy for which condition

- [ ] `data/knowledge/treatment/alternative_treatments.txt`
  - Art therapy
  - Music therapy
  - Animal-assisted therapy
  - Acupuncture
  - Traditional Chinese Medicine perspectives
  - Complementary approaches
  - Evidence base for each

---

### 8. Caregiver Support 👨‍👩‍👧

**Files to Create:**

- [ ] `data/knowledge/caregivers/supporting_someone.txt`
  - How to talk about mental health
  - Active listening skills
  - What to say and what NOT to say
  - Encouraging treatment
  - Setting healthy boundaries
  - When to step back

- [ ] `data/knowledge/caregivers/caregiver_burnout.txt`
  - Recognizing caregiver burnout
  - Self-care for caregivers
  - Respite care options
  - Support groups for caregivers in Singapore
  - When to seek your own help

- [ ] `data/knowledge/caregivers/family_therapy.txt`
  - When to involve family in treatment
  - Family psychoeducation
  - Communication strategies
  - Resources for families in Singapore

---

## 💡 Phase 3: Nice to Have

### 9. Stigma & Awareness 🎭

**Files to Create:**

- [ ] `data/knowledge/awareness/mental_health_myths.txt`
  - Common myths debunked
  - "Mental illness isn't real"
  - "Just snap out of it"
  - "Therapy is only for weak people"
  - "Medication changes your personality"
  - Evidence-based corrections

- [ ] `data/knowledge/awareness/cultural_stigma.txt`
  - Mental health stigma in Asian cultures
  - Family expectations and "face"
  - Shame and honor cultures
  - Breaking stigma
  - Intergenerational differences

- [ ] `data/knowledge/awareness/success_stories.txt`
  - Recovery is possible
  - Famous people who've spoken about mental health
  - Personal growth through treatment
  - Hope and resilience

---

### 10. Specific Populations 🌈

**Files to Create:**

- [ ] `data/knowledge/populations/lgbtq_mental_health.txt`
  - Unique mental health challenges
  - Coming out stress
  - Discrimination and minority stress
  - LGBTQ-affirming resources in Singapore
  - Support organizations (Oogachaga, Pink Dot)

- [ ] `data/knowledge/populations/migrant_workers.txt`
  - Language barriers to care
  - Isolation and homesickness
  - Work-related stress
  - Accessible resources
  - Multilingual support

- [ ] `data/knowledge/populations/international_students.txt`
  - Culture shock and adjustment
  - Academic pressure
  - Being away from family
  - University counseling services

- [ ] `data/knowledge/populations/disabilities_mental_health.txt`
  - Intersection of physical and mental health
  - Accessibility needs
  - Specialized services in Singapore

---

## 📊 Progress Tracking

### Phase 1 Progress
- [ ] Singapore Resources: 0/5 files
- [ ] Conditions: 0/7 files
- [ ] Emergency: 0/5 files
- [ ] FAQs: 0/4 files
- **Total Phase 1:** 0/21 files

### Phase 2 Progress
- [ ] Life Stages: 0/6 files
- [ ] Self-Help: 0/7 files
- [ ] Treatment: 0/4 files
- [ ] Caregivers: 0/3 files
- **Total Phase 2:** 0/20 files

### Phase 3 Progress
- [ ] Awareness: 0/3 files
- [ ] Populations: 0/4 files
- **Total Phase 3:** 0/7 files

### **Overall Progress: 0/48 files**

---

## 🎯 Quick Wins - Top 5 Files to Create First

These will give you the most immediate improvement:

1. **`singapore_resources/mental_health_services.txt`**
   - Comprehensive list of all mental health services in Singapore
   - Most commonly requested information

2. **`conditions/depression.txt`**
   - Depression is one of most common queries
   - Detailed, comprehensive guide

3. **`conditions/anxiety_disorders.txt`**
   - Anxiety/panic is extremely common
   - Practical, actionable content

4. **`faqs/therapy_questions.txt`**
   - Answers the most common user questions
   - Reduces uncertainty about seeking help

5. **`self_help/cognitive_behavioral_techniques.txt`**
   - Practical techniques users can try immediately
   - Evidence-based, actionable advice

---

## 📚 Content Sources & References

### Reliable Sources to Use:
- ✅ National Institute of Mental Health (NIMH)
- ✅ NHS Mental Health (UK)
- ✅ Beyond Blue (Australia)
- ✅ Mind (UK)
- ✅ Institute of Mental Health Singapore (IMH)
- ✅ Ministry of Health Singapore (MOH)
- ✅ WHO Mental Health Resources
- ✅ American Psychological Association (APA)
- ✅ Singapore Association for Mental Health (SAMH)
- ✅ National Council of Social Service (NCSS)

### Content Guidelines:
- Use simple, accessible language
- Include Singapore-specific context
- Provide practical, actionable advice
- Include real examples
- Cite sources when appropriate
- Maintain consistent formatting
- Keep cultural sensitivity in mind

---

## 🔄 Update Process

After creating each file:

1. **Add file to appropriate category** in `data/knowledge/`
2. **Run update agent:**
   ```bash
   python agent/update_agent.py auto
   ```
3. **Verify addition:**
   ```bash
   python agent/update_agent.py status
   ```
4. **Test RAG retrieval** with relevant queries
5. **Check this box** in TODO.md
6. **Commit to Git** with descriptive message

---

## 🎉 Expected Impact

### Before (Current):
- ~250 chunks in ChromaDB
- Basic coverage of mental health topics
- Generic responses
- Limited Singapore context

### After (Target):
- ~1,000+ chunks in ChromaDB
- Comprehensive coverage
- Specific, actionable guidance
- Rich Singapore context
- Better RAG accuracy
- More helpful responses

---

## 📝 Notes

- Focus on **quality over quantity** - each file should be comprehensive
- **Singapore context is crucial** - always include local resources
- **Keep updating** - mental health resources change, review quarterly
- **User feedback** - track what queries aren't answered well, add content accordingly
- **Version control** - commit each major addition to track progress

---

**Last Updated:** November 1, 2025
**Version:** 1.0
**Status:** Planning Phase
