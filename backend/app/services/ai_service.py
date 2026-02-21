from typing import Optional, Dict, List
import json
import re
import random
from datetime import datetime, timezone

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
from ..config import settings


class AIService:
    """AI Service for LLM integrations - Exclusively using Gemini 2.0 Flash"""
    
    def __init__(self):
        if GEMINI_AVAILABLE and settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)
            self.model = "gemini-2.0-flash"
        else:
            print("Warning: Gemini initialization failed. Check API key and google-genai package.")
            self.client = None
            self.model = None
    
    def _convert_messages_for_gemini(self, messages: List[Dict[str, str]]) -> tuple:
        """Convert OpenAI-style messages to Gemini format"""
        gemini_messages = []
        system_instruction = None
        
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            
            if role == "system":
                system_instruction = content
            elif role == "user":
                gemini_messages.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=content)]
                ))
            elif role == "assistant":
                gemini_messages.append(types.Content(
                    role="model", 
                    parts=[types.Part.from_text(text=content)]
                ))
                
        return system_instruction, gemini_messages
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Generate chat completion using Gemini"""
        try:
            if self.client and settings.gemini_api_key:
                system_instruction, gemini_messages = self._convert_messages_for_gemini(messages)
                
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=gemini_messages,
                    config=config
                )
                
                # Check for response text (safety filters might block it)
                try:
                    return response.text
                except (ValueError, AttributeError):
                    # If blocked, try to get fallback based on user message
                    print("Warning: Gemini response blocked by safety filters.")
                    user_msg = messages[-1]["content"] if messages else ""
                    return self._get_fallback_response(user_msg)
            
            else:
                return "AI provider not available. Please check your Gemini API configuration."

        
        except Exception as e:
            print(f"AI Error: {e}")
            # Use intelligent fallback on failure
            user_msg = messages[-1]["content"] if messages else ""
            return self._get_fallback_response(user_msg)
            
    def _extract_json(self, text: str) -> Dict:
        """Helper to extract and parse JSON from LLM response safely"""
        if not text or not isinstance(text, str):
            return {}
            
        try:
            # Try direct parse
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Try to find JSON block inside markdown or text
            
            # 1. Look for ```json ... ```
            json_block_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if json_block_match:
                try:
                    return json.loads(json_block_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # 2. Look for any block between { and }
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            return {"error": "Failed to parse AI response as JSON", "raw_content": text}
    
    async def academic_assistance(
        self, 
        task_description: str,
        branch: str,
        task_type: str,
        student_history: Optional[Dict] = None
    ) -> str:
        """Provide academic assistance"""
        history_context = ""
        if student_history:
            weak_areas = ", ".join(student_history.get("weak_areas", []))
            strong_areas = ", ".join(student_history.get("strong_areas", []))
            history_context = f"\nStudent's weak areas: {weak_areas}\nStrong areas: {strong_areas}"
        
        system_prompt = f"""You are an academic tutor helping a B-Tech {branch} student with their {task_type}.
{history_context}

Provide step-by-step guidance without giving direct answers. Focus on concept clarity and understanding.
Be encouraging and supportive."""
        
        # New SDK supports system instructions in config, but we can also use messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_description}
        ]
        
        return await self.chat_completion(messages, temperature=0.7)
    
    async def career_recommendation(
        self,
        branch: str,
        interests: List[str],
        career_goal: str,
        skills_analysis: Optional[Dict] = None
    ) -> Dict:
        """Generate career recommendations"""
        skills_context = ""
        if skills_analysis:
            skills_context = f"\nSkills from activities: {', '.join(skills_analysis.get('skills', []))}"
        
        system_prompt = f"""You are a career counselor for B-Tech students.
Analyze this student's profile:
- Branch: {branch}
- Interests: {', '.join(interests)}
- Career Goal: {career_goal}
{skills_context}

Provide 3-5 specific career path recommendations in JSON format:
{{
  "paths": [
    {{
      "domain": "Career domain name",
      "match_score": 85,
      "reasoning": "Why this suits the student",
      "required_skills": ["skill1", "skill2"],
      "roadmap_phases": [
        {{
          "phase": "Phase name",
          "duration": "3 months",
          "focus": "What to learn"
        }}
      ]
    }}
  ]
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate career recommendations for me."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.8, max_tokens=1000)
        
        # Parse JSON response
        parsed_result = self._extract_json(response)
        
        return {
            "recommendations": parsed_result.get("paths", []),
            "raw_text": response if "error" in parsed_result else None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def resume_content_generation(
        self,
        projects: List[Dict],
        skills: List[str],
        branch: str,
        target_domain: str
    ) -> Dict:
        """Generate resume bullet points"""
        projects_desc = "\n".join([f"- {p.get('title', 'Project')}: {p.get('description', '')}" for p in projects])
        
        system_prompt = f"""You are an expert resume writer specializing in {target_domain} roles for {branch} engineering students.

Student's projects:
{projects_desc}

Skills: {', '.join(skills)}

Generate professional, ATS-friendly bullet points for their projects.
Requirements:
- Start with strong action verbs
- Include quantifiable achievements where possible
- Use domain-specific keywords
- Keep each bullet concise (1-2 lines)

Provide 3-5 bullet points for each project."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate resume bullet points."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7, max_tokens=800)
        
        return {
            "generated_content": response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def ats_analysis(
        self,
        resume_text: str,
        job_description: Optional[str] = None
    ) -> Dict:
        """Analyze resume for ATS compatibility"""
        jd_context = ""
        if job_description:
            jd_context = f"\n\nTarget Job Description:\n{job_description}"
        
        system_prompt = f"""You are an ATS (Applicant Tracking System) analyzer.

Analyze this resume for ATS compatibility:
{resume_text}
{jd_context}

Provide:
1. ATS score (0-100)
2. Key missing keywords
3. Specific suggestions for improvement

Format as JSON:
{{
  "ats_score": 75,
  "keywords_found": ["keyword1", "keyword2"],
  "keywords_missing": ["keyword3", "keyword4"],
  "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Analyze my resume."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.5, max_tokens=600)
        
        parsed_result = self._extract_json(response)
        
        # Ensure correct types for Pydantic validation
        try:
            ats_score = int(parsed_result.get("ats_score", 0))
        except (ValueError, TypeError):
            ats_score = 0

        return {
            "ats_score": ats_score,
            "keywords_found": parsed_result.get("keywords_found") if isinstance(parsed_result.get("keywords_found"), list) else [],
            "keywords_missing": parsed_result.get("keywords_missing") if isinstance(parsed_result.get("keywords_missing"), list) else [],
            "suggestions": parsed_result.get("suggestions") if isinstance(parsed_result.get("suggestions"), list) else [],
            "match_details": parsed_result.get("match_details", {}),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Generate intelligent fallback responses when AI API is unavailable"""
        message_lower = user_message.lower()
        
        # Academic help patterns
        if any(word in message_lower for word in ['study', 'learn', 'understand', 'subject', 'exam', 'test', 'assignment', 'homework']):
            responses = [
                "Great question! When studying, I recommend the Feynman Technique: try explaining the concept in simple words as if teaching someone else. This helps identify gaps in your understanding. Also, break your study sessions into 25-minute focused blocks with 5-minute breaks (Pomodoro Technique). Would you like specific tips for any particular subject?",
                "Studying effectively is all about active recall and spaced repetition. Instead of just re-reading notes, try testing yourself frequently. Create flashcards, solve practice problems, and explain concepts aloud. Also, don't cram - spread your study sessions over days or weeks. What subject are you working on?",
                "Focus on understanding concepts rather than memorizing. Use multiple resources - videos, articles, practice problems. Study in a distraction-free environment, and teach what you learn to others. This reinforces your own understanding. Need help with a specific topic?"
            ]
            return random.choice(responses)
        
        # Motivation patterns
        elif any(word in message_lower for word in ['motivate', 'inspire', 'give up', 'fail', 'difficult', 'hard', 'cant', "can't", 'stressed', 'overwhelmed']):
            responses = [
                "I understand it feels overwhelming right now, but remember - every expert was once a beginner. Your struggles today are building the skills you'll use tomorrow. Break your goals into smaller, achievable tasks. Celebrate small wins. You're capable of more than you think! 💪",
                "Tough times don't last, but tough students do! It's okay to feel challenged - that's how we grow. Remember why you started this journey. Take breaks when needed, but don't give up. Every great engineer faced difficulties. What matters is persistence. You've got this!",
                "Feeling stuck is part of the learning process. Instead of saying 'I can't do this,' try 'I can't do this YET.' Every mistake is a lesson. Take a deep breath, break the problem into smaller parts, and tackle one piece at a time. Progress, not perfection!"
            ]
            return random.choice(responses)
        
        # Career/future patterns
        elif any(word in message_lower for word in ['career', 'job', 'future', 'work', 'placement', 'interview', 'company', 'salary']):
            responses = [
                "Great that you're thinking ahead! Focus on building strong fundamentals in your branch subjects first. Then, identify your interests and work on relevant projects. Contribute to open source, build a portfolio, and network with professionals. Internships are crucial - they give real-world experience. What field interests you most?",
                "Career success comes from continuous learning and practical experience. Start by identifying your strengths and interests. Work on projects that showcase your skills. Learn in-demand technologies. Practice coding/problem-solving regularly. Attend hackathons and workshops. Remember, your first job is just the beginning of a long journey!",
                "Planning your career is smart! Build technical skills through projects, contribute to GitHub, create a strong LinkedIn profile. Practice for technical interviews regularly. Soft skills matter too - communication, teamwork, problem-solving. Consider what type of work excites you and align your learning accordingly."
            ]
            return random.choice(responses)
        
        # Productivity/time management patterns
        elif any(word in message_lower for word in ['productive', 'time', 'manage', 'focus', 'concentrate', 'procrastinate', 'distract']):
            responses = [
                "Great question! Try the Pomodoro Technique: work in focused 25-minute sessions with 5-minute breaks. Use apps to block distracting websites during study time. Create a dedicated study space. Plan your day the night before. Prioritize tasks using the Eisenhower Matrix (urgent vs important). Most importantly, be consistent!",
                "Productivity tips that work: 1) Start with your hardest task (eat the frog). 2) Use time-blocking - assign specific hours to specific tasks. 3) Minimize multitasking. 4) Keep your phone away during study. 5) Take regular breaks. 6) Get enough sleep - tired minds aren't productive!",
                "Managing time effectively is a skill you can develop. Create a weekly schedule with dedicated study blocks. Use the 2-minute rule - if something takes less than 2 minutes, do it now. Batch similar tasks together. Track how you spend time for a week to identify time-wasters. Remember: discipline beats motivation!"
            ]
            return random.choice(responses)
        
        # Skills/learning patterns  
        elif any(word in message_lower for word in ['skill', 'learn','course', 'tutorial', 'practice', 'improve', 'better']):
            responses = [
                "Building skills requires consistent practice! Focus on project-based learning - it's more effective than just watching tutorials. Start with fundamentals, then build real projects. Use platforms like GitHub to showcase your work. Learn by teaching others. Set specific, measurable goals. What skill are you working on?",
                "Great that you want to improve! Here's my advice: 1) Learn by doing - build projects, not just tutorials. 2) Join coding communities. 3) Read documentation and source code. 4) Practice daily, even if just 30 minutes. 5) Get feedback on your work. 6) Don't try to learn everything - go deep in a few areas first.",
                "Skill development is a journey! Start with free resources like NPTEL, Coursera, and YouTube. But don't just consume - create! Build projects that solve real problems. Contribute to open source. Participate in hackathons. Learn from failures. The best learning happens when you're building something challenging."
            ]
            return random.choice(responses)
        
        # General greeting patterns
        elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']):
            responses = [
                "Hello! I'm here to help you with your academic journey, career planning, motivation, or any challenges you're facing. What's on your mind today?",
                "Hey there! Great to see you! Whether you need study tips, career advice, motivation, or just someone to talk to, I'm here. How can I support you today?",
                "Hi! Welcome! I'm your AI mentor, ready to help with academics, career guidance, productivity tips, or anything else you need. What would you like to discuss?"
            ]
            return random.choice(responses)
        
        # Thank you patterns
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            responses = [
                "You're very welcome! I'm always here to help. Keep up the great work, and don't hesitate to reach out anytime you need guidance or support!",
                "Happy to help! Remember, asking questions and seeking guidance is a sign of strength, not weakness. Keep pushing forward - you're doing great!",
                "My pleasure! Your success is what matters. Keep learning, keep growing, and keep believing in yourself. I'm here whenever you need me!"
            ]
            return random.choice(responses)
        
        # Default response
        else:
            responses = [
                "That's an interesting question! As a B-Tech student, remember that challenges are opportunities to grow. Whether it's about academics, career planning, or personal development, I'm here to guide you. Could you tell me more about what you're working on or struggling with?",
                "I'm here to support you! Whether you need help with studying, career planning, managing stress, or improving productivity, feel free to ask. What specific aspect would you like to discuss?",
                "Thanks for sharing! My goal is to help you succeed in your engineering journey. I can assist with academic guidance, career advice, motivation, study strategies, and more. What would be most helpful for you right now?"
            ]
            return random.choice(responses)
    
    async def mentor_chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """AI mentor chat using Gemini"""
        try:
            system_prompt = """You are a friendly and supportive AI mentor for B-Tech students.
You provide:
- Academic guidance and study tips
- Motivation and encouragement
- Career advice
- Stress management strategies
- Productivity tips

Be warm, understanding, and encouraging. Keep responses concise but helpful (2-3 paragraphs max)."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Last 5 messages for context
            
            messages.append({"role": "user", "content": user_message})
            
            return await self.chat_completion(messages, temperature=0.8)
        except Exception as e:
            print(f"Mentor chat error: {e}")
            return self._get_fallback_response(user_message)
    
    async def generate_motivation(self) -> str:
        """Generate motivational message using Gemini"""
        try:
            if self.client and settings.gemini_api_key:
                system_prompt = """You are a motivational coach for engineering students.
Generate a short, impactful motivational message (2-3 sentences) to inspire students.
Focus on perseverance, growth, and achievement."""
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Give me a motivational message."}
                ]
                
                return await self.chat_completion(messages, temperature=0.9, max_tokens=150)
            else:
                # Fallback motivational quotes if client is not initialized
                quotes = [
                    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                    "The difference between who you are and who you want to be is what you do.",
                    "Engineering is not about having all the answers - it's about having the persistence to find them."
                ]
                return random.choice(quotes)

        except Exception as e:
            print(f"Motivation generation error: {e}")
            return "Believe in yourself and your abilities. Every challenge you face is making you stronger and more capable. Keep pushing forward!"
    
    async def detailed_career_matching(
        self,
        student_context: str,
        available_domains: List[Dict]
    ) -> Dict:
        """
        Match student profile to career domains with detailed reasoning
        Returns top 5 matching domains with match scores
        """
        # Limit to representative domains to avoid token limits
        domain_summaries = []
        for domain in available_domains[:20]:  # Limit sample
            domain_summaries.append({
                "id": domain['domain_id'],
                "title": domain['title'],
                "category": domain['category'],
                "key_skills": [s['name'] for s in domain['key_skills'][:5]],
                "description": domain['description'][:150]
            })
        
        system_prompt = f"""You are an expert career counselor for engineering students.

{student_context}

Available career domains:
{domain_summaries}

Analyze the student's profile and recommend the top 5 best-matching career domains.
For each recommendation, provide:
1. Match score (0-100)
2. Reasoning (why it's a good fit)
3. One key next step

Return as JSON:
{{
  "matches": [
    {{
      "domain_id": "string",
      "domain_title": "string",
      "match_score": 85,
      "reasoning": "Brief explanation why this matches",
      "next_step": "Immediate action student should take"
    }}
  ]
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Analyze my profile and recommend career paths."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7, max_tokens=800)
        
        # Parse JSON response
        parsed_result = self._extract_json(response)
        
        # Ensure matches key exists and is a list
        if "matches" not in parsed_result or not isinstance(parsed_result["matches"], list):
            # Fallback for Demo Mode or API Failure
            print("AI Service: Using fallback mode for career recommendations")
            
            # Select 3 random domains
            selected_domains = random.sample(available_domains, min(3, len(available_domains)))
            matches = []
            
            for domain in selected_domains:
                matches.append({
                    "domain_id": domain['domain_id'],
                    "domain_title": domain['title'],
                    "match_score": random.randint(75, 95),
                    "reasoning": f"Based on your profile, {domain['title']} is a strong match due to alignment with engineering fundamentals.",
                    "next_step": "Explore the industry roadmap for this domain."
                })
            
            parsed_result = {"matches": matches}
             
        return parsed_result
    
    async def ats_analysis_with_domain(
        self,
        resume_text: str,
        target_domain: Dict,
        job_description: Optional[str] = None
    ) -> Dict:
        """
        Analyze resume for ATS compatibility with domain-specific keyword checking
        """
        domain_keywords = target_domain.get('keywords_for_ats', [])
        domain_skills = [s['name'] for s in target_domain.get('key_skills', [])]
        
        jd_context = ""
        if job_description:
            jd_context = f"\n\nTarget Job Description:\n{job_description}"
        
        system_prompt = f"""You are an ATS (Applicant Tracking System) analyzer for {target_domain['title']} roles.

Domain-Critical Keywords: {', '.join(domain_keywords)}
Required Skills: {', '.join(domain_skills)}

Analyze this resume:
{resume_text}
{jd_context}

Provide:
1. ATS score (0-100) based on keyword presence
2. Keywords found vs. missing (from domain-critical list)
3. Specific suggestions to improve ATS score

Format as JSON:
{{
  "ats_score": 75,
  "keywords_found": ["keyword1", "keyword2"],
  "keywords_missing": ["keyword3", "keyword4"],
  "suggestions": ["suggestion1", "suggestion2"],
  "domain_match": "How well resume targets this domain"
}}"""
        
        response = await self.chat_completion(messages, temperature=0.5, max_tokens=600)
        
        parsed_result = self._extract_json(response)

        
        try:
            ats_score = int(parsed_result.get("ats_score", 0))
        except (ValueError, TypeError):
            ats_score = 0

        return {
            "ats_score": ats_score,
            "keywords_found": parsed_result.get("keywords_found") if isinstance(parsed_result.get("keywords_found"), list) else [],
            "keywords_missing": parsed_result.get("keywords_missing") if isinstance(parsed_result.get("keywords_missing"), list) else [],
            "suggestions": parsed_result.get("suggestions") if isinstance(parsed_result.get("suggestions"), list) else [],
            "domain_match": parsed_result.get("domain_match", "Good potential"),
            "target_domain": target_domain['title'],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    async def generate_skill_roadmap(
        self,
        target_domain: Dict,
        current_skills: List[str],
        timeline_months: int = 12
    ) -> Dict:
        """
        Generate personalized learning roadmap for target domain
        """
        skill_gap = []
        for req_skill in target_domain.get('key_skills', [])[:10]:
            skill_name = req_skill['name']
            if not any(skill_name.lower() in cs.lower() for cs in current_skills):
                skill_gap.append(f"{skill_name} ({req_skill['level']})")
        
        system_prompt = f"""You are a learning path designer for {target_domain['title']}.

Student's current skills: {', '.join(current_skills) if current_skills else 'Beginner'}
Skills needed: {', '.join(skill_gap) if skill_gap else 'Mostly covered'}
Timeline: {timeline_months} months

Create a month-by-month learning plan with:
- What to learn each month
- Recommended resources (courses, books, projects)
- Milestones to achieve

Be specific and actionable. Format as structured text."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a {timeline_months}-month roadmap for me."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7, max_tokens=1000)
        
        return {
            "roadmap": response,
            "domain": target_domain['title'],
            "duration_months": timeline_months
        }
    
    async def interview_preparation(
        self,
        target_domain: Dict,
        experience_level: str = "fresher"
    ) -> Dict:
        """
        Generate domain-specific interview preparation guidance
        """
        key_skills = [s['name'] for s in target_domain.get('key_skills', [])[:8]]
        
        system_prompt = f"""You are an interview coach for {target_domain['title']} positions.

Experience Level: {experience_level}
Key Technical Areas: {', '.join(key_skills)}

Provide interview preparation guidance:
1. 5 most common technical questions for this role
2. 3 key concepts to review
3. 2 behavioral question tips specific to this domain

Keep it concise and actionable."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Help me prepare for interviews."}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7, max_tokens=800)
        
        return {
            "preparation_guide": response,
            "domain": target_domain['title'],
            "level": experience_level
        }

    async def internship_review(
        self,
        internship_data: Dict,
        student_profile: Dict
    ) -> Dict:
        """
        Generate personalized tips for an internship application
        """
        company = internship_data.get('company', 'this company')
        role = internship_data.get('role', 'this role')
        domain = internship_data.get('domain', 'this domain')
        
        interests = ", ".join(student_profile.get('interests', []))
        branch = student_profile.get('branch', 'Engineering')
        
        system_prompt = f"""You are an expert career mentor helping a B-Tech {branch} student with their internship application at {company} for a {role} role ({domain}).
        
        Student Interests: {interests}
        
        Provide 3-4 highly specific, actionable tips to increase their chance of success:
        1. How to tailor their resume for this specific company.
        2. Key technical skills to highlight or brush up on.
        3. A domain-specific tip (e.g., for Finance vs. Web Dev).
        4. A personalized networking tip.
        
        Be professionally encouraging and very specific to the company/domain mentioned."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"How can I improve my chances at {company} for the {role} role?"}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7, max_tokens=600)
        
        return {
            "review": response,
            "company": company,
            "role": role,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Singleton instance
ai_service = AIService()

