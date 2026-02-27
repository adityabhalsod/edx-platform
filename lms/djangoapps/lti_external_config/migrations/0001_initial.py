# Proxy model migration — no new database table is created.

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("lti_consumer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReusableLtiConfiguration",
            fields=[],
            options={
                "proxy": True,
                "verbose_name": "Reusable LTI Configuration",
                "verbose_name_plural": "Reusable LTI Configurations",
            },
            bases=("lti_consumer.lticonfiguration",),
        ),
    ]
