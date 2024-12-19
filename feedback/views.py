from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import FeedbackForm

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/')  # Переход на страницу успеха
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form})
