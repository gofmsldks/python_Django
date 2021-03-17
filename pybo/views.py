from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm


def index(requeset):

    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}

    return render(requeset, 'pybo/question_list.html', context)

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):

    question = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = AnswerForm() # 사실상 필요없는 부분, question_create 와는 달리 초기 진입과정이 필요없음.

    context = {'question': question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() # get 일때 (처음 진입할때 form을 선언해 놓아야 함으로 필요)

    context = {'form':form}
    return render(request, 'pybo/question_form.html', context) # 코드를 최적화 해놔서 처음 보면 헷갈릴 수 있음
    # 전체적으로 html에서 질문 내용을 입력하고 POST 형식으로 보내고 받은 데이터를 QuestionForm에다 넣고 인스턴스 형성
    # 만약 유효하지 않으면 form에다 에러 메시지 넣고 form을 다시 render
    # 근데 여기에서 질문등록 버튼을 누르고 처음 진입을 해야하는 상황에서 form이 정의 되지 않았으므로 else에 form = QuestionForm()을 해줌.

'''
제너릭뷰
class IndexView(generic.ListView):
    """
    pybo 목록 출력
    """
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


class DetailView(generic.DetailView):
    """
    pybo 내용 출력
    """
    model = Question
    
'''

'''

[Answer 모델로 Answer 모델 데이터 저장하는 예]

question = get_object_or_404(Question, pk=question_id)
answer = Answer(question=question, content=request.POST.get('content'), create_
date=timezone.now())
answer.save()


'''