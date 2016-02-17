import factory
from users import models
from random import randint


class UsersFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.User

    uid = factory.LazyAttribute(
        lambda s: "{}".format(randint(0, 99999999999999)))

    username = factory.LazyAttribute(
        lambda s: "{}".format(randint(0, 99999999999999)))

    first_name = 'Leo'
    last_name = 'Nnc'
