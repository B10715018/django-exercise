from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

import datetime


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time= timezone.now()+datetime.timedelta(days=30)
        future_question= Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time=timezone.now()-datetime.timedelta(days=1,seconds=1)
        old_question=Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        time=timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_questions=Question(pub_date=time)
        self.assertIs(recent_questions.was_published_recently(), True)

def create_question(question_text):
    return Question.objects.create(question_text=question_text)

class QuestionIndexViewTest(TransactionTestCase):
    reset_sequences = True
    def test_no_question(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=-30)):
            question=create_question(question_text='Past Question')
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
        [question])

    def test_future_question(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=30)):
            create_question(question_text='Future Question')
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=30)):
            create_question(question_text='Future Question')
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=-30)):
            question=create_question(question_text='Past Question')
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
            question
        ])
    
    def test_two_past_questions(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=-30)):
            question1=create_question(question_text='Past Question 1')
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=-5)):
            question2=create_question(question_text='Past Question 2')
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question2,question1])

class QuestionDetailViewTest(TransactionTestCase):
    reset_sequences: True
    # test future questions
    def test_future_question(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=30)):
            future_question=create_question(question_text='Future Question')
        url=reverse('polls:detail',args=(future_question.id,))
        response=self.client.get(url)
        self.assertContains(response,future_question.question_text)
    
    # test past questions
    def test_past_question(self):
        with patch('django.utils.timezone.now', return_value=timezone.now()+
        datetime.timedelta(days=-30)):
            past_question=create_question(question_text='Past Question')
        url=reverse('polls:detail',args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response,past_question.question_text)
