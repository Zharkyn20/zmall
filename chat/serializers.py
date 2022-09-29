from rest_framework import serializers

from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='chat.chat_id', read_only=True)
    sender = serializers.CharField(source='sender.pk', read_only=True)
    sender_name = serializers.CharField(source='sender.__str__', read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    file = serializers.FileField(required=False, allow_empty_file=True, allow_null=True)

    def get_type(self, obj):
        return 'file' if obj.file else 'message'

    class Meta:
        model = Message
        fields = (
            'sender',
            'sender_name',
            'chat',
            'message',
            'send_date',
            'is_read',
            'file',
            'type',
        )


class ChatListSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)
    unread_count = serializers.SerializerMethodField(read_only=True)
    advertisement_name = serializers.CharField(source='advertisement.name', read_only=True)

    def get_unread_count(self, obj):
        messages = Message.objects.exclude(sender=self.context.get('request').user.pk)
        message_count = messages.filter(chat=obj, is_read=False).count()
        return message_count

    def get_message(self, obj):
        instance = Message.objects.filter(chat=obj).last()
        serializer = MessageSerializer(instance)
        data = serializer.data

        if data.get('chat'):
            del data['chat']

        return data

    class Meta:
        model = Chat
        fields = (
            'chat_id',
            'advertisement',
            'advertisement_name',
            'message',
            'unread_count',
        )


class ChatSerializer(serializers.ModelSerializer):
    advertisement_name = serializers.CharField(source='advertisement.name')
    advertisement_price = serializers.IntegerField(source='advertisement.price')
    sender_name = serializers.CharField(source='sender.__str__')
    owner = serializers.IntegerField(source='advertisement.owner.pk')
    owner_name = serializers.CharField(source='advertisement.owner.__str__')

    class Meta:
        model = Chat
        fields = (
            'chat_id',
            'advertisement',
            'advertisement_name',
            'advertisement_price',
            'sender',
            'sender_name',
            'owner',
            'owner_name',
        )
