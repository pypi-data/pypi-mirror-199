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
"""Application and entities that are used to describe Users on Discord."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("PartialUser", "User", "OwnUser", "UserFlag", "PremiumType")

import abc
import typing

import attr

from mable import snowflakes
from mable import traits
from mable import undefined
from mable import urls
from mable.internal import attr_extensions
from mable.internal import enums
from mable.internal import routes

if typing.TYPE_CHECKING:
    from mable import channels
    from mable import colors
    from mable import embeds as embeds_
    from mable import files
    from mable import guilds
    from mable import locales
    from mable import messages
    from mable.api import special_endpoints


@typing.final
class UserFlag(enums.Flag):
    """The known user flags that represent account badges."""

    NONE = 0
    """None."""

    DISCORD_EMPLOYEE = 1 << 0
    """Discord Employee."""

    PARTNERED_SERVER_OWNER = 1 << 1
    """Owner of a partnered Discord server."""

    HYPESQUAD_EVENTS = 1 << 2
    """HypeSquad Events."""

    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1."""

    HYPESQUAD_BRAVERY = 1 << 6
    """House of Bravery."""

    HYPESQUAD_BRILLIANCE = 1 << 7
    """House of Brilliance."""

    HYPESQUAD_BALANCE = 1 << 8
    """House of Balance."""

    EARLY_SUPPORTER = 1 << 9
    """Early Supporter."""

    TEAM_USER = 1 << 10
    """Team user."""

    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2."""

    VERIFIED_BOT = 1 << 16
    """Verified Bot."""

    EARLY_VERIFIED_DEVELOPER = 1 << 17
    """Early verified Bot Developer.

    Only applies to users that verified their account before 20th August 2019.
    """

    DISCORD_CERTIFIED_MODERATOR = 1 << 18
    """Discord Certified Moderator."""

    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the active member list."""

    ACTIVE_DEVELOPER = 1 << 22
    """User is an active bot developer."""


@typing.final
class PremiumType(int, enums.Enum):
    """The types of Nitro."""

    NONE = 0
    """No premium."""

    NITRO_CLASSIC = 1
    """Premium including basic perks like animated emojis and avatars."""

    NITRO = 2
    """Premium including all perks (e.g. 2 server boosts)."""


class PartialUser(snowflakes.Unique, abc.ABC):
    """A partial interface for a user.

    Fields may or may not be present, and should be explicitly checked
    before using them to ensure they are not `mable.undefined.UNDEFINED`.

    This is used for endpoints and events that only expose partial user
    information.

    For full user info, consider calling the `fetch_self` method to perform an
    API call.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def app(self) -> traits.RESTAware:
        """Client application that models may use for procedures."""

    @property
    @abc.abstractmethod
    def avatar_hash(self) -> undefined.UndefinedNoneOr[str]:
        """Avatar hash for the user, if they have one, otherwise `None`."""

    @property
    @abc.abstractmethod
    def banner_hash(self) -> undefined.UndefinedNoneOr[str]:
        """Banner hash for the user, if they have one, otherwise `None`."""

    @property
    @abc.abstractmethod
    def accent_color(self) -> undefined.UndefinedNoneOr[colors.Color]:
        """Custom banner color for the user if set, else `None`.

        The official client will decide the default color if not set.
        """

    @property
    def accent_colour(self) -> undefined.UndefinedNoneOr[colors.Color]:
        """Alias for the `accent_color` field."""
        return self.accent_color

    @property
    @abc.abstractmethod
    def discriminator(self) -> undefined.UndefinedOr[str]:
        """Discriminator for the user."""

    @property
    @abc.abstractmethod
    def username(self) -> undefined.UndefinedOr[str]:
        """Username for the user."""

    @property
    @abc.abstractmethod
    def is_bot(self) -> undefined.UndefinedOr[bool]:
        """Whether this user is a bot account."""

    @property
    @abc.abstractmethod
    def is_system(self) -> undefined.UndefinedOr[bool]:
        """Whether  this user is a system account."""

    @property
    @abc.abstractmethod
    def flags(self) -> undefined.UndefinedOr[UserFlag]:
        """Flag bits that are set for the user."""

    @property
    @abc.abstractmethod
    def mention(self) -> str:
        """Return a raw mention string for the given user.

        Examples
        --------
        .. code-block:: python

            >>> some_user.mention
            '<@123456789123456789>'
        """

    async def fetch_dm_channel(self) -> channels.DMChannel:
        """Fetch the DM channel for this user.

        Returns
        -------
        mable.channels.DMChannel
            The requested channel.

        Raises
        ------
        mable.errors.UnauthorizedError
            If you are unauthorized to make the request (invalid/missing token).
        mable.errors.NotFoundError
            If the user is not found.
        mable.errors.RateLimitTooLongError
            Raised in the event that a rate limit occurs that is
            longer than `max_rate_limit` when making a request.
        mable.errors.InternalServerError
            If an internal error occurs on Discord while handling the request.
        """
        return await self.app.rest.create_dm_channel(self.id)

    async def fetch_self(self) -> User:
        """Get this user's up-to-date object by performing an API call.

        Returns
        -------
        mable.users.User
            The requested user object.

        Raises
        ------
        mable.errors.NotFoundError
            If the user is not found.
        mable.errors.RateLimitTooLongError
            Raised in the event that a rate limit occurs that is
            longer than `max_rate_limit` when making a request.
        mable.errors.InternalServerError
            If an internal error occurs on Discord while handling the request.
        """
        return await self.app.rest.fetch_user(user=self.id)

    async def send(
        self,
        content: undefined.UndefinedOr[typing.Any] = undefined.UNDEFINED,
        *,
        attachment: undefined.UndefinedOr[files.Resourceish] = undefined.UNDEFINED,
        attachments: undefined.UndefinedOr[typing.Sequence[files.Resourceish]] = undefined.UNDEFINED,
        component: undefined.UndefinedOr[special_endpoints.ComponentBuilder] = undefined.UNDEFINED,
        components: undefined.UndefinedOr[typing.Sequence[special_endpoints.ComponentBuilder]] = undefined.UNDEFINED,
        embed: undefined.UndefinedOr[embeds_.Embed] = undefined.UNDEFINED,
        embeds: undefined.UndefinedOr[typing.Sequence[embeds_.Embed]] = undefined.UNDEFINED,
        tts: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        reply: undefined.UndefinedOr[snowflakes.SnowflakeishOr[messages.PartialMessage]] = undefined.UNDEFINED,
        reply_must_exist: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        mentions_everyone: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        mentions_reply: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        user_mentions: undefined.UndefinedOr[
            typing.Union[snowflakes.SnowflakeishSequence[PartialUser], bool]
        ] = undefined.UNDEFINED,
        role_mentions: undefined.UndefinedOr[
            typing.Union[snowflakes.SnowflakeishSequence[guilds.PartialRole], bool]
        ] = undefined.UNDEFINED,
        flags: typing.Union[undefined.UndefinedType, int, messages.MessageFlag] = undefined.UNDEFINED,
    ) -> messages.Message:
        """Send a message to this user in DM's.

        Parameters
        ----------
        content : mable.undefined.UndefinedOr[typing.Any]
            If provided, the message contents. If
            `mable.undefined.UNDEFINED`, then nothing will be sent
            in the content. Any other value here will be cast to a
            `str`.

            If this is a `mable.embeds.Embed` and no `embed` nor `embeds` kwarg
            is provided, then this will instead update the embed. This allows
            for simpler syntax when sending an embed alone.

            Likewise, if this is a `mable.files.Resource`, then the
            content is instead treated as an attachment if no `attachment` and
            no `attachments` kwargs are provided.

        Other Parameters
        ----------------
        attachment : mable.undefined.UndefinedOr[mable.files.Resourceish]
            If provided, the message attachment. This can be a resource,
            or string of a path on your computer or a URL.

            Attachments can be passed as many different things, to aid in
            convenience.

            - If a `pathlib.PurePath` or `str` to a valid URL, the
                resource at the given URL will be streamed to Discord when
                sending the message. Subclasses of
                `mable.files.WebResource` such as
                `mable.files.URL`,
                `mable.messages.Attachment`,
                `mable.emojis.Emoji`,
                `EmbedResource`, etc will also be uploaded this way.
                This will use bit-inception, so only a small percentage of the
                resource will remain in memory at any one time, thus aiding in
                scalability.
            - If a `mable.files.Bytes` is passed, or a `str`
                that contains a valid data URI is passed, then this is uploaded
                with a randomized file name if not provided.
            - If a `mable.files.File`, `pathlib.PurePath` or
                `str` that is an absolute or relative path to a file
                on your file system is passed, then this resource is uploaded
                as an attachment using non-blocking code internally and streamed
                using bit-inception where possible. This depends on the
                type of `concurrent.futures.Executor` that is being used for
                the application (default is a thread pool which supports this
                behaviour).
        attachments : mable.undefined.UndefinedOr[typing.Sequence[mable.files.Resourceish]]
            If provided, the message attachments. These can be resources, or
            strings consisting of paths on your computer or URLs.
        component : mable.undefined.UndefinedOr[mable.api.special_endpoints.ComponentBuilder]
            If provided, builder object of the component to include in this message.
        components : mable.undefined.UndefinedOr[typing.Sequence[mable.api.special_endpoints.ComponentBuilder]]
            If provided, a sequence of the component builder objects to include
            in this message.
        embed : mable.undefined.UndefinedOr[mable.embeds.Embed]
            If provided, the message embed.
        embeds : mable.undefined.UndefinedOr[typing.Sequence[mable.embeds.Embed]]
            If provided, the message embeds.
        tts : mable.undefined.UndefinedOr[bool]
            If provided, whether the message will be read out by a screen
            reader using Discord's TTS (text-to-speech) system.
        reply : mable.undefined.UndefinedOr[mable.snowflakes.SnowflakeishOr[mable.messages.PartialMessage]]
            If provided, the message to reply to.
        reply_must_exist : mable.undefined.UndefinedOr[bool]
            If provided, whether to error if the message being replied to does
            not exist instead of sending as a normal (non-reply) message.
            Defaults to `True`.

            This will not do anything if not being used with `reply`.
        mentions_everyone : mable.undefined.UndefinedOr[bool]
            If provided, whether the message should parse @everyone/@here
            mentions.
        mentions_reply : mable.undefined.UndefinedOr[bool]
            If provided, whether to mention the author of the message
            that is being replied to.

            This will not do anything if not being used with `reply`.
        user_mentions : mable.undefined.UndefinedOr[typing.Union[mable.snowflakes.SnowflakeishSequence[mable.users.PartialUser], bool]]
            If provided, and `True`, all user mentions will be detected.
            If provided, and `False`, all user mentions will be ignored
            if appearing in the message body.
            Alternatively this may be a collection of
            `mable.snowflakes.Snowflake`, or
            `mable.users.PartialUser` derivatives to enforce mentioning
            specific users.
        role_mentions : mable.undefined.UndefinedOr[typing.Union[mable.snowflakes.SnowflakeishSequence[mable.guilds.PartialRole], bool]]
            If provided, and `True`, all role mentions will be detected.
            If provided, and `False`, all role mentions will be ignored
            if appearing in the message body.
            Alternatively this may be a collection of
            `mable.snowflakes.Snowflake`, or
            `mable.guilds.PartialRole` derivatives to enforce mentioning
            specific roles.
        flags : mable.undefined.UndefinedOr[mable.messages.MessageFlag]
            If provided, optional flags to set on the message. If
            `mable.undefined.UNDEFINED`, then nothing is changed.

            Note that some flags may not be able to be set. Currently the only
            flags that can be set are `NONE` and `SUPPRESS_EMBEDS`.

        Returns
        -------
        mable.messages.Message
            The created message.

        Raises
        ------
        ValueError
            If more than 100 unique objects/entities are passed for
            `role_mentions` or `user_mentions`.
        TypeError
            If both `attachment` and `attachments` are specified.
        mable.errors.BadRequestError
            This may be raised in several discrete situations, such as messages
            being empty with no attachments or embeds; messages with more than
            2000 characters in them, embeds that exceed one of the many embed
            limits; too many attachments; attachments that are too large;
            invalid image URLs in embeds; `reply` not found or not in the same
            channel; too many components.
        mable.errors.UnauthorizedError
            If you are unauthorized to make the request (invalid/missing token).
        mable.errors.ForbiddenError
            If you are missing the `SEND_MESSAGES` in the channel or the
            person you are trying to message has the DM's disabled.
        mable.errors.NotFoundError
            If the user is not found.
        mable.errors.RateLimitTooLongError
            Raised in the event that a rate limit occurs that is
            longer than `max_rate_limit` when making a request.
        mable.errors.InternalServerError
            If an internal error occurs on Discord while handling the request.
        """  # noqa: E501 - Line too long
        channel_id = None
        if isinstance(self.app, traits.CacheAware):
            channel_id = self.app.cache.get_dm_channel_id(self.id)

        if channel_id is None:
            channel_id = (await self.fetch_dm_channel()).id

        return await self.app.rest.create_message(
            channel=channel_id,
            content=content,
            attachment=attachment,
            attachments=attachments,
            component=component,
            components=components,
            embed=embed,
            embeds=embeds,
            tts=tts,
            reply=reply,
            reply_must_exist=reply_must_exist,
            mentions_everyone=mentions_everyone,
            user_mentions=user_mentions,
            role_mentions=role_mentions,
            mentions_reply=mentions_reply,
            flags=flags,
        )


class User(PartialUser, abc.ABC):
    """Interface for any user-like object.

    This does not include partial users, as they may not be fully formed.
    """

    __slots__: typing.Sequence[str] = ()

    @property
    @abc.abstractmethod
    def app(self) -> traits.RESTAware:
        """Client application that models may use for procedures."""

    @property
    @abc.abstractmethod
    def accent_color(self) -> typing.Optional[colors.Color]:
        """The custom banner color for the user, if set else `None`.

        The official client will decide the default color if not set.
        """

    @property
    def accent_colour(self) -> typing.Optional[colors.Color]:
        """Alias for the `accent_color` field."""
        return self.accent_color

    @property
    @abc.abstractmethod
    def avatar_hash(self) -> typing.Optional[str]:
        """Avatar hash for the user, if they have one, otherwise `None`."""

    @property
    def avatar_url(self) -> typing.Optional[files.URL]:
        """Avatar URL for the user, if they have one set.

        May be `None` if no custom avatar is set. In this case, you
        should use `default_avatar_url` instead.
        """
        return self.make_avatar_url()

    @property
    @abc.abstractmethod
    def banner_hash(self) -> typing.Optional[str]:
        """Banner hash for the user, if they have one, otherwise `None`."""

    @property
    def banner_url(self) -> typing.Optional[files.URL]:
        """Banner URL for the user, if they have one set.

        May be `None` if no custom banner is set.
        """
        return self.make_banner_url()

    @property
    def default_avatar_url(self) -> files.URL:
        """Default avatar URL for this user."""
        return routes.CDN_DEFAULT_USER_AVATAR.compile_to_file(
            urls.CDN_URL,
            discriminator=int(self.discriminator) % 5,
            file_format="png",
        )

    @property
    def display_avatar_url(self) -> files.URL:
        """Display avatar URL for this user."""
        return self.make_avatar_url() or self.default_avatar_url

    @property
    @abc.abstractmethod
    def discriminator(self) -> str:
        """Discriminator for the user."""

    @property
    @abc.abstractmethod
    def flags(self) -> UserFlag:
        """Flag bits that are set for the user."""

    @property
    @abc.abstractmethod
    def is_bot(self) -> bool:
        """Whether this user is a bot account."""

    @property
    @abc.abstractmethod
    def is_system(self) -> bool:
        """Whether this user is a system account."""

    @property
    @abc.abstractmethod
    def mention(self) -> str:
        """Return a raw mention string for the given user.

        Examples
        --------
        .. code-block:: python

            >>> some_user.mention
            '<@123456789123456789>'
        """

    @property
    @abc.abstractmethod
    def username(self) -> str:
        """Username for the user."""

    def make_avatar_url(self, *, ext: typing.Optional[str] = None, size: int = 4096) -> typing.Optional[files.URL]:
        """Generate the avatar URL for this user, if set.

        If no custom avatar is set, this returns `None`. You can then
        use the `default_avatar_url` attribute instead to fetch the displayed
        URL.

        Parameters
        ----------
        ext : typing.Optional[str]
            The ext to use for this URL, defaults to `png` or `gif`.
            Supports `png`, `jpeg`, `jpg`, `webp` and `gif` (when
            animated). Will be ignored for default avatars which can only be
            `png`.

            If `None`, then the correct default extension is
            determined based on whether the icon is animated or not.
        size : int
            The size to set for the URL, defaults to `4096`.
            Can be any power of two between 16 and 4096.
            Will be ignored for default avatars.

        Returns
        -------
        typing.Optional[mable.files.URL]
            The URL to the avatar, or `None` if not present.

        Raises
        ------
        ValueError
            If `size` is not a power of two or not between 16 and 4096.
        """
        if self.avatar_hash is None:
            return None

        if ext is None:
            if self.avatar_hash.startswith("a_"):
                ext = "gif"
            else:
                ext = "png"

        return routes.CDN_USER_AVATAR.compile_to_file(
            urls.CDN_URL,
            user_id=self.id,
            hash=self.avatar_hash,
            size=size,
            file_format=ext,
        )

    def make_banner_url(self, *, ext: typing.Optional[str] = None, size: int = 4096) -> typing.Optional[files.URL]:
        """Generate the banner URL for this user, if set.

        If no custom banner is set, this returns `None`.

        Parameters
        ----------
        ext : typing.Optional[str]
            The ext to use for this URL, defaults to `png` or `gif`.
            Supports `png`, `jpeg`, `jpg`, `webp` and `gif` (when
            animated).

            If `None`, then the correct default extension is
            determined based on whether the banner is animated or not.
        size : int
            The size to set for the URL, defaults to `4096`.
            Can be any power of two between 16 and 4096.

        Returns
        -------
        typing.Optional[mable.files.URL]
            The URL to the banner, or `None` if not present.

        Raises
        ------
        ValueError
            If `size` is not a power of two or not between 16 and 4096.
        """
        if self.banner_hash is None:
            return None

        if ext is None:
            if self.banner_hash.startswith("a_"):
                ext = "gif"
            else:
                ext = "png"

        return routes.CDN_USER_BANNER.compile_to_file(
            urls.CDN_URL,
            user_id=self.id,
            hash=self.banner_hash,
            size=size,
            file_format=ext,
        )


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class PartialUserImpl(PartialUser):
    """Implementation for partial information about a user.

    This is pretty much the same as a normal user, but information may not be
    present, which will be denoted by `mable.undefined.UNDEFINED`.
    """

    id: snowflakes.Snowflake = attr.field(hash=True, repr=True)
    """The ID of this user."""

    app: traits.RESTAware = attr.field(
        repr=False, eq=False, hash=False, metadata={attr_extensions.SKIP_DEEP_COPY: True}
    )
    """Client application that models may use for procedures."""

    discriminator: undefined.UndefinedOr[str] = attr.field(eq=False, hash=False, repr=True)
    """Four-digit discriminator for the user."""

    username: undefined.UndefinedOr[str] = attr.field(eq=False, hash=False, repr=True)
    """Username of the user."""

    avatar_hash: undefined.UndefinedNoneOr[str] = attr.field(eq=False, hash=False, repr=False)
    """Avatar hash of the user, if a custom avatar is set."""

    banner_hash: undefined.UndefinedNoneOr[str] = attr.field(eq=False, hash=False, repr=False)
    """Banner hash of the user, if a custom banner is set."""

    accent_color: undefined.UndefinedNoneOr[colors.Color] = attr.field(eq=False, hash=False, repr=False)
    """The custom banner color for the user, if set.

    The official client will decide the default color if not set.
    """

    is_bot: undefined.UndefinedOr[bool] = attr.field(eq=False, hash=False, repr=True)
    """Whether this user is a bot account."""

    is_system: undefined.UndefinedOr[bool] = attr.field(eq=False, hash=False, repr=True)
    """Whether this user is a system account."""

    flags: undefined.UndefinedOr[UserFlag] = attr.field(eq=False, hash=False, repr=True)
    """Public flags for this user."""

    @property
    def mention(self) -> str:
        """Return a raw mention string for the given user.

        Examples
        --------
        .. code-block:: python

            >>> some_user.mention
            '<@123456789123456789>'
        """
        return f"<@{self.id}>"

    def __str__(self) -> str:
        if self.username is undefined.UNDEFINED or self.discriminator is undefined.UNDEFINED:
            return f"Partial user ID {self.id}"
        return f"{self.username}#{self.discriminator}"


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class UserImpl(PartialUserImpl, User):
    """Concrete implementation of user information."""

    discriminator: str = attr.field(eq=False, hash=False, repr=True)
    """The user's discriminator."""

    username: str = attr.field(eq=False, hash=False, repr=True)
    """The user's username."""

    avatar_hash: typing.Optional[str] = attr.field(eq=False, hash=False, repr=False)
    """The user's avatar hash, if they have one, otherwise `None`."""

    banner_hash: typing.Optional[str] = attr.field(eq=False, hash=False, repr=False)
    """Banner hash of the user, if they have one, otherwise `None`"""

    accent_color: typing.Optional[colors.Color] = attr.field(eq=False, hash=False, repr=False)
    """The custom banner color for the user, if set.

    The official client will decide the default color if not set.
    """

    is_bot: bool = attr.field(eq=False, hash=False, repr=True)
    """`True` if this user is a bot account, `False` otherwise."""

    is_system: bool = attr.field(eq=False, hash=False, repr=True)
    """`True` if this user is a system account, `False` otherwise."""

    flags: UserFlag = attr.field(eq=False, hash=False, repr=True)
    """The public flags for this user."""


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class OwnUser(UserImpl):
    """Represents a user with extended OAuth2 information."""

    is_mfa_enabled: bool = attr.field(eq=False, hash=False, repr=False)
    """Whether the user's account has multi-factor authentication enabled."""

    locale: typing.Optional[typing.Union[str, locales.Locale]] = attr.field(eq=False, hash=False, repr=False)
    """The user's set locale.

    This is not provided in the `READY` event.
    """

    is_verified: typing.Optional[bool] = attr.field(eq=False, hash=False, repr=False)
    """Whether the email for this user's account has been verified.

    Will be `None` if retrieved through the OAuth2 flow without the `email`
    scope.
    """

    email: typing.Optional[str] = attr.field(eq=False, hash=False, repr=False)
    """The user's set email.

    Will be `None` if retrieved through OAuth2 flow without the `email`
    scope. Will always be `None` for bot users.
    """

    premium_type: typing.Union[PremiumType, int, None] = attr.field(eq=False, hash=False, repr=False)
    """The type of Nitro Subscription this user account had.

    This will always be `None` for bots.
    """

    async def fetch_self(self) -> OwnUser:
        """Get this user's up-to-date object.

        Returns
        -------
        mable.users.OwnUser
            The requested user object.

        Raises
        ------
        mable.errors.UnauthorizedError
            If you are unauthorized to make the request (invalid/missing token).
        mable.errors.RateLimitTooLongError
            Raised in the event that a rate limit occurs that is
            longer than `max_rate_limit` when making a request.
        mable.errors.InternalServerError
            If an internal error occurs on Discord while handling the request.
        """
        return await self.app.rest.fetch_my_user()

    async def fetch_dm_channel(self) -> typing.NoReturn:
        raise TypeError("Unable to fetch your own DM channel")

    async def send(
        self,
        content: undefined.UndefinedOr[typing.Any] = undefined.UNDEFINED,
        *,
        attachment: undefined.UndefinedOr[files.Resourceish] = undefined.UNDEFINED,
        attachments: undefined.UndefinedOr[typing.Sequence[files.Resourceish]] = undefined.UNDEFINED,
        component: undefined.UndefinedOr[special_endpoints.ComponentBuilder] = undefined.UNDEFINED,
        components: undefined.UndefinedOr[typing.Sequence[special_endpoints.ComponentBuilder]] = undefined.UNDEFINED,
        embed: undefined.UndefinedOr[embeds_.Embed] = undefined.UNDEFINED,
        embeds: undefined.UndefinedOr[typing.Sequence[embeds_.Embed]] = undefined.UNDEFINED,
        nonce: undefined.UndefinedOr[str] = undefined.UNDEFINED,
        tts: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        reply: undefined.UndefinedOr[snowflakes.SnowflakeishOr[messages.PartialMessage]] = undefined.UNDEFINED,
        reply_must_exist: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        mentions_everyone: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        mentions_reply: undefined.UndefinedOr[bool] = undefined.UNDEFINED,
        user_mentions: undefined.UndefinedOr[
            typing.Union[snowflakes.SnowflakeishSequence[PartialUser], bool]
        ] = undefined.UNDEFINED,
        role_mentions: undefined.UndefinedOr[
            typing.Union[snowflakes.SnowflakeishSequence[guilds.PartialRole], bool]
        ] = undefined.UNDEFINED,
        flags: typing.Union[undefined.UndefinedType, int, messages.MessageFlag] = undefined.UNDEFINED,
    ) -> typing.NoReturn:
        raise TypeError("Unable to send a DM to yourself")
