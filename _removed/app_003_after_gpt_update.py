import platform
import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID())

    def resolve_user(self, info, id):
        return get_user_by_id(id)

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

'''
这里做了以下几点优化：

创建了独立的 Mutation 类型，并将新增、删除和更新用户的方法放入其中，使代码结构更清晰。
将 Query 和 Mutation 类型都注册到了 schema 中，以便正确处理查询和变异操作。
修改了 resolve_add_user、resolve_delete_user 和 resolve_update_user 方法的签名，使其符合 GraphQL 规范。
将 schema 直接传递给 GraphQLView，避免了多余的 graphene.Schema 实例化步骤。
请注意，代码中的 get_user_by_id 方法需要进行定义和实现，以根据用户 ID 从数据库或其他数据源获取用户数据。另外，确保 USERS 列表的数据与你的需求相匹配。
'''