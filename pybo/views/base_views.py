from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from pybo.models import Question
from django.db.models import Q, Count


def index(request):

    '''pybo 목록 출력'''


    # 입력 파라미터
    # page는 html에서 다음페이지나 이전 페이지를 요청하면 주소뒤에 ?page=숫자 의 get 방식으로 던저줌
    # 만약 그냥 제일 처음 진입 하면 그냥 page는 1로 초기화 해줌 -> get('page', '1')이렇게
    # 그래서 html에서 주소뒤에 ?page=숫자 이런식으로 던지거나 아니면 form으로 get 방식으로 던저주는것임.

    page = request.GET.get('page', '1')  # 페이지숫자를 url서 뒤에 붙여 get으로 던짐 (?page = 1)
    kw = request.GET.get('kw', '')  # 검색어


    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    #정렬 기준이 추천순(recommend)인 경우에는 추천 수가 큰 것부터 정렬하므로 order_by에 추천 수 -num_voter를 입력했다.
    # 추천 수는 장고의 annotate 함수와 Count 함수를 사용.
    # Question.objects.annotate(num_voter=Count('voter'))에서 사용한 annotate 함수는
    # Question 모델의 기존 필드인 author, subject, content, create_date, modify_date, voter에 질문의
    # 추천 수에 해당하는 num_voter 필드를 임시로 추가해 주는 함수.
    # 이렇게 annotate 함수로 num_voter 필드를 추가하면 filter 함수나 order_by 함수에서
    # num_voter 필드를 사용할 수 있음.
    # 여기서 num_voter는 Count('voter')와 같이 Count 함수를 사용하여 만듦.
    # Count('voter')는 해당 질문의 추천 수이다.

#order_by('-num_voter', '-create_date')와 같이 order_by 함수에 두 개 이상의 인자가 전달되는 경우 1번째 항목부터 우선순위를 매긴다. 즉, 추천 수가 같으면 최신순으로 정렬한다.

#그리고 page, kw와 마찬가지로 템플릿에서 요청한 so값을 저장할 수 있도록 context에 so를 추가했다. 코드 수정 후 질문 목록 화면에서 정렬 기능을 사용해 보자. '인기순'으로 정렬하면 답변수가 많은 게시물부터 보여주는 것을 확인할 수 있을 것이다.

    # 조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

        #  함수에 사용된 subject__icontains=kw는 제목에 kw 문자열이 포함되었는지를 의미.
        #  answer__author__username__icontains은 답변을 작성한 사람의 이름에 포함되는지를 의미.
        #  filter 함수에서 모델 필드에 접근하려면 이처럼 __를 이용하면 됨.

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)
