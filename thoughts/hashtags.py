import re
from typing import List

from django.utils.datastructures import OrderedSet


def unique_hashtags(text: str) -> List[str]:
    hashtags = re.findall('#(\w+)', text)
    return list(OrderedSet(hashtags))
