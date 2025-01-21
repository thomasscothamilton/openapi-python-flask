import unittest
from unittest.mock import patch, MagicMock
from server.controllers import document_controller
from flask import Flask


class TestDocumentController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    @patch.dict('os.environ', {
        'USE_SQLITE': "True"
    })
    @patch('server.controllers.document_controller.SessionLocal')
    def test_documents_get(self, mock_session):
        mock_session.return_value.__enter__.return_value.query.return_value.all.return_value = []
        with self.app.test_request_context():
            result = document_controller.documents_get()
            self.assertEqual(result[1], 200)
            self.assertEqual(result[0].json, [])

    @patch.dict('os.environ', {
        'USE_SQLITE': "True"
    })
    @patch('server.controllers.document_controller.SessionLocal')
    def test_documents_id_get(self, mock_session):
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = None
        with self.app.test_request_context():
            result = document_controller.documents_id_get(1)
            self.assertEqual(result[1], 404)
            self.assertEqual(result[0].json, {"error": "Document not found"})

    @patch.dict('os.environ', {
        'USE_SQLITE': "True"
    })
    @patch('server.controllers.document_controller.SessionLocal')
    @patch('server.controllers.document_controller.publish_message')
    def test_documents_post(self, mock_publish, mock_session):
        mock_session.return_value.__enter__.return_value.add.return_value = None
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_session.return_value.__enter__.return_value.refresh.return_value = None
        mock_publish.return_value = None
        with self.app.test_request_context(json={"title": "Test", "content": "Test content"}):
            result = document_controller.documents_post()
            self.assertEqual(result[1], 201)
            self.assertIn("id", result[0].json)

    @patch.dict('os.environ', {
        'USE_SQLITE': "True"
    })
    @patch('server.controllers.document_controller.SessionLocal')
    @patch('server.controllers.document_controller.publish_message')
    def test_documents_id_delete(self, mock_publish, mock_session):
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = MagicMock()
        mock_session.return_value.__enter__.return_value.delete.return_value = None
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_publish.return_value = None
        with self.app.test_request_context():
            result = document_controller.documents_id_delete(1)
            self.assertEqual(result[1], 200)
            self.assertEqual(result[0].json, {"message": "Document deleted"})

    @patch.dict('os.environ', {
        'USE_SQLITE': "True"
    })
    @patch('server.controllers.document_controller.SessionLocal')
    @patch('server.controllers.document_controller.publish_message')
    def test_documents_id_put(self, mock_publish, mock_session):
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = MagicMock()
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_publish.return_value = None
        with self.app.test_request_context(json={"title": "Updated title", "content": "Updated content"}):
            result = document_controller.documents_id_put(1, {"title": "Updated title", "content": "Updated content"})
            self.assertEqual(result[1], 200)
            self.assertEqual(result[0].json, {"message": "Document updated"})

if __name__ == '__main__':
    unittest.main()