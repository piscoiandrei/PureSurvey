from django.shortcuts import render, redirect
from .models import *
from django.db.models import Avg
import logging

# Create your views here.
logger = logging.getLogger(__name__)


def home(request):
    logger.debug("Entering 'home' view")

    surveys = Survey.objects.all()

    avg_list = list()

    for s in surveys:
        temp = s.rating_set.aggregate(Avg('score'))
        if temp['score__avg'] is not None:
            t = round(temp['score__avg'], 2)
            avg_list.append(t)
        else:
            avg_list.append(0.00)

    context = {
        'zipped': zip(surveys, avg_list)
    }

    logger.debug("Returning from 'home' view")
    return render(request, 'surveys/home.html', context)


def survey(request, pk):
    logger.debug("Entered 'survey' view")

    current_survey = Survey.objects.get(id=pk)
    context = {
        'survey': current_survey,
    }

    if request.method == "POST":
        logger.info(f"POST REQUEST {request.POST}")
        for key in request.POST:
            if 'answer' in str(key):
                value = request.POST[key]
                # format : 'question.id-answer.id'
                indices = value.split('-')

                question = Question.objects.get(pk=int(indices[0]))
                answer = Answer.objects.get(pk=int(indices[1]))

                logger.info(f'Question : {question.text} #{indices[0]} '
                            f'with Answer : {answer.text} #{indices[1]}')

                result = Results(survey=current_survey, question=question,
                                 answer=answer)
                result.save()
                logger.debug("Saving the results")

        rating_score = request.POST['rating_value']
        rating = Rating(score=rating_score, survey=current_survey)
        logger.info(f"Rating {rating}")
        rating.save()
        logger.debug("Saving the rating")

        logger.debug("Redirecting from 'survey' view (POST)")
        return redirect('/')
    else:
        logger.info(f"Context: {current_survey}")
        logger.debug("Returning from 'survey' view")
        return render(request, 'surveys/survey.html', context)


def results(request, pk):
    logger.debug("Entered 'results' view")

    current_survey = Survey.objects.get(pk=pk)
    questions = Question.objects.filter(survey=current_survey)
    pack = list()

    for q in questions:
        all_answers = q.answer_set.all()
        percentages = list()
        # this will return all the entries in Results for this specific question
        total_answers_selected = Results.objects.filter(question=q).count()

        for answer in all_answers:
            times_selected = Results.objects.filter(answer=answer).count()
            if times_selected > 0:
                p = round((times_selected / total_answers_selected) * 100, 2)
            else:
                p = 0
            percentages.append(p)

        t = list()
        t.append(q)
        t.append(percentages)
        pack.append(t)

    context = {
        'pack': pack,
        'survey': current_survey,
    }

    logger.info(f"Context:'\n' {current_survey} '\n' {pack} '\n' End Context")
    logger.debug("Returning from 'results' view")
    return render(request, 'surveys/results.html', context)
