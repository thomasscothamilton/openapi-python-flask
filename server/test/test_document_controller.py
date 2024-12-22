import unittest
from unittest.mock import patch, MagicMock
from flask import json
from server.models.document import Document  # noqa: E501
from server.test import BaseTestCase
from server.controllers import document_controller


class TestDocumentController(BaseTestCase):
    """DocumentController integration test stubs"""

    @patch('server.controllers.document_controller.Document')
    def test_documents_get(self, mock_document):
        """Test case for documents_get

        Get all documents
        """
        result = document_controller.documents_get()
        self.assertEqual(result, 'do some magic!')

    @patch('server.controllers.document_controller.Document')
    def test_documents_id_delete(self, mock_document):
        """Test case for documents_id_delete

        Delete a document by ID
        """
        result = document_controller.documents_id_delete('123')
        self.assertEqual(result, 'do some magic!')

    @patch('server.controllers.document_controller.Document')
    def test_documents_id_get(self, mock_document):
        """Test case for documents_id_get

        Get a document by ID
        """
        result = document_controller.documents_id_get('123')
        self.assertEqual(result, 'do some magic!')

    @patch('server.controllers.document_controller.connexion')
    @patch('server.controllers.document_controller.Document')
    def test_documents_id_put(self, mock_document, mock_connexion):
        """Test case for documents_id_put

        Update a document by ID
        """
        mock_connexion.request.is_json = True
        mock_connexion.request.get_json.return_value = {'key': 'value'}
        mock_document.from_dict.return_value = Document()

        result = document_controller.documents_id_put('123', {'key': 'value'})
        self.assertEqual(result, {'document_id': '123', 'document': mock_document.from_dict.return_value})

    @patch('server.controllers.document_controller.connexion')
    @patch('server.controllers.document_controller.Document')
    def test_documents_post(self, mock_document, mock_connexion):
        """Test case for documents_post

        Create a new document
        """
        mock_connexion.request.is_json = True
        mock_connexion.request.get_json.return_value = {'key': 'value'}
        mock_document.from_dict.return_value = Document()

        result = document_controller.documents_post({'key': 'value'})
        self.assertEqual(result, 'do some magic!')


if __name__ == '__main__':
    unittest.main()