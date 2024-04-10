#!/usr/bin/env python3

import unittest
from unittest import IsolatedAsyncioTestCase
from fastapi.testclient import TestClient
from main import app

class TestMain(IsolatedAsyncioTestCase):
    async def test_edit_user(self):
        client = TestClient(app)
        # Test case 1: Successful update
        response = await client.put(
            "/edit_user",
            json={
                "email": "test@example.com",
                "firstName": "John",
                "lastName": "Doe",
                "password": "new_password",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "email": "test@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "password": "new_password",
        })

        # Test case 2: Invalid email
        response = await client.put(
            "/edit_user",
            json={
                "email": "invalid_email",
                "firstName": "John",
                "lastName": "Doe",
                "password": "new_password",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid email"})

        # Add more test cases as needed

if __name__ == "__main__":
    unittest.main()