import factory

from django.contrib.auth.models import User
from notes.models import Notes
from django.contrib.auth.hashers import make_password


class userFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user_{n:04}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.LazyFunction(lambda: make_password("password"))


class noteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notes

    title = factory.Faker("sentence", nb_words=3)
    text = factory.Faker("paragraph", nb_sentences=3)
    user = factory.SubFactory(userFactory)