from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # models.CASCADE: 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제
    #author 추가한 후 makemigrations 하면 오류 생김,름
    # Question 모델에 author 필드를 추가하면 이미 등록되어 있던 게시물에 author 필드에 해당되는 값이 저장되어야 하는데,
    # 장고는 author 필드에 어떤 값을 넣어야 하는지 모름
    # 해결하는 방법에는 2가지가 있다. 첫 번째 방법은 author 필드를 null로 설정하는 방법이고,
    # 두 번째 방법은 기존 게시물에 추가될 author 필드의 값에 강제로 임의 계정 정보를 추가하는 방법.
    # 질문, 답변에는 author 필드값이 무조건 있어야 하므로 두 번째 방법을 사용. 오류 메시지를 유지한 상태에서 '1'을 입력하고 엔터 두번 반복.
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True) # 수정일시를 의미, null=True, blank=True는 어떤 조건으로든 값을 비워둘 수 있음
    voter = models.ManyToManyField(User, related_name='voter_question')    # voter 추가, 다대다 관계를 위 한 ManyToManyField
    # 추천은 질문이나 답변에 적용해야 하는 요소.
    # Question, Answer 모델에 추천인 필드 voter를 추가해야 한다.
    # 게시판 서비스를 사용해 봤다면 글 1개에 여러 명이 추천할 수 있고,
    # 반대로 1명이 여러 개의 글을 추천할 수 있음을 쉽게 알 수 있음.
    # 그리고 이런 경우에는 모델의 다대다(ManyToMany) 관계를 사용해야 한다.

    # Question 모델에서 사용한 author와 voter 필드가 모두 User 모델을 참조,
    # 추후 User.question_set과 같이 User 모델을 통해 Question 데이터에 접근할 경우 author 필드를 기준으로 할지 voter 필드를 기준으로 할지 장고는 알 수 없으므로
    # 직접 정하라는 뜻이다. related_name 옵션 추가로 해결할 수 있다.
    # author 필드에는 related_name='author_question'을 추가하고, voter 필드에는 related_name='voter_question'을 추가.
    # 이렇게 하면 특정 사용자가 작성한 질문을 얻기 위해 some_user.author_question.all(), some_user.voter_question.all() 같은 코드를 사용할 수 있다.
    def __str__(self):
         return self.subject

class Answer(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # models.CASCADE: 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제
    # author 추가한 후 makemigrations 하면 오류 생김,름
    # Question 모델에 author 필드를 추가하면 이미 등록되어 있던 게시물에 author 필드에 해당되는 값이 저장되어야 하는데,
    # 장고는 author 필드에 어떤 값을 넣어야 하는지 모름
    # 해결하는 방법에는 2가지가 있다. 첫 번째 방법은 author 필드를 null로 설정하는 방법이고,
    # 두 번째 방법은 기존 게시물에 추가될 author 필드의 값에 강제로 임의 계정 정보를 추가하는 방법.
    # 질문, 답변에는 author 필드값이 무조건 있어야 하므로 두 번째 방법을 사용. 오류 메시지를 유지한 상태에서 '1'을 입력하고 엔터 두번 반복.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True) # 수정일시를 의미, null=True, blank=True는 어떤 조건으로든 값을 비워둘 수 있음
    voter = models.ManyToManyField(User, related_name='voter_answer')





class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,null=True, blank=True)
    # 질문에 댓글을 작성하면 Comment 모델의 question 필드에 값이 저장되고,
    # 답변에 댓글이 작성되면 answer에 값이 저장.
    # 즉, Comment 모델 데이터에는 question 필드 또는 answer 필드 중 하나에만 값이 저장되므로
    # *두 필드는 모두 null=True, blank=True여야 한다.

