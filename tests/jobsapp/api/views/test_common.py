import json
import pytest

from django.urls import reverse

from rest_framework import status
from jobsapp.models import Job

from tests.factories import JobFactory, UserFactory
from jobsapp.api.views.common import JobViewSet


@pytest.mark.django_db
@pytest.mark.urls('jobsapp.api.urls')
class TestJobViewSet:
    NUM_OF_JOBS = 5

    @pytest.fixture(autouse=True)
    def generate_data(self):
        for x in range(self.NUM_OF_JOBS):
            JobFactory()

    def test_get_jobs_by_id(self, rf) -> None:
        job = Job.objects.first()
        request = rf.get(reverse('job-detail', kwargs={'pk': job.pk}))
        response = JobViewSet.as_view({'get': 'retrieve'})(request, pk=job.pk).render()
        response_json = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert response_json['user']['id'] == job.user.pk
        assert response_json['title'] == job.title

    def test_get_jobs_by_bad_id(self, rf) -> None:
        request = rf.get(reverse('job-detail', kwargs={'pk': "256985698"}))
        response = JobViewSet.as_view({'get': 'retrieve'})(request, pk="256985698").render()
        response_json = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_json['message'] == 'No Job matches the given query.'

    def test_get_all_jobs(self, rf) -> None:
        request = rf.get(reverse('job-list'))
        response = JobViewSet.as_view({'get': 'list'})(request).render()
        response_json = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(response_json) == self.NUM_OF_JOBS
