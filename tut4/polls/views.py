from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

# def detail(request, question_id):
#     try:
#         q = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404('Question does not exist')
#
#     #short version of the try and except:
#     # q = get_object_or_404(Question, pk=question_id)
#     # use get_list_or_404 in case of filtering instead of 'get'-ing
#
#     return render(request, 'polls/detail.html', {
#         'question': q,
#     })

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {
#         'question': question,
#     })

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
       return render(request, 'polls/detail.html', {
           'question': p,
           'error_message': 'Did not select a choice.',
       })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=[p.id]))
