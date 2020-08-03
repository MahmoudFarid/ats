import json

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from ats.companies.models import CompanyAdmin, Company
from ats.companies.tests.factories import CompanyFactory, CompanyAdminFactory, CompanyStaffFactory

from ..tests.factories import CategoryFactory, JobFactory
from ..models import Job


class TestJobViewSet(APITestCase):

    def setUp(self) -> None:
        self.main_api = '/api/jobs/'
        self.obj_api = '/api/jobs/{}/'
        self.category = CategoryFactory()
        self.company = CompanyFactory()
        self.unauthorized_client = APIClient()
        self.job_data = {
            "title": "Software Engineer |||",
            "description": "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
            "tags": "Letraset sheets containing Lorem",
            "category": self.category.id,
        }

        self.admin = CompanyAdminFactory(company=self.company)
        self.admin_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.admin)
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.staff = CompanyStaffFactory()
        self.staff_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.staff)
        self.staff_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list_active_jobs_by_company_admin_client(self):
        JobFactory.create_batch(5, status=Job.STATUS.ACTIVE)
        JobFactory.create_batch(5, status=Job.STATUS.DRAFT)
        self.assertEqual(Job.objects.count(), 10)

        response = self.admin_client.get(
            self.main_api,
        )
        self.assertEqual(response.json().get('count'), 5)

        for job in response.json().get('results'):
            self.assertEqual(int(job['status']), Job.STATUS.ACTIVE)

    def test_create_job_by_company_admin_client(self):
        self.assertEqual(Job.objects.count(), 0)

        response = self.admin_client.post(
            self.main_api,
            data=json.dumps(self.job_data),
            content_type='application/json'
        )
        self.assertEqual(int(response.json().get('status')), Job.STATUS.DRAFT)
        self.assertEqual(response.json().get('company'), str(self.admin.company.name))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Job.objects.count(), 1)

    def test_create_job_by_unauthorized_client(self):
        self.assertEqual(Job.objects.count(), 0)

        response = self.unauthorized_client.post(
            self.main_api,
            data=json.dumps(self.job_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Job.objects.count(), 0)

    def test_create_job_by_staff_client(self):
        self.assertEqual(Job.objects.count(), 0)

        response = self.staff_client.post(
            self.main_api,
            data=json.dumps(self.job_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Job.objects.count(), 0)

    def test_list_jobs_by_unauthorized_client(self):
        JobFactory.create_batch(5, status=Job.STATUS.ACTIVE)
        self.assertEqual(Job.objects.count(), 5)

        response = self.unauthorized_client.get(
            self.main_api
        )
        self.assertEqual(response.json().get('count'), 5)

    def test_retrieve_job_by_unauthorized_client(self):
        job = JobFactory(status=Job.STATUS.ACTIVE)
        self.assertEqual(Job.objects.count(), 1)

        response = self.unauthorized_client.get(
            self.obj_api.format(job.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), job.id)

    def test_retrieve_job_by_admin_client(self):
        job = JobFactory(status=Job.STATUS.ACTIVE)
        self.assertEqual(Job.objects.count(), 1)

        response = self.admin_client.get(
            self.obj_api.format(job.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), job.id)

    def test_update_job_by_admin_client(self):
        job = JobFactory(company=self.admin.company)
        self.assertEqual(Job.objects.count(), 1)

        response = self.admin_client.put(
            self.obj_api.format(job.id),
            data=json.dumps(self.job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('title'), self.job_data.get('title'))

    def test_update_job_by_another_admin_client(self):
        job = JobFactory()
        self.assertEqual(Job.objects.count(), 1)

        response = self.admin_client.put(
            self.obj_api.format(job.id),
            data=json.dumps(self.job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_update_job_by_user_client(self):
        job = JobFactory()
        self.assertEqual(Job.objects.count(), 1)

        response = self.client.put(
            self.obj_api.format(job.id),
            data=json.dumps(self.job_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_job_by_another_admin_client(self):
        job = JobFactory()
        self.assertEqual(Job.objects.count(), 1)

        response = self.admin_client.delete(
            self.obj_api.format(job.id),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Job.objects.count(), 1)

    def test_delete_job_by_admin_client(self):
        job = JobFactory(company=self.admin.company)
        self.assertEqual(Job.objects.count(), 1)

        response = self.admin_client.delete(
            self.obj_api.format(job.id),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Job.objects.count(), 0)

    def test_delete_job_by_user_client(self):
        job = JobFactory()
        self.assertEqual(Job.objects.count(), 1)

        response = self.client.delete(
            self.obj_api.format(job.id),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Job.objects.count(), 1)


