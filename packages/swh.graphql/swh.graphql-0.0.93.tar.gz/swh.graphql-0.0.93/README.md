Software Heritage GraphQL API
=============================

This repository holds the development of Software Heritage GraphQL API.
A staging version of this service is available at https://graphql.staging.swh.network

Running locally
---------------

Refer to https://docs.softwareheritage.org/devel/getting-started.html#getting-started for
running software heritage services locally.

If you wish to run SWH-GraphQL independently, and have access to SWH storage services,
following make targets can be used.

* make run-dev: Use the config file at ``swh/graphql/config/dev.yml`` and start the service in
  auto-reload mode using uvicorn

* make run-dev-stable: Use the config file at ``swh/graphql/config/dev.yml`` and start the
  service using uvicorn

* make run-dev-docker: Run the service inside a docker container and Use the config file
  at ``swh/graphql/config/dev.yml``

* make run-wsgi-docker: Run the service inside a docker container and Use the config file
  at ``swh/graphql/config/staging.yml``

* visit http://localhost:8000 to use the query explorer

Running a query
---------------

The easiest way to run a query is using the query explorer.
Please provide an SWH API token if you wish to run bigger queries.

Using curl
----------

.. code-block:: console

   curl -i -H 'Content-Type: application/json' -H "Authorization: bearer your-api-token" -X POST -d '{"query": "query {origins(first: 2) {nodes {url}}}"}' http://127.0.0.1:8000


Using Python requests
---------------------

.. code-block:: python

   import requests

   url = "http://127.0.0.1:8000"
   query = """
   {
     origins(first: 2) {
       pageInfo {
         hasNextPage
           endCursor
       }
       edges {
         node {
           url
         }
       }
     }
   }
   """
   json = {"query" : query}
   api_token = "your-api-token"
   headers = {'Authorization': 'Bearer %s' % api_token}

   r = requests.post(url=url, json=json, headers=headers)
   print (r.json())
