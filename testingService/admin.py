from django.contrib import admin
from testingService.models import Subject, Question, Answer
from django import forms
from django.forms.models import BaseInlineFormSet


class AnswerInlineFormSet(BaseInlineFormSet):

  def clean(self):
  # проверка на количество ответов на вопрос - не меньше двух
    count = 0
    isCorrect = []
    for answer in self.forms:
      try:
        if answer.cleaned_data:
          count += 1
          isCorrect.append(answer.cleaned_data['isCorrect'])
      except AttributeError:
        pass
    if count < 2:
      raise forms.ValidationError('Для вопроса должно быть предложено хотя бы два ответа')
  # валидация на то, что должен быть хотя бы один правильный вариант
    if True not in isCorrect:
      raise forms.ValidationError('Должен быть хотя бы один правильный ответ')
  # валидация на то, что все варианты не могут быть правильными 
    if False not in isCorrect:
      raise forms.ValidationError('Все варианты не могут быть правильными')


class AnswerInline(admin.TabularInline):
 
  model = Answer
  extra = 1
  formset = AnswerInlineFormSet


class QuestionInlineFormSet(BaseInlineFormSet):
 
  def clean(self):
  # проверка на количество вопросов по теме - не меньше одного
    count = 0
    for question in self.forms:
      try:
        if question.cleaned_data:
          count += 1
      except AttributeError:
        pass
    if count < 1:
      raise forms.ValidationError('Для теста должен быть предложен хотя бы один вопрос')


class QuestionInline(admin.TabularInline):
 
  model = Question
  extra = 1
  show_change_link = True
  formset = QuestionInlineFormSet


class SubjectAdmin(admin.ModelAdmin):
 
  fieldsets = [
    (None, {'fields': ['title']}),
  ]
  inlines = [QuestionInline]


admin.site.register(Subject, SubjectAdmin)


class QuestionAdmin(admin.ModelAdmin):
  
  inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
