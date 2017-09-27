from rocketchat_API.rocketchat import RocketChat

secrets = {
    "email": "abc@123.com",
    "name": "Test",
    "password": "password",
    "username": "test"
}

# Connect via admin account
rocket = RocketChat(secrets['username'], secrets['password'], server_url='http://localhost', ssl_verify=False)
admin = rocket.me().json()

def create_user(email, name, password, username):
    """Creates user and returns user info"""
    create_user_response = rocket.users_create(email, name, password, username).json()
    if not create_user_response['success']:
        raise ValueError(create_user_response['error'])
    return create_user_response['user']

def add_user_to_group(username, group_name):
    user_id = get_user(username)['_id']
    group_id = get_group(group_name)['_id']
    user_group_response = rocket.groups_invite(group_id, user_id).json()
    if not user_group_response['success']:
        raise ValueError(user_group_response['error'])
    return user_group_response

def create_new_group(name):
    """Creates new group, adds admin user to group, and returns group info"""
    create_group_response = rocket.groups_create(name).json()
    if not create_group_response['success']:
        raise ValueError(create_group_response['error'])
    add_owner_response = rocket.groups_add_owner(group['group']['_id'], admin['_id'])
    if not add_owner_response['success']:
        raise ValueError(add_owner_response['error'])
    return create_group_response['group']

def get_user(username):
    users = rocket.users_list().json()['users']
    user = [user for user in users if user['username'] == username]
    return user[0] if user else None

def get_group(group_name):
    groups = rocket.groups_list().json()['groups']
    group = [group for group in groups if group['name'] == group_name]
    return group[0] if group else None


print(add_user_to_group("userone", "testgroup3"))

#create_user('abc1@123.com', 'test1', 'pass', 'test1')

# rocket.channels_list().json()
# rocket.chat_post_message('good news everyone!', channel='GENERAL', alias='Farnsworth').json()
# rocket.channels_history('GENERAL', count=5).json()