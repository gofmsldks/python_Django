from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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


class Answer(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
