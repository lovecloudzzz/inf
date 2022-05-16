from random import  choice
class Topic:
    def __init__(self):
        self.topics = []
    def subscribe(self, user_id, topic):
        for i in range(len(self.topics)):
            if self.topics[i][0] == topic:
                self.topics[i].append(user_id)
    def create_topic(self, topic):
        self.topics.append([topic])
    def post_feed(self,topic, post_id):
        for i in range(len(self.topics)):
            if self.topics[i][0] == topic:
                for i in range(1, len(self.topics[i])):
                    print(f'пользователь {i} получил уведомление от топика {topic}, пост id = {post_id}')
site = Topic()
site.create_topic('Блог1')
site.create_topic('Блог2')
for i in range(10):
    site.subscribe(i, 'Блог1')
print(site.topics)
for i in range(10):
    site.post_feed('Блог1', i)
