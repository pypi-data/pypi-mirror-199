# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""A sane Python framework for writing modern Discord bots.

To get started, you will want to initialize an instance of `mable.impl.bot.GatewayBot`
for writing a gateway based bot, `mable.impl.rest_bot.RESTBot` for a REST based bot,
or `mable.impl.rest.RESTApp` if you only need to use the REST API.
"""

from __future__ import annotations

from mable import api
from mable import applications
from mable import events
from mable import files
from mable import impl
from mable import interactions
from mable import snowflakes
from mable import undefined
from mable._about import __author__
from mable._about import __ci__
from mable._about import __copyright__
from mable._about import __coverage__
from mable._about import __discord_invite__
from mable._about import __docs__
from mable._about import __email__
from mable._about import __git_sha1__
from mable._about import __issue_tracker__
from mable._about import __license__
from mable._about import __maintainer__
from mable._about import __url__
from mable._about import __version__
from mable.applications import Application
from mable.applications import ApplicationFlags
from mable.applications import ApplicationRoleConnectionMetadataRecord
from mable.applications import ApplicationRoleConnectionMetadataRecordType
from mable.applications import AuthorizationApplication
from mable.applications import AuthorizationInformation
from mable.applications import ConnectionVisibility
from mable.applications import OAuth2AuthorizationToken
from mable.applications import OAuth2ImplicitToken
from mable.applications import OAuth2Scope
from mable.applications import OwnApplicationRoleConnection
from mable.applications import OwnConnection
from mable.applications import OwnGuild
from mable.applications import PartialOAuth2Token
from mable.applications import Team
from mable.applications import TeamMember
from mable.applications import TeamMembershipState
from mable.applications import TokenType
from mable.audit_logs import *
from mable.channels import *
from mable.colors import *
from mable.colours import *
from mable.commands import *
from mable.components import *
from mable.embeds import *
from mable.emojis import *
from mable.errors import *
from mable.events.base_events import Event
from mable.events.base_events import ExceptionEvent
from mable.events.channel_events import *
from mable.events.guild_events import *
from mable.events.interaction_events import *
from mable.events.lifetime_events import *
from mable.events.member_events import *
from mable.events.message_events import *
from mable.events.reaction_events import *
from mable.events.role_events import *
from mable.events.scheduled_events import *
from mable.events.shard_events import *
from mable.events.typing_events import *
from mable.events.user_events import *
from mable.events.voice_events import *
from mable.files import URL
from mable.files import Bytes
from mable.files import File
from mable.files import LazyByteIteratorish
from mable.files import Pathish
from mable.files import Rawish
from mable.files import Resourceish
from mable.guilds import *
from mable.impl import ClientCredentialsStrategy
from mable.impl import GatewayBot
from mable.impl import RESTApp
from mable.impl import RESTBot
from mable.intents import *
from mable.interactions.base_interactions import *
from mable.interactions.command_interactions import *
from mable.interactions.component_interactions import *
from mable.interactions.modal_interactions import *
from mable.invites import *
from mable.iterators import *
from mable.locales import *
from mable.messages import *
from mable.permissions import *
from mable.presences import *
from mable.scheduled_events import *
from mable.sessions import *
from mable.snowflakes import SearchableSnowflakeish
from mable.snowflakes import SearchableSnowflakeishOr
from mable.snowflakes import Snowflake
from mable.snowflakes import Snowflakeish
from mable.snowflakes import SnowflakeishOr
from mable.snowflakes import SnowflakeishSequence
from mable.snowflakes import Unique
from mable.stickers import *
from mable.templates import *
from mable.traits import *
from mable.undefined import UNDEFINED
from mable.undefined import UndefinedNoneOr
from mable.undefined import UndefinedOr
from mable.undefined import UndefinedType
from mable.users import *
from mable.voices import *
from mable.webhooks import *
