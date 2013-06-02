# -*- coding: utf-8 -*-
from celery.task import task
from celery.registry import tasks
from django.db import transaction
from importer.csv_importer import CSVImport
from importer.kmy_importer import KMYImport
from logging import getLogger

logger = getLogger('importer')


def run_importers(wealth, imported_file, to_run=None, account=None):
  importers = []
  importers.append(CSVImport())
  importers.append(KMYImport())

  for importer in importers:
    if to_run and importer.extension not in to_run:
      continue
    if importer.is_supported(imported_file):
      importer.process(wealth, imported_file, account)
      return importer

  raise ValueError('File type is not understood, contact us!')


@task()
@transaction.commit_manually
def commit_task(wealth, importer, task_id=None):
  logger.info('Running import task for user %s' % wealth)

  try:
    importer.save()
    transaction.commit()
    logger.info('Successfully imported for user %s' % wealth)
  except Exception:
    transaction.rollback()
    logger.info('Failed to import for user %s' % wealth)
  transaction.commit()
 

tasks.register(commit_task)
