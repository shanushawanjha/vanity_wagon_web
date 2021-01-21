class QuickReply:

    def __init__(self, text=None):
        self.template = {
            "quick_reply": {
                "text": text,
                "buttons": []
            },
            "input": True
        }

    def add_postback(self, text=None, title='', payload='', user_input=True):
        if not self.template["quick_reply"]["text"]:
            self.template["quick_reply"]['text'] = text
        button = {'title': title, 'type': 'postback', 'payload': payload}
        self.template["quick_reply"]["buttons"].append(button)
        self.template["input"] = user_input

    def add_web_url(self, text=None, title='', url='', user_input=False, extension=False):
        if not self.template["quick_reply"]["text"]:
            self.template["quick_reply"]['text'] = text
        button = {'title': title, 'type': 'web_url', 'url': url, 'extension': extension}
        self.template["quick_reply"]["buttons"].append(button)
        self.template["input"] = user_input

    def add_generic_(self, type, title, payload=None, web_url=None, text=None, user_input=True, extension=True):
        if not self.template["quick_reply"]["text"]:
            self.template["quick_reply"]['text'] = text
        if type == "web_url":
            button = {'title': title, 'type': 'web_url', 'url': web_url, 'extension': extension}
        else:
            button = {'title': title, 'type': 'postback', 'payload': payload}
        self.template["quick_reply"]["buttons"].append(button)
        self.template["input"] = user_input

    def get_qr(self):
        return self.template
