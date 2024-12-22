import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from server.models.document import Document  # noqa: E501
from server import util


def documents_get():  # noqa: E501
    """Get all documents

     # noqa: E501


    :rtype: Union[List[Document], Tuple[List[Document], int], Tuple[List[Document], int, Dict[str, str]]
    """
    return 'do some magic!'


def documents_id_delete(document_id):  # noqa: E501
    """Delete a document by ID

     # noqa: E501

    :param document_id: 
    :type document_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def documents_id_get(document_id):  # noqa: E501
    """Get a document by ID

     # noqa: E501

    :param document_id: 
    :type document_id: str

    :rtype: Union[Document, Tuple[Document, int], Tuple[Document, int, Dict[str, str]]
    """
    return 'do some magic!'


def documents_id_put(document_id, document):  # noqa: E501
    """Update a document by ID

     # noqa: E501

    :param document_id: 
    :type document_id: str
    :param document: 
    :type document: dict | bytes

    :rtype: Union[Document, Tuple[Document, int], Tuple[Document, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        document = Document.from_dict(connexion.request.get_json())  # noqa: E501
    return { 'document_id': document_id, 'document': document }


def documents_post(document):  # noqa: E501
    """Create a new document

     # noqa: E501

    :param document: 
    :type document: dict | bytes

    :rtype: Union[Document, Tuple[Document, int], Tuple[Document, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        document = Document.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
