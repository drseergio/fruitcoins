# -*- coding: utf-8 -*-
from base64 import decodestring
from core.forms import MoneypitForm
from core.models import Receipt
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import CharField
from django.forms import FloatField
from django.forms import ValidationError
from PIL import Image
from logging import getLogger
from settings import MAX_RECEIPTS
from settings import MAX_RECEIPT_DIMENSION
from settings import MAX_RECEIPT_SIZE
from StringIO import StringIO
from uuid import uuid4

logger = getLogger('core')


class UploadForm(MoneypitForm):
  longitude = FloatField(required=False)
  latitude = FloatField(required=False)
  image = CharField()

  def __init__(self, *args, **kwargs):
    self.wealth = kwargs.pop('wealth', None)
    super(UploadForm, self).__init__(*args, **kwargs)

  def clean_latitude(self):
    latitude = self.cleaned_data['latitude']
    if not latitude:
      return 0
    if latitude < -90 or latitude > 90:
      raise ValidationError('Invalid latitude')
    return latitude

  def clean_longitude(self):
    longitude = self.cleaned_data['longitude']
    if not longitude:
      return 0
    if longitude < -180 or longitude > 180:
      raise ValidationError('Invalid longitude')
    return longitude

  def clean_image(self):
    receipts = Receipt.objects.filter(wealth=self.wealth)
    if len(receipts) > MAX_RECEIPTS:
      raise ValidationError('You have reached you receipt limit')
    image64 = self.cleaned_data['image']
    if len(image64) > MAX_RECEIPT_SIZE:
      raise ValidationError('Receipt too large')
    try:
      decoded = decodestring(image64)
      content = StringIO(decoded)
      img = Image.open(content)
    except TypeError:
      raise ValidationError('Invalid base64 data')
    except IOError:
      raise ValidationError('Not a JPEG image')
    if img.format != 'JPEG':
      raise ValidationError('Only JPEGs are supported')
    if (img.size[0] > MAX_RECEIPT_DIMENSION or
        img.size[1] > MAX_RECEIPT_DIMENSION):
      try:
        img.thumbnail(
            (MAX_RECEIPT_DIMENSION, MAX_RECEIPT_DIMENSION),
            Image.ANTIALIAS)
      except IOError:
        raise ValidationError('Couldn\t scale receipt, abandoning')
    return img

  def save(self):
    img = self.cleaned_data['image']
    temp_handle = StringIO()
    img.save(temp_handle, 'jpeg')
    temp_handle.seek(0)
    filename = '%s.%s' % (uuid4(), 'jpeg')
    suf = SimpleUploadedFile(
        filename,
        temp_handle.read(),
        content_type='image/jpeg')
    receipt = Receipt(
        image = suf,
        date = datetime.now(),
        wealth = self.wealth,
        longitude = self.cleaned_data['longitude'],
        latitude = self.cleaned_data['latitude'])
    receipt.save()
