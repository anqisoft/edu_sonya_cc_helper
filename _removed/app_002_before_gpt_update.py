import platform

import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)


class User(graphene.ObjectType):
	id = graphene.ID()
	name = graphene.String()
	email = graphene.String()


USERS = []


# 	{'id': 1, 'name': 'AnQi', 'email': 'greenxmcn@gmail.com' },
# 	{'id': 2, 'name': 'erioruan', 'email': '' },
# 	{'id': 3, 'name': 'chensson', 'email': '' },
# ]

def get_user_by_id(id):
	print(f'get_user_by_id({id})')
	# 根据id从数据库或其他数据源获取用户数据
	# 这里只是一个示例，你可以根据你的需求进行实现
	for user in USERS:
		if user['id'] == id:
			print(user)
			return user
	return None


class Query(graphene.ObjectType):
	user = graphene.Field(User, id=graphene.ID())

	def resolve_user(self, info, id):
		# 根据id从数据库或其他数据源获取用户数据
		# 这里只是一个示例，你可以根据你的需求进行实现
		return get_user_by_id(id)

	# 定义其它方法，比如获取所有用户的方法
	def resolve_users(self, info):
		return USERS

	# 增加用户
	def resolve_add_user(self, info, name, email):
		# 根据id从数据库或其他数据源获取用户数据
		# 这里只是一个示例，你可以根据你的需求进行实现
		user = {'id': len(USERS) + 1, 'name': name, 'email': email}
		USERS.append(user)
		return user

	# 删除用户
	def resolve_delete_user(self, info, id):
		# 根据id从数据库或其他数据源获取用户数据
		# 这里只是一个示例，你可以根据你的需求进行实现
		for user in USERS:
			if user['id'] == id:
				USERS.remove(user)
				return True
		return False

	# 修改用户

	def resolve_update_user(self, info, id, name, email):
		# 根据id从数据库或其他数据源获取用户数据
		# 这里只是一个示例，你可以根据你的需求进行实现
		for user in USERS:
			if user['id'] == id:
				user['name'] = name
				user['email'] = email
				return user
		return None


app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query), graphiql=True))


# 增加GET请求的路由，方便在浏览器中查看
@app.route('/')
def index():
	# return '<a href="/graphql">graphql</a>'
	# 通过javascript自动跳转到/graphql
	return '<script>window.location.href="/graphql"</script>'


if __name__ == '__main__':
	# print(platform.system()) # Windows
	if platform.system() == 'Windows':
		app.run(port=8001, debug=True)
	else:
		app.run()

'''
query {
  user {
    id
    name
    email
  }
}
'''

# https://graphql.org/
