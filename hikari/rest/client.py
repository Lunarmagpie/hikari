#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Marshall wrappings for the RESTSession implementation in `hikari.rest.session`.

This provides an object-oriented interface for interacting with discord's RESTSession
API.
"""

from __future__ import annotations

__all__ = ["RESTClient"]

import typing

from hikari import http_settings
from hikari.api import rest_app
from hikari.rest import channel
from hikari.rest import gateway
from hikari.rest import guild
from hikari.rest import invite
from hikari.rest import me
from hikari.rest import oauth2
from hikari.rest import react
from hikari.rest import session
from hikari.rest import user
from hikari.rest import voice
from hikari.rest import webhook


class RESTClient(
    channel.RESTChannelComponent,
    me.RESTCurrentUserComponent,
    gateway.RESTGatewayComponent,
    guild.RESTGuildComponent,
    invite.RESTInviteComponent,
    oauth2.RESTOAuth2Component,
    react.RESTReactionComponent,
    user.RESTUserComponent,
    voice.RESTVoiceComponent,
    webhook.RESTWebhookComponent,
):
    """
    A marshalling object-oriented RESTSession API client.

    This client bridges the basic RESTSession API exposed by
    `hikari.rest.session.RESTSession` and wraps it in a unit of processing that can handle
    handle parsing API objects into Hikari entity objects.

    Parameters
    ----------
    app : hikari.components.application.Application
        The client application that this rest client should be bound by.
        Includes the rest config.

    !!! note
        For all endpoints where a `reason` argument is provided, this may be a
        string inclusively between `0` and `512` characters length, with any
        additional characters being cut off.
    """

    def __init__(
        self,
        *,
        app: rest_app.IRESTApp,
        config: http_settings.HTTPSettings,
        debug: bool,
        token: typing.Optional[str],
        token_type: typing.Optional[str],
        rest_url,
        version,
    ) -> None:
        if token_type is not None:
            token = f"{token_type} {token}"
        super().__init__(
            app,
            session.RESTSession(
                allow_redirects=config.allow_redirects,
                base_url=rest_url,
                connector=config.tcp_connector,
                debug=debug,
                proxy_headers=config.proxy_headers,
                proxy_auth=config.proxy_auth,
                ssl_context=config.ssl_context,
                verify_ssl=config.verify_ssl,
                timeout=config.request_timeout,
                token=token,
                trust_env=config.trust_env,
                version=version,
            ),
        )
