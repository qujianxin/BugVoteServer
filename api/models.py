from django.db import models


class Administration(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.username


class ImageItem(models.Model):
    image = models.ImageField(upload_to="images/")
    desc = models.TextField(blank=True, default="#")


class BugType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Config(models.Model):
    name = models.CharField(max_length=40, unique=True)
    context = models.TextField(blank=True, default="")
    images = models.ManyToManyField(ImageItem, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    phone_number = models.CharField(max_length=11, primary_key=True)
    password = models.CharField(max_length=40)
    school = models.CharField(max_length=40)
    major = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    bug_number = models.PositiveIntegerField(default=0)
    bonus = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.phone_number


class BugRecord(models.Model):
    commit_person = models.ForeignKey(User)
    information = models.TextField()
    bonus = models.PositiveIntegerField(default=0)
    bug_type = models.ForeignKey(BugType)
    have_seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class News(models.Model):
    title = models.TextField()
    author = models.CharField(max_length=40)
    time = models.DateTimeField(auto_now_add=True)
    context = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-time',)
