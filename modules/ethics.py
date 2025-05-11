import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def grade_ethics_answers(answers):
    """
    Grade ethics answers based on insurance industry standards

    Parameters:
    -----------
    answers : dict
        Dictionary of answers with variable names as keys and boolean values

    Returns:
    --------
    dict
        Dictionary with score, feedback, and other grading information
    """
    # These are the "model answers" based on general insurance standards
    model_answers = {
        'drake_rating': False,  # Not appropriate to use Drake listening as a rating factor
        'kendrick_rating': False,  # Not appropriate to use Kendrick listening as a rating factor
        'age_rating': True,  # Age is a commonly used rating factor
        'vehicle_rating': True,  # Vehicle type is a commonly used rating factor
        'religion_rating': False,  # Religion is not appropriate
        'race_rating': False,  # Race/ethnicity is not appropriate
        'experience_rating': True,  # Years of driving experience is a valid rating factor
        'multiproduct_rating': True,  # Multi-product discount is a common and accepted practice
        'speeding_rating': True,  # Speeding convictions are directly related to driving risk
        'driving_rating': True,  # Driving history is universally used
    }

    # Count correct answers
    correct = 0
    total = len(model_answers)

    # Track incorrect answers
    incorrect = []

    for var, model_answer in model_answers.items():
        user_answer = answers.get(var, False)
        if user_answer == model_answer:
            correct += 1
        else:
            # Format the variable name for displaying
            var_formatted = var.replace('_rating', '').replace('_', ' ').title()
            incorrect.append(var_formatted)

    # Calculate score out of 10
    score = round(correct / total * 10)

    # Generate feedback based on score
    if score >= 9:
        feedback = "Excellent! You have a strong understanding of ethical rating considerations."
    elif score >= 7:
        feedback = "Good work! You understand most key ethical rating principles."
    elif score >= 5:
        feedback = "You're on the right track. Consider how these relate to risk vs. discrimination."
    else:
        feedback = "Review how insurers balance predictive value with social fairness."

    # Add specific feedback if there were incorrect answers
    if incorrect:
        feedback += f" Reconsider: {', '.join(incorrect)}."

    return {
        'score': score,
        'feedback': feedback,
        'correct': correct,
        'total': total,
        'incorrect': incorrect
    }


def get_ethics_questions():
    """
    Returns a list of ethics questions for the UI

    Returns:
    --------
    list
        List of dictionaries with question information
    """
    return [
        {
            'id': 'drake_rating',
            'title': 'Drake Listeners',
            'ethical': False
        },
        {
            'id': 'kendrick_rating',
            'title': 'Kendrick Listeners',
            'ethical': False
        },
        {
            'id': 'age_rating',
            'title': 'Driver Age',
            'ethical': True
        },
        {
            'id': 'vehicle_rating',
            'title': 'Vehicle Type',
            'ethical': True
        },
        {
            'id': 'religion_rating',
            'title': 'Religion',
            'ethical': False
        },
        {
            'id': 'race_rating',
            'title': 'Race/Ethnicity',
            'ethical': False
        },
        {
            'id': 'experience_rating',
            'title': 'Years of Driving Experience',
            'ethical': True
        },
        {
            'id': 'multiproduct_rating',
            'title': 'Multi-Product Discount',
            'ethical': True
        },
        {
            'id': 'speeding_rating',
            'title': 'Speeding Convictions',
            'ethical': True
        },
        {
            'id': 'driving_rating',
            'title': 'Driving History',
            'ethical': True
        }
    ]