#
# Copyright 2019 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""Model for group management."""
from uuid import uuid4

from django.db import models
from django.utils import timezone
from management.principal.model import Principal
from management.rbac_fields import AutoDateTimeField
from management.role.model import Role


class Group(models.Model):
    """A group."""

    uuid = models.UUIDField(default=uuid4, editable=False,
                            unique=True, null=False)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True)
    principals = models.ManyToManyField(Principal, related_name='group')
    created = models.DateTimeField(default=timezone.now)
    modified = AutoDateTimeField(default=timezone.now)
    platform_default = models.BooleanField(default=False)
    system = models.BooleanField(default=False)

    def roles(self):
        """Roles for a group."""
        return Role.objects.filter(policies__in=self.__policy_ids()).distinct()

    def role_count(self):
        """Role count for a group."""
        return self.roles().count()

    def __policy_ids(self):
        """Policy IDs for a group."""
        return self.policies.values_list('id', flat=True)

    class Meta:
        ordering = ['name', 'modified']
