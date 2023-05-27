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
        # 显示所有USERS内容
        print('resolve_user(), USERS', USERS)

        # 用lambda表达式处理，如果USERS中有指定id的用户，则返回；否则返回None
        return next(filter(lambda x: x['id'] == id, USERS), None)

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
        for user in USERS:
            if user['id'] == id:
                USERS.remove(user)
                return True
        return False

    def resolve_update_user(self, info, id, name, email):
        # 显示所有USERS内容
        print('resolve_update_user(), USERS', USERS)

        for user in USERS:
            if user['id'] == id:
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
