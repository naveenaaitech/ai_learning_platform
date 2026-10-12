
from django.db import transaction

from pydantic import ValidationError

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .schemas import InterviewRequest, InterviewResponse
from .services.groq_service import generate_interview_questions
from .models import Question, Interview, InterviewQuestion


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):

    return Response({
        "username": request.user.username,
        "user_id": request.user.id
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_questions(request):


    # Step 1: Validate the student's request
    try:
        interview_request = InterviewRequest.model_validate(
            request.data
        )
    except ValidationError as e:
        return Response({
            "success": False,
            "error": "Invalid request",
            "details": e.errors()
        }, status=400)


    # Step 2: Generate questions using Groq
    try:
        result = generate_interview_questions(
            interview_request.technology,
            interview_request.difficulty,
            interview_request.count
        )


        # Step 3: Validate the AI response
        validated_result = InterviewResponse.model_validate(result)


    except ValidationError as e:
        return Response({
            "success": False,
            "error": "Invalid AI response",
            "details": e.errors()
        }, status=502)


    except Exception:
        return Response({
            "success": False,
            "error": "Unable to generate questions. Please try again."
        }, status=502)


    # Step 4: Save the interview and questions together
    try:
        with transaction.atomic():


            interview = Interview.objects.create(
                user=request.user,
                technology=validated_result.technology,
                difficulty=validated_result.difficulty,
                total_questions=len(validated_result.questions)
            )


            saved_questions = []


            for index, item in enumerate(
                validated_result.questions,
                start=1
            ):
                question = Question.objects.create(
                    technology=validated_result.technology,
                    question=item.question,
                    topic=item.topic,
                    difficulty=item.difficulty
                )


                InterviewQuestion.objects.create(
                    interview=interview,
                    question=question,
                    question_order=index
                )


                saved_questions.append({
                    "question_id": question.id,
                    "question": item.question,
                    "topic": item.topic,
                    "difficulty": item.difficulty,
                    "question_order": index
                })


        # Step 5: Return the saved interview details
        return Response({
            "success": True,
            "message": "Interview created successfully",
            "interview_id": interview.id,
            "technology": interview.technology,
            "difficulty": interview.difficulty,
            "total_questions": interview.total_questions,
            "questions": saved_questions
        }, status=201)


    except Exception:
        return Response({
            "success": False,
            "error": "Unable to save the interview. Please try again."
        }, status=500)
