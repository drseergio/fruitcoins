# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.mail import send_mail
from django.forms import CharField
from core.forms import MoneypitForm
from core.models import Feedback
from settings import FEEDBACK_EMAIL
from settings import SENDER_EMAIL


class FeedbackForm(MoneypitForm):
  text = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(FeedbackForm, self).__init__(*args, **kwargs)

  def save(self):
    feedback = Feedback(
        text=self.cleaned_data['text'],
        date=datetime.now(),
        wealth=self.wealth)
    feedback.save()
    send_mail('New feedback!', feedback.text, SENDER_EMAIL, [FEEDBACK_EMAIL])
