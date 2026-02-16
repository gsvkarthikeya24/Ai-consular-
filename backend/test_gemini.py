"""
Test script for Gemini API integration
Run this to verify your Gemini API key is working correctly
"""
import asyncio
import sys
from app.services.ai_service import ai_service

async def test_gemini():
    """Test Gemini API integration"""
    
    print("Testing Gemini API Integration for AI Counselor")
    print("=" * 60)
    print()
    
    # Test 1: Simple chat completion
    print("Test 1: Simple Chat Completion")
    print("-" * 60)
    try:
        response = await ai_service.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Say hello and confirm you're working correctly!"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        print(f"Response: {response}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 2: AI Mentor Chat
    print("Test 2: AI Mentor Chat (Career Guidance)")
    print("-" * 60)
    try:
        mentor_response = await ai_service.mentor_chat(
            user_message="I need help preparing for my Data Structures exam. What should I focus on?"
        )
        print(f"Mentor Response: {mentor_response}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 3: Career Recommendation
    print("Test 3: Career Recommendation")
    print("-" * 60)
    try:
        career_rec = await ai_service.career_recommendation(
            branch="Computer Science",
            interests=["AI", "Machine Learning", "Data Science"],
            career_goal="AI/ML Engineer"
        )
        print(f"Career Recommendations Generated:")
        if 'recommendations' in career_rec:
            for idx, path in enumerate(career_rec['recommendations'][:2], 1):
                print(f"   {idx}. {path.get('domain', 'N/A')} (Match: {path.get('match_score', 0)}%)")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Test 4: Motivational Message
    print("Test 4: Motivational Message Generation")
    print("-" * 60)
    try:
        motivation = await ai_service.generate_motivation()
        print(f"Motivation: {motivation}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    
    # Test 5: Detailed Career Matching
    print("Test 5: Detailed Career Matching")
    print("-" * 60)
    try:
        # Mock available domains for testing
        mock_domains = [
            {
                "domain_id": "software-engineering",
                "title": "Software Engineering",
                "category": "IT",
                "key_skills": [{"name": "Python", "level": "High"}, {"name": "System Design", "level": "Medium"}],
                "description": "Building software solutions."
            },
            {
                "domain_id": "data-science",
                "title": "Data Science",
                "category": "IT",
                "key_skills": [{"name": "Python", "level": "High"}, {"name": "Statistics", "level": "High"}],
                "description": "Analyzing data to find patterns."
            }
        ]
        
        student_context = """
        Student Profile:
        - Branch: Computer Science
        - Interests: coding, algorithms, problem solving
        - Completed Tasks: 5
        - CGPA: 8.5
        """
        
        detailed_match = await ai_service.detailed_career_matching(
            student_context=student_context,
            available_domains=mock_domains
        )
        print(f"Detailed Matching Response Received")
        if 'ai_response' in detailed_match:
            print(f"   Response length: {len(detailed_match['ai_response'])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # Test 6: Internship Review
    print("Test 6: Internship Review")
    print("-" * 60)
    try:
        mock_internship = {
            "company": "Tech Corp",
            "role": "SDE Intern",
            "domain": "Software Engineering"
        }
        
        mock_profile = {
            "branch": "Computer Science",
            "interests": ["Web Development", "Cloud Computing"]
        }
        
        review = await ai_service.internship_review(
            internship_data=mock_internship,
            student_profile=mock_profile
        )
        print(f"Internship Review Received")
        if 'review' in review:
            print(f"   Review length: {len(review['review'])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    
    # Test 7: Resume Content Generation
    print("Test 7: Resume Content Generation")
    print("-" * 60)
    try:
        mock_projects = [
            {"title": "E-commerce App", "description": "Built a shop using React"}
        ]
        mock_skills = ["React", "Node.js"]
        
        resume_content = await ai_service.resume_content_generation(
            projects=mock_projects,
            skills=mock_skills,
            branch="Computer Science",
            target_domain="Web Development"
        )
        print(f"Resume Content Generated")
        if 'generated_content' in resume_content:
            print(f"   Content length: {len(resume_content['generated_content'])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # Test 8: ATS Analysis
    print("Test 8: ATS Analysis")
    print("-" * 60)
    try:
        mock_resume = "Experienced Web Developer with 2 years of experience in React and Node.js."
        mock_jd = "Looking for a Web Developer with React, Node.js, and Docker skills."
        
        ats_result = await ai_service.ats_analysis(
            resume_text=mock_resume,
            job_description=mock_jd
        )
        print(f"ATS Analysis Received")
        print(f"   Score: {ats_result.get('ats_score', 'N/A')}")
        print(f"   Missing Keywords: {ats_result.get('keywords_missing', [])}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    print("=" * 60)
    print("All tests completed!")
    print()
    print("Note: If you see demo/fallback responses, make sure:")
    print("1. Your GEMINI_API_KEY is set in the .env file")
    print("2. LLM_PROVIDER=gemini in the .env file")
    print("3. You've restarted the backend server")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_gemini())
