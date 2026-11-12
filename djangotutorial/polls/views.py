from django.db.models import F, Max, Sum
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import VoteForm, QuestionAddForm
from polls.utils import minimax

from .models import Question, Choice

class AllView(generic.ListView):
 model = Question
 template_name = 'polls/all.html'



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]



class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



# fusion et modification de la classe DetailView et
# de la méthode vote en la seule méthode vote
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices_form = [(choice.id, choice.choice_text)
                    for choice in question.choice_set.all()]
    if request.method == 'POST' :
        form = VoteForm(question.question_text, choices_form, request.POST)
        if form.is_valid():
            selected_choice = question.choice_set.get(pk= \
                                    form.cleaned_data['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    else:
        form = VoteForm(question.question_text, choices_form)
    return render(request, "polls/detail.html", {"form": form, "question": question})



class AllView(generic.ListView):
    model = Question
    template_name = "polls/all.html"
    context_object_name = "question_list"



class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context['question']
        choices = question.get_choices()
        context['choices'] = choices
        return context



def statistics(request):
    nbr_sondages = Question.objects.count()
    nbr_choix = Choice.objects.count()
    nbr_votes = \
    Choice.objects.aggregate(somme=Sum('votes'))['somme']
    moyenne_par_sondage = nbr_votes / nbr_sondages
    (question_la_moins_populaire, question_la_plus_populaire) = \
    minimax()
    id_derniere_question = \
    Question.objects.aggregate(max=Max('id'))['max']
    derniere_question = \
    Question.objects.get(pk=id_derniere_question)
    return render(request, 'polls/statistics.html', {
    'nbr_sondages': nbr_sondages,
    'nbr_choix': nbr_choix,
    'nbr_votes': nbr_votes,
    'moyenne_par_sondage': moyenne_par_sondage,
    'question_la_plus_populaire': question_la_plus_populaire,
    'question_la_moins_populaire':
    question_la_moins_populaire,
    'derniere_question': derniere_question,
    })



NB_MAX_CHOIX = 5
# fusion et modification des méthodes add et confirm_add
# en la seule méthode add
def add(request):
    if request.method == 'POST':
        form = QuestionAddForm(request.POST)
        if form.is_valid():
            question = \
            Question(question_text=\
                    form.cleaned_data['question_text'],
                    pub_date=timezone.now())
            question.save()
            # on traite à présent les champs de choix remplis
            # (on s'arrête au premier vide)

            for no_choix in range(NB_MAX_CHOIX):
                nom_champ = 'choice_{}'.format(no_choix)
                choice_text = form.cleaned_data[nom_champ].strip()
                if choice_text:
                    choice = Choice(question=question,
                                    choice_text=choice_text)
                    choice.save()
                else:
                    break
            return render(request, 'polls/confirm_add.html')
    else:
        form = QuestionAddForm()

    return render(request, 'polls/add.html', {'form': form})
