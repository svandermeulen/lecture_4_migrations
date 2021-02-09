"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/02/2021
"""
from django import template

register = template.Library()


@register.filter(name="get_item")
def get_item(dictionary: dict, key: str):
    return dictionary.get(key)


def main():
    pass


if __name__ == "__main__":
    main()
