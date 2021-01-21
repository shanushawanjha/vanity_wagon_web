class Carousel:

    def __init__(self):
        self.template = {
            "carousel": []
        }

    def add_element(self, image_url='', title='', caption='', buttons=None, default_action_url=''):
        payload = {'image_url': image_url, "title": title, "caption": caption, "buttons": buttons,
                   "default_url": default_action_url}
        self.template["carousel"].append(payload)

    def get_message(self):
        return self.template
