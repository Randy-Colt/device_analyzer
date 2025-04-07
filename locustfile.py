from locust import HttpUser, task


class WebsiteTest(HttpUser):
    @task(1)
    def test_create_user(self):
        self.client.post('http://127.0.0.1:8000/api/devices/owners')

    @task(2)
    def test_create_device(self):
        self.client.post('http://127.0.0.1:8000/api/devices/', {'owner_id': 1})

    @task(3)
    def test_get_stats_for_device_user(self):
        self.client.get('http://127.0.0.1:8000/api/devices/owners/1/stats')

    @task(4)
    def test_get_stats(self):
        self.client.get('http://127.0.0.1:8000/api/devices/1/stats')