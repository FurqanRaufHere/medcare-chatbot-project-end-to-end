
def create_structured_medical_response(
    topic,
    greeting,
    overview,
    key_points,
    details,
    recommendations,
    important_notes,
    next_steps,
    closing=None
):
    """
    Generate a structured medical response with consistent formatting
    
    Args:
        topic (str): Main medical topic
        greeting (str): Personalized greeting
        overview (str): Brief overview of the topic
        key_points (list): List of key information points
        details (str): Detailed medical information
        recommendations (list): List of recommendations
        important_notes (str): Warnings and special considerations
        next_steps (list): Suggested actions
        closing (str, optional): Custom closing message. If None, uses default.
        
    Returns:
        str: Formatted markdown response
    """
    
    # Format key points as bullet list
    key_points_formatted = "\n".join([f"- {point}" for point in key_points])
    
    # Format recommendations as bullet list
    recommendations_formatted = "\n".join([f"- {rec}" for rec in recommendations])
    
    # Format next steps as numbered list
    next_steps_formatted = "\n".join([f"{i+1}. {step}" for i, step in enumerate(next_steps)])
    
    # Default closing if not provided
    if closing is None:
        closing = f"Remember, this information is for educational purposes only. Please consult with your healthcare provider for personalized medical advice regarding {topic}."
    
    # Create the full response using markdown formatting
    response = f"""# {topic}

## Greeting
{greeting}

## Topic Overview
{overview}

## Key Information
{key_points_formatted}

## Medical Details
{details}

## Recommendations
{recommendations_formatted}

## Important Notes
{important_notes}

## Next Steps
{next_steps_formatted}

## Closing
{closing}
"""
    return response


def format_llm_response(llm_response):
    """
    Ensure LLM responses conform to our structured format
    
    If the LLM response doesn't follow the expected format,
    this function will try to extract relevant information
    and reformat it according to our template.
    
    Args:
        llm_response (str): The response from the LLM
        
    Returns:
        str: Properly formatted response
    """
    # This is a placeholder for more advanced formatting logic
    # In a real implementation, you might:
    # 1. Check if all required sections are present
    # 2. Add missing sections with default content
    # 3. Reformat sections that don't follow conventions
    
    # For now, just return the original response
    return llm_response


# Example medical topic templates that can be used directly

def get_atkins_diet_template():
    """Returns a pre-formatted template for Atkins Diet questions"""
    return create_structured_medical_response(
        topic="Atkins Diet",
        greeting="Hello! Thank you for your question about the Atkins diet.",
        overview="The Atkins diet is a low-carbohydrate eating plan designed for weight loss that emphasizes protein and fats while restricting carbohydrates.",
        key_points=[
            "The diet works by shifting your metabolism from burning carbs to burning stored body fat",
            "It consists of four phases with gradually increasing carbohydrate intake",
            "It may lead to significant short-term weight loss but sustainability varies"
        ],
        details="""The Atkins diet operates on the principle of ketosis, where your body burns fat for fuel when carbohydrate intake is limited. The standard program includes:

**Phase 1 (Induction)**: 20g net carbs daily for 2 weeks
**Phase 2 (Balancing)**: Gradually add more nuts, low-carb vegetables
**Phase 3 (Fine-Tuning)**: Introduce more carbs as you approach weight goal
**Phase 4 (Maintenance)**: Sustainable long-term carb intake""",
        recommendations=[
            "Consult with your healthcare provider before starting, especially if you have existing health conditions",
            "Ensure adequate water intake while following the diet",
            "Focus on healthy fats and quality proteins rather than processed foods"
        ],
        important_notes="The Atkins diet may not be suitable for everyone. People with kidney disease, pregnant or breastfeeding women, and those taking certain medications should exercise caution. Side effects may include headache, dizziness, weakness, and constipation, particularly during the early phases.",
        next_steps=[
            "Speaking with your healthcare provider",
            "Planning your meals in advance",
            "Monitoring your progress and how you feel"
        ]
    )


def get_medication_template():
    """Returns a pre-formatted template for medication administration questions"""
    return create_structured_medical_response(
        topic="Medication Administration",
        greeting="Hello! I understand you have questions about medication administration.",
        overview="Proper medication administration is critical for effective treatment and patient safety, involving the right medication, dose, route, time, and patient.",
        key_points=[
            "Always verify the '5 Rights': right patient, medication, dose, route, and time",
            "Be aware of potential drug interactions and contraindications",
            "Proper documentation is essential for continuity of care"
        ],
        details="""Medication administration requires attention to detail and adherence to established protocols. Different routes of administration include:

**Oral**: Taken by mouth, easiest and most common route
**Intravenous (IV)**: Delivered directly into veins, provides rapid effect
**Intramuscular (IM)**: Injected into muscle tissue, slower absorption than IV
**Subcutaneous**: Injected into tissue between skin and muscle
**Topical**: Applied to skin or mucous membranes""",
        recommendations=[
            "Double-check all medication orders before administration",
            "Understand the purpose, normal dosage, and side effects of medications you administer",
            "Follow proper hand hygiene and aseptic technique",
            "Report adverse reactions immediately"
        ],
        important_notes="Medication errors can have serious or fatal consequences. Never administer a medication if you're uncertain about any aspect of the order. Always consult appropriate references or healthcare professionals when in doubt.",
        next_steps=[
            "Review your facility's medication administration policies",
            "Ensure proper training for specific administration techniques",
            "Maintain current knowledge about medications you frequently administer",
            "Report any near-misses or errors through proper channels"
        ]
    )