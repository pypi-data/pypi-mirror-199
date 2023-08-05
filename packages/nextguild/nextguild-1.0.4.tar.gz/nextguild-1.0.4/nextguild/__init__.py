import requests
import json
import time
import asyncio
import websockets
from functools import wraps


class Client:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'NextGuild/1.0',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.base_url = 'https://www.guilded.gg/api/v1'
        self.cache = {}
        self._message_handlers = []

    def send_message(self, channel_id, content=None, embed=None, isPrivate=None):
        payload = {}

        if content is not None:
            payload['content'] = content

        if embed is not None:
            payload['embeds'] = [embed.embed]
            
        if isPrivate is not None:
            payload['isPrivate'] = isPrivate
            

        response = requests.post(
            f'{self.base_url}/channels/{channel_id}/messages',
            headers=self.headers,
            json=payload
        )

    def send_reply(self, channel_id, replyids, content=None, embed=None, isPrivate=None):
        url = f'{self.base_url}/channels/{channel_id}/messages'
        data = {}
        if content is not None:
            data['content'] = content

        if embed is not None:
            data['embeds'] = [embed.embed]

        if isPrivate is not None:
            data['isPrivate'] = isPrivate



        response = self.request('POST', url, json=data)
        return response

    def edit_message(self, channel_id, message_id, content=None, embed=None, isPrivate=None):
        payload = {}
        if content is not None:
            payload['content'] = content

        if embed is not None:
            payload['embeds'] = [embed.embed]

        if isPrivate is not None:
            payload['isPrivate'] = isPrivate


        url = f'{self.base_url}/channels/{channel_id}/messages/{message_id}'
        response = self.request('PUT', url, json=payload)
        return response

    def delete_message(self, channel_id, message_id):
        url = f'{self.base_url}/channels/{channel_id}/messages/{message_id}'
        response = self.request('DELETE', url)
        return response

    def get_message(self, channel_id, message_id):
        url = f'{self.base_url}/channels/{channel_id}/messages/{message_id}'
        response = self.request('GET', url)
        return response

    def get_channel_messages(self,channel_id,limit=None,before=None,after=None,includePrivate=None):
        url = f'{self.base_url}/channels/{channel_id}/messages'
        params = {}
        if limit:
            params['limit'] = limit
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if includePrivate:
            params['includePrivate'] = includePrivate
        response = self.request('GET', url, params=params)
        return response

    def purge(self, channel_id, amount):
        messages = self.get_channel_messages(channel_id, amount)
        message_ids = [msg['id'] for msg in messages['messages']]
        for message_id in message_ids:
            self.delete_message(channel_id, message_id)
        return len(message_ids)

    def request(self, method, url, **kwargs):
        response = requests.request(method, url, headers=self.headers, **kwargs)
        if response.status_code == 429:
            retry_after = int(response.headers.get('retry-after', '1'))
            print(f'Received 429 status. Retrying after {retry_after} seconds.')
            time.sleep(retry_after)
            return self.request(method, url, **kwargs)
        else:
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = response.text
            if 200 <= response.status_code < 300:
                return data
            else:
                raise ValueError(
                    f'Request failed with status {response.status_code}: {data}')

    def create_channel(self,name,type,serverid,groupid=None,categoryid=None,ispublic=None):
        data = {'name': name, 'type': type}
        url = f'{self.base_url}/channels'
        if categoryid:
            data.update({'categoryId': categoryid})
        if groupid:
            data.update({'groupId': groupid})
        if serverid:
            data.update({'serverId': serverid})
        if ispublic:
            data.update({"isPublic": ispublic})
        response = self.request('POST', url, json=data)
        return response

    def get_channel(self, channelid):
        url = f'{self.base_url}/channels/{channelid}'
        response = self.request('GET', url)
        return response

    def delete_channel(self, channelid):
        url = f'{self.base_url}/channels/{channelid}'
        response = self.request('DELETE', url)
        return response

    def update_channel(self, channelid, name=None, topic=None, ispublic=None):
        data = {}
        url = f'{self.base_url}/channels/{channelid}'
        if name:
            data.update({'name': name})
        if topic:
            data.update({'topic': topic})
        if ispublic:
            data.update({'ispublic': ispublic})
        response = self.request('PATCH', url, json=data)
        return response

    def get_server(self, serverid):
        url = f'{self.base_url}/servers/{serverid}'
        response = self.request('GET', url)
        return response

    def get_server_members(self, serverid):
        url = f'{self.base_url}/servers/{serverid}/members'
        response = self.request('GET', url)
        return response

    def get_server_member(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}'
        response = self.request('GET', url)
        return response

    def update_nickname(self, serverid, userid, nickname):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/nickname'
        data = {'nickname': nickname}
        response = self.request('PUT', url, json=data)
        return response

    def delete_nickname(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/nickname'
        response = self.request('DELETE', url)
        return response

    def kick_member(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}'
        response = self.request('DELETE', url)
        return response

    def ban_member(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/bans/{userid}'
        response = self.request('POST', url)
        return response

    def add_role(self, serverid, userid, roleid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/roles/{roleid}'
        response = self.request('PUT', url)
        return response

    def remove_role(self, serverid, userid, roleid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/roles/{roleid}'
        response = self.request('DELETE', url)
        return response

    def get_member_roles(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/roles'
        response = self.request('GET', url)
        return response

    def unban_member(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/bans/{userid}'
        response = self.request('DELETE', url)
        return response

    def get_member_ban(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/bans/{userid}'
        response = self.request('GET', url)
        return response

    def add_group_member(self, groupid, userid):
        url = f'{self.base_url}/groups/{groupid}/members/{userid}'
        response = self.request('PUT', url)
        return response

    def remove_group_member(self, groupid, userid):
        url = f'{self.base_url}/groups/{groupid}/members/{userid}'
        response = self.request('DELETE', url)
        return response

    def get_member_bans(self, serverid):
        url = f'{self.base_url}/servers/{serverid}/bans'
        response = self.request('GET', url)
        return response

    def get_social_link(self, userid, type):
        url = f'{self.base_url}/users/{userid}/social-links/{type}'
        response = self.request('GET', url)
        return response

    def award_xp(self, serverid, userid, amount):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/xp'
        data = {'amount': amount}
        response = self.request('POST', url, json=data)
        return response

    def get_xp(self, serverid, userid):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/xp'
        response = self.request('GET', url)
        return response

    def set_xp(self, serverid, userid, amount):
        url = f'{self.base_url}/servers/{serverid}/members/{userid}/xp'
        data = {'amount': amount}
        response = self.request('PUT', url, json=data)
        return response

    def award_xp_to_role(self, serverid, roleid, amount):
        url = f'{self.base_url}/servers/{serverid}/roles/{roleid}/xp'
        data = {'amount': amount}
        response = self.request('POST', url, json=data)
        return response

    def create_listitem(self, channelid, title, note=None):
        data = {'message': title}
        url = f'{self.base_url}/channels/{channelid}/items'
        if note:
            data.update({'note': {'content': note}})
        response = self.request('POST', url, json=data)
        return response

    def get_listitem(self, channelid, listitemid):
        url = f'{self.base_url}/channels/{channelid}/items/{listitemid}'
        response = self.request('GET', url)
        return response

    def get_listitems(self, channelid):
        url = f'{self.base_url}/channels/{channelid}/items'
        response = self.request('GET', url)
        return response

    def delete_listitem(self, channelid, listitemid):
        url = f'{self.base_url}/channels/{channelid}/items/{listitemid}'
        response = self.request('DELETE', url)
        return response

    def update_listitem(self, channelid, listitemid, title, note=None):
        data = {}
        url = f'{self.base_url}/channels/{channelid}/items/{listitemid}'
        if title:
            data.update({'message': title})
        if note:
            data.update({'note': {'content': note}})
        response = self.request('PUT', url, json=data)
        return response

    def complete_listitem(self, channelid, listitemid):
        url = f'{self.base_url}/channels/{channelid}/items/{listitemid}/complete'
        response = self.request('POST', url)
        return response

    def uncomplete_listitem(self, channelid, listitemid):
        url = f'{self.base_url}/channels/{channelid}/items/{listitemid}/complete'
        response = self.request('DELETE', url)
        return response

    def create_event(self, channelid, title, **args):
        data = {'name': title}
        eurl = f'{self.base_url}/channels/{channelid}/events'
        for key, value in args.items():
            data.update({key: value})
        response = self.request('POST', eurl, json=data)
        return response

    def get_events(self, channelid, before=None, after=None, limit=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events'
        params = {}
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if limit:
            params['limit'] = limit
        response = self.request('GET', url, params=params)
        return response

    def delete_event(self, channelid, eventid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}'
        response = self.request('DELETE', url)
        return response

    def get_calendar_event_rsvp(self, channelid, eventid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/rsvp'
        response = self.request('GET', url)
        return response

    def create_calendar_event_rsvp(self, channelid, eventid, rsvp):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/rsvp'
        data = {'rsvp': rsvp}
        response = self.request('POST', url, json=data)
        return response

    def delete_calendar_event_rsvp(self, channelid, eventid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/rsvp'
        response = self.request('DELETE', url)
        return response

    def get_calendar_event_rsvps(self, channelid, eventid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/rsvps'
        response = self.request('GET', url)
        return response

    def create_webhook(self, serverid, channelid, name):
        url = f'{self.base_url}/servers/{serverid}/webhooks'
        data = {'name': name, 'channelId': channelid}
        response = self.request('POST', url, json=data)
        return response

    def update_webhook(self, serverid, webhookid, name, channelid=None):
        url = f'https://www.guilded.gg/api/v1/servers/{serverid}/webhooks/{webhookid}'
        data = {'name': name}
        if channelid:
            data.update({'channelId': channelid})
        response = self.request('PUT', url, json=data)
        return response

    def delete_webhook(self, serverid, webhookid):
        url = f'https://www.guilded.gg/api/v1/servers/{serverid}/webhooks/{webhookid}'
        response = self.request('DELETE', url)
        return response

    def get_webhook(self, serverid, webhookid):
        url = f'https://www.guilded.gg/api/v1/servers/{serverid}/webhooks/{webhookid}'
        response = self.request('GET', url)
        return response

    def get_webhooks(self, serverid, channelid):
        url = f'https://www.guilded.gg/api/v1/servers/{serverid}/webhooks'
        data = {'channelId': channelid}
        response = self.request('GET', url, params=data)
        return response

    def send_webhook_message(self, serverid, webhookid, content=None, embed=None):
        payload = {}
        webhookinformation = self.get_webhook(serverid, webhookid)
        token = webhookinformation['webhook']['token']
        url = f'https://media.guilded.gg/webhooks/{webhookid}/{token}'
        data = {}
        if content:
            data = {'content': content}
        if embed:
            data = {'embeds': embed.embed}

        self.request('POST', url, json=data)

    def create_forum_post(self, channelid, title, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics'
        data = {}
        if content:
            data = {'title': title, 'content': content}
        if embed:
            data = {'title': title, 'embeds': embed.embed}
        response = self.request('POST', url, json=data)
        return response

    def get_forum_topics(self, channelid, before=None, limit=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics'
        params = {}
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        response = self.request('GET', url, params=params)
        return response

    def get_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}'
        response = self.request('GET', url)
        return response

    def update_forum_topic(self, channelid, forumtopicid, title=None, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}'
        data = {}
        if content:
            data = {'title': title, 'content': content}
        if embed:
            data = {'title': title, 'embeds': embed.embed}

        response = self.request('PATCH', url, json=data)
        return response

    def delete_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}'
        response = self.request('DELETE', url)
        return response

    def pin_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/pin'
        response = self.request('PUT', url)
        return response

    def unpin_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/pin'
        response = self.request('DELETE', url)
        return response

    def lock_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/lock'
        response = self.request('PUT', url)
        return response

    def unlock_forum_topic(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/lock'
        response = self.request('DELETE', url)
        return response

    def create_forum_comment(self, channelid, forumtopicid, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/comments'
        if content:
            data = {'content': content}
        if embed:
            data = {'embeds': embed.embed}

        response = self.request('POST', url, json=data)
        return response

    def get_forum_comments(self, channelid, forumtopicid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/comments'
        response = self.request('GET', url)
        return response

    def get_forum_comment(self, channelid, forumtopicid, forumcommentid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/comments/{forumcommentid}'
        response = self.request('GET', url)
        return response

    def update_forum_comment(self, channelid, forumtopicid, forumcommentid, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/comments/{forumcommentid}'
        data = {}
        if content:
            data = {'content': content}
        if embed:
            data = {'embeds': embed.embed}
        response = self.request('PATCH', url, json=data)
        return response

    def delete_forum_comment(self, channelid, forumtopicid, forumcommentid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{forumtopicid}/comments/{forumcommentid}'
        response = self.request('DELETE', url)
        return response

    def create_reaction(self, channelid, contentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/content/{contentid}/emotes/{emoteid}'
        response = self.request('PUT', url)
        return response

    def delete_reaction(self, channelid, contentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/content/{contentid}/emotes/{emoteid}'
        response = self.request('DELETE', url)
        return response

    def create_topic_reaction(self, channelid, topicid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{topicid}/emotes/{emoteid}'
        response = self.request('PUT', url)
        return response

    def delete_topic_reaction(self, channelid, topicid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{topicid}/emotes/{emoteid}'
        response = self.request('DELETE', url)
        return response

    def create_topic_comment_reaction(self, channelid, topicid, topiccommentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{topicid}/comments/{topiccommentid}/emotes/{emoteid}'
        response = self.request('PUT', url)
        return response

    def delete_topic_comment_reaction(self, channelid, topicid, topiccommentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/topics/{topicid}/comments/{topiccommentid}/emotes/{emoteid}'
        response = self.request('DELETE', url)
        return response

    def create_event_reaction(self, channelid, eventid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/emotes/{emoteid}'
        response = self.request('PUT', url)
        return response

    def delete_event_reaction(self, channelid, eventid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/emotes/{emoteid}'
        response = self.request('DELETE', url)
        return response

    def create_event_comment_reaction(self, channelid, eventid, commentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/comments/{commentid}/emotes/{emoteid}'
        response = self.request('PUT', url)
        return response

    def delete_event_comment_reaction(self, channelid, eventid, commentid, emoteid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/events/{eventid}/comments/{commentid}/emotes/{emoteid}'
        response = self.request('DELETE', url)
        return response

    # here's gonna be more stuff

    def create_doc(self, channelid, title, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs'
        data = {}
        if content:
            data = {'title': title, 'content': content}
        if embed:
            data = {'title': title, 'embeds': embed.embed}

        response = self.request('POST', url, json=data)
        return response

    def get_docs(self, channelid, before=None, limit=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs'
        params = {}
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        response = self.request('GET', url, params=params)
        return response

    def get_doc(self, channelid, docid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}'
        response = self.request('GET', url)
        return response

    def update_doc(self, channelid, docid, title=None, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}'
        data = {}
        if content:
            data = {'title': title, 'content': content}

        if embed:
            data = {'title': title, 'embeds': embed.embed}

        response = self.request('PUT', url, json=data)
        return response

    def delete_doc(self, channelid, docid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}'
        response = self.request('DELETE', url)
        return response

    def create_doc_comment(self, channelid, docid, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}/comments'

        data = {}
        if data:
            data = {'content': content}
        if embed:
            data = {'embeds': embed.embed}

        response = self.request('POST', url, json=data)
        return response

    def update_doc_comment(self, channelid, docid, commentid, content=None, embed=None):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}/comments/{commentid}'
        data = {}
        if content:
            data = {'content': content}
        if embed:
            data = {'embeds': embed.embed}

        response = self.request('PATCH', url, json=data)
        return response

    def delete_doc_comment(self, channelid, docid, commentid):
        url = f'https://www.guilded.gg/api/v1/channels/{channelid}/docs/{docid}/comments/{commentid}'
        response = self.request('DELETE', url)
        return response

    def get_bot_user_id(self):
        response = requests.get(f'https://www.guilded.gg/api/v1/users/@me', headers=self.headers)
        return response.json()['user']['id']


class Embed:
    def __init__(self, title=None, description=None, color=None, author=None, author_url=None, author_icon=None,
                 footer=None, footer_icon=None, thumbnail=None, image=None, fields=None):
        self.embed = {}

        if title:
            self.embed.update({'title': title})

        if description:
            self.embed.update({'description': description})

        if color:
            if isinstance(color, str) and color.startswith("#"):
                color = int(color[1:], 16)
            self.embed.update({'color': color})

        if author or author_url or author_icon:
            author_dict = {}
            if author:
                author_dict.update({'name': author})
            if author_url:
                author_dict.update({'url': author_url})
            if author_icon:
                author_dict.update({'iconUrl': author_icon})
            self.embed.update({'author': author_dict})

        if footer or footer_icon:
            footer_dict = {}
            if footer:
                footer_dict.update({'text': footer})
            if footer_icon:
                footer_dict.update({'iconUrl': footer_icon})
            self.embed.update({'footer': footer_dict})

        if thumbnail:
            self.embed.update({'thumbnail': {'url': thumbnail}})

        if image:
            self.embed.update({'image': {'url': image}})

        if fields:
            self.embed.update({'fields': fields})
        else:
            self.embed.update({'fields': []})

    def add_field(self, title, value):
        self.embed['fields'].append({
            'name': title,
            'value': value
        })


class Message:
    def __init__(self, eventData):
        try:
          self.content = eventData['message']['content']
        except:
          self.content = []
        try:
          self.authorId = eventData['message']['createdBy']
        except:
          self.authorId = []
        try:
          self.channelId = eventData['message']['channelId']
        except:
          self.channelId = []
        try:
          self.guildId = eventData['serverId']
        except:
          self.guildId = []
        try:
          self.messageId = eventData['message']['id']
        except:
          self.messageId = []
        try:
          self.mentions = eventData['message']['mentions']['users']
        except:
          self.mentions = []


class Events:
    def __init__(self, client):
        self._message_create_handlers = []
        self._message_update_handlers = []
        self._message_delete_handlers = []
        self._member_join_handlers = []
        self._member_leave_handlers = []
        self._member_banned_handlers = []
        self._member_unbanned_handlers = []
        self._ready_handlers = []
        self.client = client

    def on_message(self, func):
        @wraps(func)
        def wrapper(message):
            return func(message)

        self._message_create_handlers.append(wrapper)
        return wrapper
      
    async def _handle_create_message(self, eventData):
        message = Message(eventData)
        for handler in self._message_create_handlers:
            await handler(message)
  
    def on_message_update(self, func):
        @wraps(func)
        def wrapper(message):
            return func(message)

        self._message_update_handlers.append(wrapper)
        return wrapper
      
    async def _handle_update_message(self, eventData):
        message = Message(eventData)
        for handler in self._message_update_handlers:
            await handler(message)
            
    def on_message_delete(self, func):
        @wraps(func)
        def wrapper(message):
            return func(message)

        self._message_delete_handlers.append(wrapper)
        return wrapper
      
    async def _handle_delete_message(self, eventData):
        message = Message(eventData)
        for handler in self._message_delete_handlers:
            await handler(message)

    def on_member_join(self, func):
        @wraps(func)
        def wrapper(member):
            return func(member)

        self._member_join_handlers.append(wrapper)
        return wrapper

    async def _handle_member_join(self, eventData):
        for handler in self._member_join_handlers:
            await handler(eventData)

    def on_member_leave(self, func):
        @wraps(func)
        def wrapper(member):
            return func(member)

        self._member_leave_handlers.append(wrapper)
        return wrapper

    async def _handle_member_leave(self, eventData):
        for handler in self._member_leave_handlers:
            await handler(eventData)

    def on_member_banned(self, func):
        @wraps(func)
        def wrapper(member):
            return func(member)
    
        self._member_banned_handlers.append(wrapper)
        return wrapper

    async def _handle_member_banned(self, eventData):
        for handler in self._member_banned_handlers:
            await handler(eventData)

    def on_member_unbanned(self, func):
        @wraps(func)
        def wrapper(member):
            return func(member)
    
        self._member_unbanned_handlers.append(wrapper)
        return wrapper

    async def _handle_member_unbanned(self, eventData):
        for handler in self._member_unbanned_handlers:
            await handler(eventData)

    def on_ready(self, func):
        @wraps(func)
        async def wrapper():
            return await func()

        self._ready_handlers.append(wrapper)
        return wrapper

    async def _handle_ready(self):
        for handler in self._ready_handlers:
            await handler()

    async def start(self):
        async with websockets.connect('wss://www.guilded.gg/websocket/v1',extra_headers={'Authorization': f'Bearer {self.client.token}'}) as websocket:
            await self._handle_ready()
            while True:
                data = await websocket.recv()
                json_data = json.loads(data)
                

                if 't' in json_data and 'd' in json_data:
                    eventType, eventData = json_data['t'], json_data['d']
                else:
                    continue

                event_handlers = {
                  'ChatMessageCreated': self._handle_create_message,
                  'ChatMessageUpdated': self._handle_update_message,
                  'ChatMessageDeleted': self._handle_delete_message,
                  'ServerMemberJoined': self._handle_member_join,
                  'ServerMemberRemoved': self._handle_member_leave,
                  'ServerMemberBanned': self._handle_member_banned,
                  'ServerMemberUnbanned': self._handle_member_unbanned,
                  }
                handler = event_handlers.get(eventType)
                if handler:
                    await handler(eventData)

    def run(self):
        asyncio.run(self.start())

