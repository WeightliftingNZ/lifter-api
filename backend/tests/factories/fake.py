"""Faker settings to be shared amount factories."""

from faker import Faker

Faker.seed(42)
fake = Faker("en_NZ")
