from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Question
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(requeset):

    '''pybo 목록 출력'''

    # 입력 파라미터
    page = requeset.GET.get('page', '1') # 페이지 ?page = 1 주소 표현해주는 함수

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}

    return render(requeset, 'pybo/question_list.html', context)

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
# 로그인이 안되어져있으면 로그인 화면으로 이동
# request.user가 User 객체가 아닌 AnonymousUser 객체먄 오류 발생하므로 해당 어노태이션 필요
# 어노테이션 사용하면 로그아웃 상태에서 '질문 등록하기'를 눌러 로그인 화면으로 전환된 상태에서 웹 브라우저 주소창의 URL을 보면 next 파라미터가 있음.
# 이는 로그인 성공 후 next 파라미터에 있는 URL로 페이지를 이동해야 한다는 의미
# ****로그인 html 탬플릿에 <input type="hidden" name="next" value="{{ next }}"> 넣어줘 next url로 가짐.
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user    # author에 유저정보 포함
            answer.save()
            return redirect('pybo:detail', question_id=question.id)

    else:
        form = AnswerForm()

    context = {'question': question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)
    # answer는 유효성을 통과 못하는 경우가 아예 입력을 안하는 것 밖에 없어서 통과 못하면 그냥 공백 출력해주면 됨
    # 오류가 나도 내용을 유지할 필요 없으므로 form = AnswerForm() 부분이 굳이 필요하지는 않음
    # 그냥 추가해놓음
    # ***사용자 관점에서 메커니즘을 파악하고 코드를 구현하면 여러모로 비슷한 기능이라도 미묘한 차이가 발생.

@login_required(login_url='common:login')
# 로그인이 안되어져있으면 로그인 화면으로 이동
# request.user가 User 객체가 아닌 AnonymousUser 객체먄 오류 발생하므로 해당 어노태이션 필요
# 어노테이션 사용하면 로그아웃 상태에서 '질문 등록하기'를 눌러 로그인 화면으로 전환된 상태에서 웹 브라우저 주소창의 URL을 보면 next 파라미터가 있음.
# 이는 로그인 성공 후 next 파라미터에 있는 URL로 페이지를 이동해야 한다는 의미
# ****로그인 html 탬플릿에 <input type="hidden" name="next" value="{{ next }}"> 넣어줘 next url로 가짐.
def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user      # author에 유저정보 포함
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() # get 일때 (처음 진입할때 form을 선언해 놓아야 함으로 필요)

    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)
    # 전체적인 과정: 처음에 html에서 질문등록 누르면 question_form.html 접근
    # 처음에는 Get형식으로 갈것이라 form = QuestionForm() 빈 객체 선언 굳이 이렇게 구성해야하나 생각이 들지만
    # 게시글 메커니즘을 생각하면 수긍이 감. 뒤 과정에서 자세히 언급.
    # 그 후 양식을 작성하고 제출을 하면 POST 형식으로 들어오고 is_valid()가 유효성 검사를 함.
    # 유효하면 question에 다 저장을 하면 되고
    # 만약 유효하지 않으면 form에다 에러 메시지 넣고 form을 다시 render
    # 이 과정에서 form에 내용이 아예 추가 되지 않은 경우와 form에 일부 내용만 추가된 경우가 있는데
    # 일부 내용만 추가된 경우 form에 해당 내용을 담아 render해줘야 함. 그럼 html에서 내용을 읽어서 작성된 내용은 보존해줌
    # form에 아무 내용 없으면 html에 default_if_none:''으로 빈공간 출력해줌
    # 따라서 유효성 검사에서 통과 못하면 form을 다시 보내줘야하는 상황이오고 html에서 이 form을 기반으로 렌더링이 다시되므로
    # 처음 진입시에도 form = QuestionForm() 이렇게 빈객체를 선언해줘서 빈 form을 보내주는 것. 안그럼 오류남
    # 위의 코드가 최적화가 잘 되어 있어서 과정에 대한 이해가 어려움.

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