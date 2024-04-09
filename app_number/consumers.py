import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from app_number.models import Statistic, DataItem
from app_number.utils import get_chart_data


class DashboardConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.dashboard_slug = None
        self.room_group_name = None

    async def connect(self):
        # print("Connected")
        dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f"app_numer-{dashboard_slug}"

        await self.channel_layer.group_add(
                self.room_group_name, 
                self.channel_name
            )
        await self.accept()


    async def disconnect(self, close_code):
        # print(f"Disconnected: {close_code}")

        await self.channel_layer.group_discard(
                self.room_group_name, 
                self.channel_name
            )


    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)

        message = json_data["message"]
        sender = json_data["sender"]

        await self.create_data(message, sender)

        await self.channel_layer.group_send(self.room_group_name,{
            'type': 'statistics_message',
            'message': message,
            'sender': sender
        })
        

    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']

        chart_data, chart_labels = await self.get_instance_chart_data()
        if chart_data and chart_labels:
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'chart_data': chart_data,
                'chart_labels': chart_labels
            }))
        else: 
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
            }))


    @database_sync_to_async
    def create_data(self, message, sender):
        obj = Statistic.objects.get(slug=self.dashboard_slug)
        DataItem.objects.create(statistic=obj, value=message, owner=sender)


    @database_sync_to_async
    def get_instance_chart_data(self):
        obj = Statistic.objects.get(slug=self.dashboard_slug)
        chart_data, chart_labels = get_chart_data(obj)
        return chart_data, chart_labels
