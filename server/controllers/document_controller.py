from flask import jsonify, request
from server.database import SessionLocal
from server.models import Document
from server.pubsub import publish_message


def handle_error(exception):
    """Helper function for standardized error responses."""
    return jsonify({"error": str(exception)}), 500


def serialize_document(document):
    """Helper function to serialize a Document object."""
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at
    }

def documents_post():
    session = SessionLocal()
    try:
        data = request.get_json()
        new_document = Document(title=data["title"], content=data["content"])
        session.add(new_document)
        session.commit()  # Commit the transaction to persist the data
        session.refresh(new_document)  # Refresh the instance to load the generated primary key

        return jsonify({
            "id": new_document.id,
            "title": new_document.title,
            "content": new_document.content,
            "created_at": new_document.created_at
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def documents_get():
    try:
        with SessionLocal() as session:
            documents = session.query(Document).all()
            return jsonify([serialize_document(doc) for doc in documents]), 200
    except Exception as e:
        return handle_error(e)


def documents_id_get(document_id):
    try:
        with SessionLocal() as session:
            document = session.query(Document).filter(Document.id == document_id).first()
            if document:
                return jsonify(serialize_document(document)), 200
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return handle_error(e)


def documents_id_delete(document_id):
    try:
        with SessionLocal() as session:
            document = session.query(Document).filter(Document.id == document_id).first()
            if document:
                session.delete(document)
                session.commit()
                # Publish Pub/Sub event
                publish_message(f"Document with ID {document_id} deleted")
                return jsonify({"message": "Document deleted"}), 200
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return handle_error(e)

def documents_id_put(document_id, document):
    try:
        with SessionLocal() as session:
            existing_document = session.query(Document).filter(Document.id == document_id).first()
            if existing_document:
                existing_document.title = document["title"]
                existing_document.content = document["content"]
                session.commit()
                # Publish Pub/Sub event
                publish_message(f"Document with ID {document_id} updated")
                return jsonify({"message": "Document updated"}), 200
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return handle_error(e)