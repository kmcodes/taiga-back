# -*- coding: utf-8 -*-

import json

from django import test
from django.core.urlresolvers import reverse

from greenmine.base.users.tests import create_user
from greenmine.projects.models import Project

from . import create_project, add_membership


class ProjectsTestCase(test.TestCase):
    fixtures = ["initial_role.json", ]

    def setUp(self):
        self.user1 = create_user(1)
        self.user2 = create_user(2)
        self.user3 = create_user(3)

        self.project1 = create_project(1, self.user1)
        self.project2 = create_project(2, self.user1)
        self.project3 = create_project(3, self.user2)

        add_membership(self.project1, self.user3, "dev")
        add_membership(self.project3, self.user3, "dev")

    def test_list_projects_by_anon(self):
        response = self.client.get(reverse("projects-list"))
        self.assertEqual(response.status_code, 401)

    def test_list_projects_by_owner(self):
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-list"))
        self.assertEqual(response.status_code, 200)
        projects_list = response.data
        self.assertEqual(len(projects_list), 2)
        self.client.logout()

        response = self.client.login(username=self.user2.username,
                                     password=self.user2.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-list"))
        self.assertEqual(response.status_code, 200)
        projects_list = response.data
        self.assertEqual(len(projects_list), 1)
        self.client.logout()

    def test_list_projects_by_membership(self):
        response = self.client.login(username=self.user3.username,
                                     password=self.user3.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-list"))
        self.assertEqual(response.status_code, 200)
        projects_list = response.data
        self.assertEqual(len(projects_list), 2)
        self.client.logout()

    def test_view_project_by_anon(self):
        response = self.client.get(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 401)

    def test_view_project_by_owner(self):
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("projects-detail", args=(self.project2.id,)))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_view_project_by_membership(self):
        response = self.client.login(username=self.user3.username,
                                     password=self.user3.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("projects-detail", args=(self.project3.id,)))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_view_project_by_not_membership(self):
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.get(reverse("projects-detail", args=(self.project3.id,)))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_create_project_by_anon(self):
        data = {
            "name": "Test Project",
            "description": "A new Test Project",
            "total_story_points": 10
        }

        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.post(
            reverse("projects-list"),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Project.objects.all().count(), 3)

    def test_create_project_by_auth(self):
        data = {
            "name": "Test Project",
            "description": "A new Test Project",
            "total_story_points": 10
        }

        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.post(
            reverse("projects-list"),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.all().count(), 4)
        self.client.logout()

    def test_edit_project_by_anon(self):
        data = {
            "description": "Edited project description",
        }

        self.assertEqual(Project.objects.all().count(), 3)
        self.assertNotEqual(data["description"], self.project1.description)
        response = self.client.patch(
            reverse("projects-detail", args=(self.project1.id,)),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Project.objects.all().count(), 3)

    def test_edit_project_by_owner(self):
        data = {
            "description": "Modified project description",
        }

        self.assertEqual(Project.objects.all().count(), 3)
        self.assertNotEqual(data["description"], self.project1.description)
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.patch(
            reverse("projects-detail", args=(self.project1.id,)),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["description"], response.data["description"])
        self.assertEqual(Project.objects.all().count(), 3)
        self.client.logout()

    def test_edit_project_by_membership(self):
        data = {
            "description": "Edited project description",
        }

        self.assertEqual(Project.objects.all().count(), 3)
        self.assertNotEqual(data["description"], self.project1.description)
        response = self.client.login(username=self.user3.username,
                                     password=self.user3.username)
        self.assertTrue(response)
        response = self.client.patch(
            reverse("projects-detail", args=(self.project1.id,)),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["description"], response.data["description"])
        self.assertEqual(Project.objects.all().count(), 3)
        self.client.logout()

    def test_edit_project_by_not_membership(self):
        data = {
            "description": "Edited project description",
        }

        self.assertEqual(Project.objects.all().count(), 3)
        self.assertNotEqual(data["description"], self.project1.description)
        response = self.client.login(username=self.user2.username,
                                     password=self.user2.username)
        self.assertTrue(response)
        response = self.client.patch(
            reverse("projects-detail", args=(self.project1.id,)),
            json.dumps(data),
            content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Project.objects.all().count(), 3)
        self.client.logout()

    def test_delete_project_by_anon(self):
        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.delete(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Project.objects.all().count(), 3)

    def test_delete_project_by_owner(self):
        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.delete(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.all().count(), 2)
        self.client.logout()

    def test_delete_project_by_membership(self):
        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.login(username=self.user3.username,
                                     password=self.user3.username)
        self.assertTrue(response)
        response = self.client.delete(reverse("projects-detail", args=(self.project1.id,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.all().count(), 2)
        self.client.logout()

    def test_delete_project_by_not_membership(self):
        self.assertEqual(Project.objects.all().count(), 3)
        response = self.client.login(username=self.user1.username,
                                     password=self.user1.username)
        self.assertTrue(response)
        response = self.client.delete(reverse("projects-detail", args=(self.project3.id,)))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Project.objects.all().count(), 3)
        self.client.logout()