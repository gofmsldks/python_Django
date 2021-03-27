from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from pybo.models import Question


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
