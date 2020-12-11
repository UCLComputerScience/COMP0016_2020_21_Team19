from django.test import TestCase
from django.core.urlresolvers import reverse

class DashboardTests(TestCase):
    def test_dashboard_status_code(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)