from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailadmin.edit_handlers import (
    PageChooserPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class RelatedLink(Orderable, models.Model):
    page = ParentalKey('BlogPost', related_name='related_links')
    title = models.CharField(max_length=255, help_text="Link title")
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        else:
            return self.link_external

    panels = [
        FieldPanel('title'),
        MultiFieldPanel([
            FieldPanel('link_external'),
            PageChooserPanel('link_page'),
        ])
    ]


class BlogPost(Page):
    date = models.DateField("Post date")
    intro = models.TextField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        ImageChooserPanel('main_image'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        InlinePanel('related_links', label='Related links'),
    ]

    def blog(self):
        return self.get_ancestors().type(Blog).last()


class Blog(Page):
    subpage_types = [BlogPost]

    def posts(self):
        return BlogPost.objects.live().descendant_of(self) \
            .order_by('-first_published_at')
