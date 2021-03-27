from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question



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





@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request,'수정권한이 없습니다. ')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        # instance의 의미 : 조회한 질문 question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modified_date = timezone.now() #수정 한 날
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request,'pybo/question_form.html', context)







@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
