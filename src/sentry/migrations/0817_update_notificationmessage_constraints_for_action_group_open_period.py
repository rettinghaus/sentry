# Generated by Django 5.1.5 on 2025-01-16 00:04
import datetime

import django.db.models.functions.comparison
from django.db import migrations, models

from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production.
    # This should only be used for operations where it's safe to run the migration after your
    # code has deployed. So this should not be used for most operations that alter the schema
    # of a table.
    # Here are some things that make sense to mark as post deployment:
    # - Large data migrations. Typically we want these to be run manually so that they can be
    #   monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   run this outside deployments so that we don't block them. Note that while adding an index
    #   is a schema change, it's completely safe to run the operation after the code has deployed.
    # Once deployed, run these manually via: https://develop.sentry.dev/database-migrations/#migration-deployment

    is_post_deployment = True

    dependencies = [
        ("sentry", "0816_add_timestamp_to_group_tombstone"),
        ("workflow_engine", "0022_add_action_group_status_model"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="notificationmessage",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    models.Q(
                        ("incident__isnull", False),
                        ("trigger_action__isnull", False),
                        ("rule_action_uuid__isnull", True),
                        ("rule_fire_history__isnull", True),
                        ("action__isnull", True),
                        ("group__isnull", True),
                        ("open_period_start__isnull", True),
                    ),
                    models.Q(
                        ("incident__isnull", True),
                        ("trigger_action__isnull", True),
                        ("rule_action_uuid__isnull", False),
                        ("rule_fire_history__isnull", False),
                        ("action__isnull", True),
                        ("group__isnull", True),
                    ),
                    models.Q(
                        ("incident__isnull", True),
                        ("trigger_action__isnull", True),
                        ("rule_action_uuid__isnull", True),
                        ("rule_fire_history__isnull", True),
                        ("action__isnull", False),
                        ("group__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="notification_type_mutual_exclusivity",
            ),
        ),
        migrations.AddConstraint(
            model_name="notificationmessage",
            constraint=models.UniqueConstraint(
                models.F("rule_fire_history"),
                models.F("rule_action_uuid"),
                django.db.models.functions.comparison.Coalesce(
                    "open_period_start",
                    models.Value(datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.UTC)),
                ),
                condition=models.Q(
                    ("error_code__isnull", True), ("parent_notification_message__isnull", True)
                ),
                name="singular_parent_message_per_rule_fire_history_rule_action_open_",
            ),
        ),
        migrations.AddConstraint(
            model_name="notificationmessage",
            constraint=models.UniqueConstraint(
                models.F("action"),
                models.F("group"),
                django.db.models.functions.comparison.Coalesce(
                    "open_period_start",
                    models.Value(datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.UTC)),
                ),
                condition=models.Q(
                    ("error_code__isnull", True), ("parent_notification_message__isnull", True)
                ),
                name="singular_parent_message_per_action_group_open_period",
            ),
        ),
        migrations.RemoveConstraint(
            model_name="notificationmessage",
            name="notification_for_issue_xor_metric_alert",
        ),
        migrations.RemoveConstraint(
            model_name="notificationmessage",
            name="singular_parent_message_per_rule_fire_history_and_rule_action",
        ),
    ]
