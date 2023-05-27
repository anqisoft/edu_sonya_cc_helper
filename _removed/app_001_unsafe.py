import platform

from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()

USERS = [
	{'id': '1', 'username': 'AnQi', 'email': 'greenxmcn@gmail.com' },
	{'id': '2', 'username': 'erioruan', 'email': '' },
	{'id': '3', 'username': 'chensson', 'email': '' },
]

def get_user_by_id(id):
	# 根据id从数据库或其他数据源获取用户数据
	# 这里只是一个示例，你可以根据你的需求进行实现
	for user in USERS:
		if user['id'] == id:
			return user


class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID())

    def resolve_user(self, info, id):
        # 根据id从数据库或其他数据源获取用户数据
        # 这里只是一个示例，你可以根据你的需求进行实现
        return get_user_by_id(id)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query), graphiql=True)
)

if __name__ == '__main__':
	# 根据操作系统类型，设置debug（如果是Windows则为True，否则为False）
	debug = True if platform.system() == 'Windows' else False
	app.run(debug=debug)
