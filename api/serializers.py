import hashlib
from api.models import User, Administration, BugRecord, News, Config, ImageItem

__author__ = 'hason'

from rest_framework import serializers


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('name', 'context', 'images')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number', 'password', 'school', 'major', 'name', 'email', 'address', 'created', 'bug_number',
            'bonus', 'rank')

    def create(self, validated_data):
        validated_data['password'] = hashlib.sha1(validated_data.get('password').encode()).hexdigest()  # 加密
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        tmp = validated_data.get('password', None)
        if tmp is not None:
            instance.password = hashlib.sha1(tmp.encode()).hexdigest()
        instance.school = validated_data.get('school', instance.school)
        instance.major = validated_data.get('major', instance.major)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.bug_number = validated_data.get('bug_number', instance.bug_number)
        instance.created = validated_data.get('created', instance.created)
        instance.bonus = validated_data.get('bonus', instance.bonus)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.save()
        return instance


class AdmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        fields = (
            'id', 'username', 'password')

    def create(self, validated_data):
        validated_data['password'] = hashlib.sha1(validated_data.get('password').encode()).hexdigest()  # 加密
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('username', instance.username)
        tmp = validated_data.get('password', None)
        if tmp is not None:
            instance.password = hashlib.sha1(tmp.encode()).hexdigest()
        instance.save()
        return instance


class BugRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugRecord
        fields = (
            'id', 'commit_person', 'information', 'bonus', 'bug_type', 'have_seen', "created"
        )

    def create(self, validated_data):
        return BugRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.commit_person = validated_data.get('commit_person', instance.commit_person)
        instance.information = validated_data.get('information', instance.information)
        tmp = validated_data.get('bonus', None)
        if tmp is not None:
            user = instance.commit_person
            if instance.bonus == 0 and tmp != 0:
                user.bug_number += 1
            elif instance.bonus != 0 and tmp == 0:
                user.bug_number -= 1
            user.bonus += tmp - instance.bonus
            instance.bonus = tmp
            user.save()
        instance.bug_type = validated_data.get('bug_type', instance.bug_type)
        instance.have_seen = validated_data.get('have_seen', instance.have_seen)
        instance.save()
        return instance


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            'id', 'title', 'author', 'time', 'context'
        )


class ImageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItem
        fields = (
            'id', 'image', 'desc'
        )
