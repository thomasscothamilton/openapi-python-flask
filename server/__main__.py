#!/usr/bin/env python3

import connexion

from server import encoder, database


def main():
    engine = database.init_connection_pool()
    database.migrate_db(engine)

    app = connexion.App(__name__, specification_dir='./openapi/')

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Document Service API'},
                pythonic_params=True)

    app.run(port=8080)


if __name__ == '__main__':
    main()
