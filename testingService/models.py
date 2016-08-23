from django.db import models


class Subject(models.Model):
  
  title = models.CharField(max_length = 64)

  def __str__(self):
    return self.title


class Question(models.Model):
  
  title = models.CharField(max_length = 128)
  subject = models.ForeignKey(Subject)

  def __str__(self):
    return self.title


class Answer(models.Model):
  
  title = models.CharField(max_length = 128)
  isCorrect = models.BooleanField(default = False)
  question = models.ForeignKey(Question)

  def __str__(self):
    return self.title