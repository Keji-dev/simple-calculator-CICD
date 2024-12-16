import http.client
import os
import unittest 
from urllib.request import urlopen
import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "6", "ERROR EN LA MULTIPLICACIÓN"
        )       
    
    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/6/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            float(response.read().decode()), 3.0, "ERROR EN LA DIVISIÓN"
        )

    def test_api_divide_by_zero_error(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        except Exception as e:
            self.assertEqual(e.code, 406, f"Se esperaba el código 406 pero fue {e.code}")

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
