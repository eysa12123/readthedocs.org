"""Utilities related to reading and generating indexable search content."""

import structlog
from django.utils import timezone
from django_elasticsearch_dsl.apps import DEDConfig
from django_elasticsearch_dsl.registries import registry

log = structlog.get_logger(__name__)


def remove_indexed_files(model, project_slug, version_slug=None, build_id=None):
    """
    Remove files from `version_slug` of `project_slug` from the search index.

    :param model: Class of the model to be deleted.
    :param project_slug: Project slug.
    :param version_slug: Version slug. If isn't given,
                    all index from `project` are deleted.
    :param build_id: Build id. If isn't given, all index from `version` are deleted.
    """

    log.bind(
        project_slug=project_slug,
        version_slug=version_slug,
    )

    if not DEDConfig.autosync_enabled():
        log.info("Autosync disabled, skipping removal from the search index.")
        return

    try:
        document = list(registry.get_documents(models=[model]))[0]
        log.info("Deleting old files from search index.")
        documents = document().search().filter("term", project=project_slug)
        if version_slug:
            documents = documents.filter("term", version=version_slug)
        if build_id:
            documents = documents.exclude("term", build=build_id)
        documents.delete()
    except Exception:
        log.exception("Unable to delete a subset of files. Continuing.")


def _get_index(indices, index_name):
    """
    Get Index from all the indices.

    :param indices: DED indices list
    :param index_name: Name of the index
    :return: DED Index
    """
    for index in indices:
        if index._name == index_name:
            return index


def _get_document(model, document_class):
    """
    Get DED document class object from the model and name of document class.

    :param model: The model class to find the document
    :param document_class: the name of the document class.
    :return: DED DocType object
    """
    documents = registry.get_documents(models=[model])

    for document in documents:
        if str(document) == document_class:
            return document


def _last_30_days_iter():
    """Returns iterator for previous 30 days (including today)."""
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)

    # this includes the current day, len() = 31
    return (thirty_days_ago + timezone.timedelta(days=n) for n in range(31))


def _get_last_30_days_str(date_format="%Y-%m-%d"):
    """Returns the list of dates in string format for previous 30 days (including today)."""
    last_30_days_str = [
        timezone.datetime.strftime(date, date_format) for date in _last_30_days_iter()
    ]
    return last_30_days_str
