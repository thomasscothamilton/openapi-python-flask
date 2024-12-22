import unittest

from flask import json

from server.models.document import Document  # noqa: E501
from server.test import BaseTestCase


class TestDocumentController(BaseTestCase):
    """DocumentController integration test stubs"""

    def test_documents_get(self):
        """Test case for documents_get

        Get all documents
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/documents',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_documents_id_delete(self):
        """Test case for documents_id_delete

        Delete a document by ID
        """
        headers = { 
        }
        response = self.client.open(
            '/documents/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_documents_id_get(self):
        """Test case for documents_id_get

        Get a document by ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/documents/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_documents_id_put(self):
        """Test case for documents_id_put

        Update a document by ID
        """
        document = {"id":"id","title":"title","content":"content"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/documents/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_documents_post(self):
        """Test case for documents_post

        Create a new document
        """
        document = {"id":"id","title":"title","content":"content"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/documents',
            method='POST',
            headers=headers,
            data=json.dumps(document),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
