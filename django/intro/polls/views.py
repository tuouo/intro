from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, django. Here's the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question {}.".format(question_id))

def results(request, question_id):
    response = "You're looking at the result of question {}."
    return HttpResponse(response.format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))

