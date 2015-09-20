# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


def create_initial_structure(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    HomePage = apps.get_model('home.HomePage')
    Blog = apps.get_model('blog.Blog')

    page_content_type, created = ContentType.objects.get_or_create(
        model='page',
        app_label='wagtailcore',
    )

    Blog.objects.create(
        title='Bitbureauet Blog',
        slug='blog',
        content_type=page_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/home/blog/',
    )

    homepage = HomePage.objects.get()
    homepage.numchild = 1
    homepage.save(update_fields=['numchild'])


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('home', '0002_create_homepage')
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.TextField()),
                ('body', wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),
                ('main_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RelatedLink',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('title', models.CharField(help_text='Link title', max_length=255)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('link_page', models.ForeignKey(null=True, blank=True, to='wagtailcore.Page', related_name='+')),
                ('page', modelcluster.fields.ParentalKey(to='blog.BlogPost', related_name='related_links')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.RunPython(create_initial_structure),
    ]
