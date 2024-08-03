from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Topic, Reply
from .forms import SignUpForm, TopicForm, ReplyForm

class TopicListView(ListView):
    model = Topic
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 5

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(topic=self.object).order_by('created_at')
        context['form'] = ReplyForm()
        return context

    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect('topic_detail', pk=topic.pk)
        return self.get(request, *args, **kwargs)

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'create_topic.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'edit_topic.html'

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()
        if not topic.can_edit_or_delete(request.user):
            raise PermissionDenied("У вас нет прав для редактирования этой темы.")
        return super().dispatch(request, *args, **kwargs)

class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'confirm_delete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()
        if not topic.can_edit_or_delete(request.user):
            raise PermissionDenied("У вас нет прав для удаления этой темы.")
        return super().dispatch(request, *args, **kwargs)

class ReplyUpdateView(LoginRequiredMixin, UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'edit_reply.html'

    def dispatch(self, request, *args, **kwargs):
        reply = self.get_object()
        if not reply.can_edit_or_delete(request.user):
            raise PermissionDenied("У вас нет прав для редактирования этого ответа.")
        return super().dispatch(request, *args, **kwargs)

class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return redirect('topic_detail', pk=self.object.topic.pk)

    def dispatch(self, request, *args, **kwargs):
        reply = self.get_object()
        if not reply.can_edit_or_delete(request.user):
            raise PermissionDenied("У вас нет прав для удаления этого ответа.")
        return super().dispatch(request, *args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(user=user, avatar=avatar) if avatar else Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    topics = Topic.objects.filter(author=user).order_by('-created_at')
    reply_count = Reply.objects.filter(author=user).count()
    profile = get_object_or_404(Profile, user=user)

    context = {
        'user': user,
        'topics': topics,
        'reply_count': reply_count,
        'profile': profile,
    }
    return render(request, 'profile.html', context)
