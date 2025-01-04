#!/usr/bin/env python3

import connexion

from server import encoder
from server.database import init_db


def main():
    init_db()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Document Service API'},
                pythonic_params=True)

    app.run(port=8080)


if __name__ == '__main__':
    main()
