import requests
url_users = 'https://jsonplaceholder.typicode.com/users'
url_posts = 'https://jsonplaceholder.typicode.com/posts'
url_comments = 'https://jsonplaceholder.typicode.com/comments'
users = requests.get(url_users).json()
posts = requests.get(url_posts).json()
comments = requests.get(url_comments).json()
def get_all_email(username: str):
    for data in users:
        if data['username'] == username:
            user_id = data['id']
    for post in posts:
        if post['userId'] == user_id:
            post_id = post['id']
            for comment in comments:
                if comment['postId'] == post_id:
                    print(comment['email'])
    return


print(get_all_email('Bret'))