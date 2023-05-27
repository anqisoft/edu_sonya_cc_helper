from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

# Define the schema
schema = """
type Query {
    get_user(id: ID!): User
}

type User {
    id: ID!
    name: String!
}
"""

# Create the GraphQL view
# graphql_view = GraphQLView(schema=schema) # AssertionError: A Schema is required to be provided to GraphQLView.
# graphql_view = GraphQLView(schema=graphene.Schema(schema)) # is not a valid ObjectType.
graphql_view = GraphQLView(schema=graphene.Schema(query=schema)) # is not a valid ObjectType.

# Register the view with the app
app.add_url_rule("/graphql", view_func=graphql_view)

# Run the app
if __name__ == "__main__":
    app.run()