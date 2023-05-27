import platform
import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

USERS = []

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID())
    users = graphene.List(User)

    def resolve_user(self, info, id):
        id_int: int = int(id)
        return next(filter(lambda x: x['id'] == id_int, USERS), None)

    def resolve_users(self, info):
        return USERS

class Mutation(graphene.ObjectType):
    add_user = graphene.Field(User, name=graphene.String(), email=graphene.String())
    delete_user = graphene.Field(graphene.Boolean, id=graphene.ID())
    update_user = graphene.Field(User, id=graphene.ID(), name=graphene.String(), email=graphene.String())

    def resolve_add_user(self, info, name, email):
        user = {'id': len(USERS) + 1, 'name': name, 'email': email}
        USERS.append(user)
        return user

    def resolve_delete_user(self, info, id):
        id_int: int = int(id)
        for user in USERS:
            if user['id'] == id_int:
                USERS.remove(user)
                return True
        return False

    def resolve_update_user(self, info, id, name, email):
        id_int: int = int(id)
        for user in USERS:
            if user['id'] == id_int:
                user['name'] = name
                user['email'] = email
                return user
        return None

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/')
def index():
    return '<script>window.location.href="/graphql"</script>'

if __name__ == '__main__':
    if platform.system() == 'Windows':
        app.run(port=8001, debug=True)
    else:
        app.run()
