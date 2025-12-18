class Label:
    def __init__(self, label_id, name, message_list_visibility, label_list_visibility, label_type):
        self.id = label_id
        self.name = name
        self.message_list_visibility = message_list_visibility
        self.label_list_visibility = label_list_visibility
        self.type = label_type


class Message:
    def __init__(self, msg_id, thread_id, sender, subject, date, body, labels):
        self.id = msg_id
        self.thread_id = thread_id
        self.from_ = sender
        self.subject = subject
        self.date = date
        self.body = body
        self.labels = labels

class Gmail:
    def __init__(self):
        self.labels = []
        self.messages = []

    def parse_data(self, data):
        for label_data in data.get('labels', []):
            label = Label(
                label_id=label_data['id'],
                name=label_data['name'],
                message_list_visibility=label_data.get('messageListVisibility', ''),
                label_list_visibility=label_data.get('labelListVisibility', ''),
                label_type=label_data.get('type', '')
            )
            self.labels.append(label)

        for message_data in data.get('messages', []):
            message = Message(
                msg_id=message_data.get('id'),
                thread_id=message_data.get('threadId'),
                sender=message_data.get('from', ''),
                subject=message_data.get('subject', ''),
                date=message_data.get('date', ''),
                body=message_data.get('body', ''),
                labels=message_data.get('labels', [])
            )
            self.messages.append(message)