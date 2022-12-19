import random
from typing import List

import requests


class GuerrillaMailApi:
    __headers: dict | None = None
    __username: str | None = None
    endpoint: str = 'https://www.guerrillamail.com/ajax.php'

    def __init__(self):
        """
        Create a new GuerrillaMailApi instance. Get a random username and set the headers.
        """
        self.__php_sess_id = ''.join(random.choices('0123456789abcdef', k=26))
        self.__headers = {
            'cookie': f'PHPSESSID={self.__php_sess_id}',
        }
        params = {
            'f': 'get_email_address',
        }
        response = requests.get(GuerrillaMailApi.endpoint, params=params, headers=self.__headers)
        self.__username = response.json()['email_addr'].split('@')[0]

    @property
    def email(self) -> str:
        """
        Get the email address of the current user.
        :return: The email address of the current user.
        """
        return f'{self.__username}@guerillamail.com'

    @property
    def username(self) -> str:
        """
        Get the username of the current user.
        :return: The username of the current user.
        """
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        """
        Set the username of the current user.
        :param username: The new username.
        :return: None
        """
        self.__username = username
        data = {
            'email_user': username,
            'lang': 'en',
            'site': 'guerrillamail.com',
            'in': '+Set+cancel',
        }
        requests.post(GuerrillaMailApi.endpoint, params={'f': 'set_email_user'}, data=data, headers=self.__headers)

    def get_emails_list(self, start_index: int = 0) -> List[int]:
        """
        Get the list of emails ids.
        :param start_index: The index of the first email to get.
        :return: The list of emails ids.
        """
        params = {'f': 'check_email',
                  'seq': start_index}
        response = requests.get(GuerrillaMailApi.endpoint, params=params, headers=self.__headers)
        return [mail['mail_id'] for mail in response.json()['list']]

    def get_email(self, email_id: int) -> str:
        """
        Get the content of an email.
        :param email_id: The id of the email to get.
        :return: The content of the email.
        """
        params = {'f': 'fetch_email',
                  'email_id': f'mr_{email_id}'}
        response = requests.get(GuerrillaMailApi.endpoint, params=params, headers=self.__headers)
        return response.json()['mail_body']


if __name__ == '__main__':
    mail_manager = GuerrillaMailApi()
    mail_manager.username = 'hello'
    mails = mail_manager.get_emails_list(0)
    print(mails)
    print(mail_manager.get_email(mails[0]))
