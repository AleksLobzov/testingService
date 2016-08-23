from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from testingService.models import Subject, Question, Answer


def index(request):
  
  if request.user.is_authenticated():
    subject_list = Subject.objects.all()
    return render(request, 'testingService/index.html', {'subject_list': subject_list})
  else:
    return render(request, 'testingService/login.html', {'error': 'Вам нужно авторизоваться'})


@csrf_exempt
def user_login(request):
  
  context = RequestContext(request)
  
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user:
      if user.is_active:
        login(request, user)
        subject_list = Subject.objects.all()
        return render(request, 'testingService/index.html', {'subject_list': subject_list})
      else:
        return render(request, 'testingService/login.html', {'error': 'Ваша учетная запись неактивна'})
    else:
      print('Неправильно указаны логин и/или пароль: {0}, {1}'.format(username, password))
      return render(request, 'testingService/login.html', {'error': 'Неправильно указаны логин и/или пароль'})
  else:
    return render_to_response('testingService/login.html', {}, context)


def user_logout(request):
  
  if request.user.is_authenticated():
    logout(request)
  return render(request, 'testingService/login.html', {'error': 'Вы вышли из системы'})


def subject(request, subject_id = None):

  if request.user.is_authenticated():

    if request.method == 'POST':
  
      subject_id = request.POST['subject_id']
      question_id = request.POST['question_id']
      is_correct = request.POST['is_correct']
      question_number = request.POST['question_number']
      question_count = request.POST['question_count']
      answers = request.POST.getlist('checks[]')
      
      threshold = int(question_number) - 1
  
      answer_is_correct = False
  
      if answers != []:     
        
        question = Question.objects.all().filter(id = int(question_id))
        answer_list = Answer.objects.all().filter(question = question, isCorrect = True)
        
        answer_is_correct = True
        
        for answer in answer_list:
          if str(answer.id) not in answers:
            answer_is_correct = False
            break
        
        if answer_is_correct == True:
          is_correct = str(int(is_correct) + 1)
        
        threshold = int(question_number)
        question_number = str(int(question_number) + 1)
        
      subject = get_object_or_404(Subject, pk = subject_id)
      question_list = Question.objects.all().filter(subject = subject).order_by('id')[threshold:]
      
      if question_list:
      
        answer_list = Answer.objects.all().filter(question = question_list[0])
        return render(request, 'testingService/subject.html', {'subject': subject, 'question': question_list[0], 'answer_list': answer_list, 'is_correct': is_correct, 'question_number': question_number, 'question_count': question_count})
      
      else:
        
        return render(request, 'testingService/subject.html', {'result': 'Количество вопросов {0}. Правильных ответов {1}. Неправильных ответов {2}. Процент правильных ответов  {3}%'.format(question_count, is_correct, int(question_count)-int(is_correct), 100*int(is_correct)/int(question_count))})
  
    else:
    
      subject = get_object_or_404(Subject, pk = subject_id)
      question_list = Question.objects.all().filter(subject = subject).order_by('id')
      answer_list = Answer.objects.all().filter(question = question_list[0])
      return render(request, 'testingService/subject.html', {'subject': subject, 'question': question_list[0], 'answer_list': answer_list, 'is_correct': '0', 'question_number': '1', 'question_count': str(len(question_list))})
  
  else:
    return render(request, 'testingService/login.html', {'error': 'Вам нужно авторизоваться'})