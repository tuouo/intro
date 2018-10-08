from django.http import HttpResponse
from django.template import loader

from polls.models import Question


def index(request):
    template = loader.get_template('polls/index.html')
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    return HttpResponse("You're looking at question {}.".format(question_id))

def results(request, question_id):
    response = "You're looking at the result of question {}."
    return HttpResponse(response.format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))

