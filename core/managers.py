from collections import defaultdict
import random

from django.db import models
from django.core.exceptions import ImproperlyConfigured


class ArticleManager(models.Manager):

    def published(self):
        return self.filter(published_at__isnull=False).order_by(
            '-published_at', )

    def next_suggestion(self, article):
        # lazy import to avoid circular import problem
        from .models import Article

        if not isinstance(article, Article):
            raise ImproperlyConfigured("Expected 'Article' instance but instead "
                                       f"received type {type(article)}.")

        # not a query
        qset = self.published()

        # queues two queries: one for the entire qset and one for the prefetch
        # noinspection PyUnresolvedReferences
        qset = (qset
                .filter(category=article.category)
                .exclude(id=article.id)
                .prefetch_related('tags')
                )

        # switch to python to keep queries down
        # query! the two queued queries are now evaluated (queries #1 & #2)
        articles = list(qset)
        if not articles:
            # no other articles with the same category
            # potentially query #3 :(
            return self.published().first()

        # use set so 'intersection' can be used later on (query #3)
        tag_ids = set(article.tags.all().values_list('id', flat=True))

        groups = defaultdict(list)
        for article in articles:
            # be sure to prefetch tags or each lap will hit the db
            # count how many tags from the qset obj are in the base obj

            # a set comprehension must be used here in place of values_list
            #   otherwise a fresh query would be made for each article
            tgt_ids = {tag.id for tag in article.tags.all()}
            intersection = len(set(tag_ids.intersection(tgt_ids)))

            # add article to group based on matching tag count
            groups[intersection].append(article)

        # get group with most matching tags
        best_match = groups[max(groups.keys())]
        # return best_match[0]

        # select an article at random in "best_match" group
        return random.choice(best_match)