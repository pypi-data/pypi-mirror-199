import os
import requests

class Teams():
    def __init__(self, webhook_url=None):
        """
        :param webhook_url: The Webhook url from the teams
        """
        if webhook_url is None:
            try:
                webhook_url = os.environ["WEBHOOK_URL"]
            except Exception:
                raise ValueError("WEBHOOK_URL is missing in both ENV Variable and constructor params.")
        self.webhook_url = webhook_url
        self.http_timeout = 60

    def change_webhook(self, new_webhook):
        """
        :param new_webhook: the new webhook that will replace the older webhook
        :return: none
        """
        self.webhook_url = new_webhook

    def send_to_multiple_channels(self, webhooks_list, message):
        """
        :param webhooks_list: The list of webhooks where the message will be sent.
        :param message: The message that will be posted across all the channels.
        :return: None
        """
        for webhook_url in webhooks_list:
            self.webhook_url = webhook_url
            self.send_message(message)

    def _validate_message(self, message):
        """
        :param message: The message that is to be sent to the teams channel should be of type Message
        :return: Boolean
        """
        if type(message) != type(Message()):
            raise ValueError("Object not of type Message")
        if 'text' not in message.data:
            raise ValueError("Message is empty!")
        return True

    def send_message(self, message):
        """
        :param message: The message that is to be sent to the teams channel should be of type Message
        :return: Boolean (Status of message)
        """
        # self._validate_message(message)
        headers = {"Content-Type": "application/json"}
        r = requests.post(
            self.webhook_url,
            json=message.message,
            headers=headers,
            timeout=self.http_timeout,
        )
        self.last_http_response = r
        if r.status_code == requests.codes.ok:  # pylint: disable=no-member
            return True
        else:
            print(r.text)
            raise r.raise_for_status()


class Message():
    def __init__(self, text=None):
        self.message = {"type": "message", "attachments": list()}
        self.message_data = dict()
        self.message_content = dict()
        self.message_data["contentType"] = "application/vnd.microsoft.card.adaptive"
        self.message_content["$schema"] = "http://adaptivecards.io/schemas/adaptive-card.json"
        self.message_content["version"] = "1.4"
        self.message_content["type"]= "AdaptiveCard"
        self.message_content["body"] = list()
        self.message_content["msteams"] = {"width": "Full"}
        if text is not None:
            textblock = {"type": "TextBlock", "text": text, "width": "Full", "wrap": True}
            self.message_content['body'].append(textblock)
        self.message_data['content'] = self.message_content
        self.message['attachments'].append(self.message_data)

    def add_title(self, title):
        """
        :param title: Title that will be added to the message.
        :return: None
        """
        textblock = {"type": "TextBlock", "text": title, "size": "Large", "weight": "Bolder"}
        self.message_content['body'] = [textblock] + self.message_content['body']
        return self

    def add_text(self, text):
        """
        :param text: Text data (Body of the message) that will be sent to the Teams channel
        :return: None
        """
        textblock = {"type": "TextBlock", "text": text, "wrap": True}
        self.message_content['body'].append(textblock)
        return self

    def add_link_button(self, buttonurl, buttontext):
        """
        This method will add a button with link
        :param buttontext: Text that will be shown in the button
        :param buttonurl: The Url that will be added to the button
        :return: Self
        """
        action_block = {
            "type": "Action.OpenUrl",
            "title": buttontext,
            "url": buttonurl
        }
        if 'actions' in self.message_content:
            self.message_content["actions"].append(action_block)
        else:
            self.message_content["actions"] = [action_block]
        return self


    def add_url(self, link_url, link_text=None):
        """
        :param link_url: Full Http url (eg: https://tekion.com")
        :param link_text: Will replace the Url with custom text, (if not present then link_url will be used as text)
        :return:
        """
        link_text = link_text if link_text is not None else link_url
        link_block = f"[{link_text}]({link_url})"
        textblock = {"type": "TextBlock", "text": link_block}
        self.message_content['body'].append(textblock)
        return self


    def mention_user(self, user_email, user_name=None):
        """
        :param user_email: User Email of the mentioned user
        :param user_name: Name of the mentioned user (this value should match in any of the text blocks)
        :return:
        """
        if user_name is None:
            user_name = user_email
        user_found = False
        for text_blocks in self.message_content['body']:
            if 'text' in text_blocks and user_name in text_blocks['text']:
                user_found = True
                text_blocks['text'] = text_blocks['text'].replace(user_name, f"<at>{user_name}</at>")
        if user_found is True:
            user_mention = {"type": "mention", "text": f"<at>{user_name}</at>", "mentioned": {"id": user_email, "name": user_name}}
            self.__add_user_to_entities(user_mention)
        return self

    def __add_user_to_entities(self, entity):
        """
        :param entity: entity to be added to the msteams object (to be used internally)
        :return:
        """
        if 'entities' in self.message_content['msteams']:
            self.message_content["msteams"]['entities'].append(entity)
        else:
            self.message_content["msteams"]['entities'] = [entity]
        return self

    def cc_users(self, user_list):
        """
        This method is to be used when any user is to be cc'ed in any of the message.
        :param user_list: List of objects with keys name and email eg: [{"name": "Dummy User", "email": "dummy@tekion.com"}]
        :return: self
        """
        cc_block = "cc: "
        for user in user_list:
            cc_block = cc_block + f"<at>{user['name']}</at>, "
        textblock = {"type": "TextBlock", "text": cc_block.strip(", ")}
        self.message_content['body'].append(textblock)
        for user in user_list:
            user_mention = {"type": "mention", "text": f"<at>{user['name']}</at>", "mentioned": {"id": user['email'], "name": user['name']}}
            self.__add_user_to_entities(user_mention)
        return self

    def add_images(self, image_path_list):
        """
        This method will add images to the message (can be used to share screenshots)
        :param image_path_list: full public url of the image (Note: the image must be public)
        :return: Self
        """
        for image in image_path_list:
            image_block = {
                "type": "Image",
                "url": image,
                "msTeams": {
                    "allowExpand": True
                }
            }
            self.message_content['body'].append(image_block)
        return self

    # def add_codeblock(self, codeblock):
    #     code_lines = codeblock.split("\n")
    #     for line in code_lines:
    #
    #     {"type": "RichTextBlock",
    #      "inlines": [{
    #          "type": "TextRun",
    #          "text": "{'Hello': 'Gyaan'}",
    #          "fontType": "monospace",
    #          "highlight": true
    #      }]}
    #     for image in image_path_list:
    #         image_block = {
    #             "type": "Image",
    #             "url": image,
    #             "msTeams": {
    #                 "allowExpand": True
    #             }
    #         }
    #         self.message_content['body'].append(image_block)

    def print(self):
        """
        prints the entire message object for user to debug.
        """
        print(self.message)


    def send(self, webhook=None):
        """
        :return: Response from Teams after sending the message
        """
        response = Teams(webhook).send_message(self)
        return response


