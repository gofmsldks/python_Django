from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer



@login_required(login_url='common:login')
# 로그인이 안되어져있으면 로그인 화면으로 이동
# request.user가 User 객체가 아닌 AnonymousUser 객체면 오류 발생하므로 해당 어노태이션 필요
# 어노테이션 사용하면 로그아웃 상태에서 '질문 등록하기'를 눌러 로그인 화면으로 전환된 상태에서 웹 브라우저 주소창의 URL을 보면 next 파라미터가 있음.
# 이는 로그인 성공 후 next 파라미터에 있는 URL로 페이지를 이동해야 한다는 의미
# ****로그인 html 탬플릿에 <input type="hidden" name="next" value="{{ next }}"> 넣어줘 next url로 가짐.
def answer_create(request, question_id):

    question = get_object_or_404(Question, pk = question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user    # author에 유저정보 포함
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))

    else:
        form = AnswerForm()

    context = {'question': question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)
    # answer는 유효성을 통과 못하는 경우가 아예 입력을 안하는 것 밖에 없어서 통과 못하면 그냥 공백 출력해주면 됨
    # 오류가 나도 내용을 유지할 필요 없으므로 form = AnswerForm() 부분이 굳이 필요하지는 않음
    # 그냥 추가해놓음
    # ***사용자 관점에서 메커니즘을 파악하고 코드를 구현하면 여러모로 비슷한 기능이라도 미묘한 차이가 발생.




@login_required(login_url='common:login')
def answer_delete(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id= answer.question.id)
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)




@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():

            answer = form.save(commit=False)
            answer.author = request.user
            answer.modified_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form, 'answer':answer}
    return render(request, 'pybo/answer_form.html', context)