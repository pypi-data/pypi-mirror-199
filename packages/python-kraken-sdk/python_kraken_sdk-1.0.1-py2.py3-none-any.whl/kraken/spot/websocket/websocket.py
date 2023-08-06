#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# Github: https://github.com/btschwertfeger
#

"""Module that implements the kraken Spot websocket clients"""
import asyncio
import json
import logging
import traceback
from copy import deepcopy
from random import random
from time import time
from typing import List

import websockets

from kraken.exceptions.exceptions import KrakenExceptions
from kraken.spot.ws_client.ws_client import SpotWsClientCl


class ConnectSpotWebsocket:
    """
    This class is only called by the KrakenSpotWSClientCl class
    to establish and handle a websocket connection.

    ====== P A R A M E T E R S ======
    client: kraken.spot.client.KrakenSpotWSClient
        the websocket client
    endpoint: str
        endpoint/url to connect with
    callback: function [optional], default=None
        callback function to call when a message is received
    private: bool [optional], default=False
        if client is authenticated to send signed messages
        and get private feeds

    """

    MAX_RECONNECT_NUM = 10

    def __init__(self, client, endpoint: str, callback, is_auth: bool = False):
        self.__client = client
        self.__ws_endpoint = endpoint
        self.__callback = callback

        self.__reconnect_num = 0
        self.__ws_conn_details = None

        self.__is_auth = is_auth

        self.__last_ping = None
        self.__socket = None
        self.__subscriptions = []

        asyncio.ensure_future(self.__run_forever(), loop=asyncio.get_running_loop())

    @property
    def subscriptions(self) -> list:
        """Returns the active subscriptions"""
        return self.__subscriptions

    @property
    def is_auth(self) -> bool:
        """Returns true if the connection can access privat endpoints"""
        return self.__is_auth

    async def __run(self, event: asyncio.Event):
        keep_alive = True
        self.__last_ping = time()
        self.__ws_conn_details = (
            None if not self.__is_auth else self.__client.get_ws_token()
        )
        logging.debug(f"Websocket token: {self.__ws_conn_details}")

        async with websockets.connect(
            f"wss://{self.__ws_endpoint}", ping_interval=30
        ) as socket:
            logging.info("Websocket connected!")
            self.__socket = socket

            if not event.is_set():
                await self.send_ping()
                event.set()
            self.__reconnect_num = 0

            while keep_alive:
                if time() - self.__last_ping > 10:
                    await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self.__socket.recv(), timeout=15)
                except asyncio.TimeoutError:  # important
                    await self.send_ping()
                except asyncio.CancelledError:
                    logging.exception("asyncio.CancelledError")
                    keep_alive = False
                    await self.__callback({"error": "asyncio.CancelledError"})
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logging.warning(_msg)
                    else:
                        if "event" in msg:
                            if msg["event"] == "subscriptionStatus" and "status" in msg:
                                # remove/assign un/subscriptions
                                try:
                                    if msg["status"] == "subscribed":
                                        self.__append_subscription(msg)
                                    elif msg["status"] == "unsubscribed":
                                        self.__remove_subscription(msg)
                                    elif msg["status"] == "error":
                                        logging.warning(msg)
                                except AttributeError:
                                    pass
                        await self.__callback(msg)

    async def __run_forever(self) -> None:
        try:
            while True:
                await self.__reconnect()
        except KrakenExceptions.MaxReconnectError:
            await self.__callback(
                {
                    "error": "kraken.exceptions.exceptions.KrakenExceptions.MaxReconnectError"
                }
            )
        except Exception as exc:
            logging.error(f"{exc}: {traceback.format_exc()}")
        finally:
            self.__client.exception_occur = True

    async def __reconnect(self):
        logging.info("Websocket start connect/reconnect")

        self.__reconnect_num += 1
        if self.__reconnect_num >= self.MAX_RECONNECT_NUM:
            raise KrakenExceptions.MaxReconnectError()

        reconnect_wait = self.__get_reconnect_wait(self.__reconnect_num)
        logging.debug(
            f"asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self.__reconnect_num}"
        )
        await asyncio.sleep(reconnect_wait)
        logging.debug("asyncio sleep done")
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(
                self.__recover_subscriptions(event)
            ): self.__recover_subscriptions,
            asyncio.ensure_future(self.__run(event)): self.__run,
        }

        while set(tasks.keys()):
            finished, pending = await asyncio.wait(
                tasks.keys(), return_when=asyncio.FIRST_EXCEPTION
            )
            exception_occur = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    traceback.print_stack()
                    message = f"{task} got an exception {task.exception()}\n {task.get_stack()}"
                    logging.warning(message)
                    for process in pending:
                        logging.warning(f"pending {process}")
                        try:
                            process.cancel()
                        except asyncio.CancelledError:
                            logging.exception("asyncio.CancelledError")
                        logging.warning("Cancel OK")
                    await self.__callback({"error": message})
            if exception_occur:
                break
        logging.warning("reconnect over")

    async def __recover_subscriptions(self, event):
        logging.info(
            f'Recover {"auth" if self.__is_auth else "public"} subscriptions {self.__subscriptions} waiting.'
        )
        await event.wait()

        for sub in self.__subscriptions:
            cpy = deepcopy(sub)
            private = False
            if (
                "subscription" in sub
                and "name" in sub["subscription"]
                and sub["subscription"]["name"] in self.__client.private_sub_names
            ):
                cpy["subscription"]["token"] = self.__ws_conn_details["token"]
                private = True
            await self.send_message(cpy, private=private)
            logging.info(f"{sub} OK")

        logging.info(
            f'Recovering {"auth" if self.__is_auth else "public"} subscriptions {self.__subscriptions} done.'
        )

    async def send_ping(self):
        """Sends ping to Keaken"""
        msg = {
            "event": "ping",
            "reqid": int(time() * 1000),
        }
        await self.__socket.send(json.dumps(msg))
        self.__last_ping = time()

    async def send_message(self, msg, private: bool = False):
        """Sends a message via websocket"""
        if private and not self.__is_auth:
            raise ValueError("Cannot send private message with public websocket.")

        while not self.__socket:
            await asyncio.sleep(0.4)

        msg["reqid"] = int(time() * 1000)
        if private and "subscription" in msg:
            msg["subscription"]["token"] = self.__ws_conn_details["token"]
        elif private:
            msg["token"] = self.__ws_conn_details["token"]
        await self.__socket.send(json.dumps(msg))

    def __append_subscription(self, msg: dict) -> None:
        """ Add a dictionary containing subscription information to list
            This is used to recover when the connection gets interrupted.

            This function should only be called in
            when self.__run receives a msg and the following conditions met:
                'event' in msg                           \
                and msg['event'] == 'subscriptionStatus' \
                and 'status' in msg                      \
                and msg['status'] == 'subscribed'

            ====== P A R A M E T E R S ======
            msg: dict
                must be like: { 'subscription': { 'name': '<placeholder>', 'placeholder': 'placeholder', ... }}
        """
        self.__remove_subscription(msg)  # remove from list, to avoid duplicates
        self.__subscriptions.append(self.__build_subscription(msg))

    def __remove_subscription(self, msg: dict) -> None:
        """ Remove a dictionary containing subscription information from list.

            This function should only be called in
            when self.__run receives a msg and the following conditions met:
                'event' in msg                           \
                and msg['event'] == 'subscriptionStatus' \
                and 'status' in msg                      \
                and msg['status'] == 'unsubscribed'

            ====== P A R A M E T E R S ======
            msg: dict
                must be like: { 'subscription': { 'name': '<placeholder>', 'placeholder': 'placeholder', ... }}
        """
        sub = self.__build_subscription(msg)
        self.__subscriptions = [x for x in self.__subscriptions if x != sub]

    def __build_subscription(self, msg: dict) -> dict:
        sub = {"event": "subscribe"}

        if not "subscription" in msg or "name" not in msg["subscription"]:
            raise ValueError("Cannot remove subscription with missing attributes.")
        if (
            msg["subscription"]["name"] in self.__client.public_sub_names
        ):  # public endpoint
            if "pair" in msg:
                sub["pair"] = (
                    msg["pair"] if isinstance(msg["pair"], list) else [msg["pair"]]
                )
            sub["subscription"] = msg["subscription"]
        elif (
            msg["subscription"]["name"] in self.__client.private_sub_names
        ):  # private endpoint
            sub["subscription"] = {"name": msg["subscription"]["name"]}
        else:
            logging.warning(
                "Feed not implemented. Please contact the python-kraken-sdk package author."
            )
        return sub

    def __get_reconnect_wait(self, attempts: int) -> float:
        return round(random() * min(60 * 3, (2**attempts) - 1) + 1)


class KrakenSpotWSClientCl(SpotWsClientCl):
    """https://docs.kraken.com/websockets/#overview

    Class to access public and (optional)
    private/authenticated websocket connection.

    This class holds up to two websocket connections, one private
    and one public.

    ====== P A R A M E T E R S ======
    key: str, [optional], default: ''
        API Key for the Kraken API
    secret: str, [optional], default: ''
        Secret API Key for the Kraken API
    url: str, [optional], default: ''
        Set a specific/custom url
    callback: async function [optional], default=None
        callback function which receives the websocket messages
    beta: bool [optional], default=False
        use the Kraken beta url

    ====== P R O P E R T I E S ======
    public_sub_names: List[str]
        list of available public subscription names
    private_sub_names: List[str]
        list of available private subscription names
    active_public_subscriptions: [dict]
        list of active public subscriptions
    active_private_subscriptions: [dict]
        list of active private subscriptions

    ====== E X A M P L E ======
    import asyncio
    from kraken.spot.client import KrakenSpotWSClient

    async def main() -> None:
        class Bot(KrakenSpotWSClient):

            async def on_message(self, event) -> None:
                print(event)

        bot = Bot() # unauthenticated
        auth_bot = Bot(key='kraken-api-key', secret='kraken-secret-key') # authenticated

        # ... now call for example subscribe and so on

        while True: await asyncio.sleep(6)

    if __name__ == '__main__':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try: asyncio.run(main())
        except KeyboardInterrupt: loop.close()
    """

    PROD_ENV_URL = "ws.kraken.com"
    AUTH_PROD_ENV_URL = "ws-auth.kraken.com"
    BETA_ENV_URL = "beta-ws.kraken.com"
    AUTH_BETA_ENV_URL = "beta-ws-auth.kraken.com"

    def __init__(
        self,
        key: str = "",
        secret: str = "",
        url: str = "",
        callback=None,
        beta: bool = False,
    ):
        super().__init__(key=key, secret=secret, url=url, sandbox=beta)
        self.__callback = callback
        self.__is_auth = key and secret
        self.exception_occur = False
        self._pub_conn = ConnectSpotWebsocket(
            client=self,
            endpoint=self.PROD_ENV_URL if not beta else self.BETA_ENV_URL,
            is_auth=False,
            callback=self.on_message,
        )

        self._priv_conn = (
            ConnectSpotWebsocket(
                client=self,
                endpoint=self.AUTH_PROD_ENV_URL if not beta else self.AUTH_BETA_ENV_URL,
                is_auth=True,
                callback=self.on_message,
            )
            if self.__is_auth
            else None
        )

    async def on_message(self, msg: dict):
        """Calls the defined callback function (if defined)
        or overload this function

        ====== P A R A M E T E R S ======
        msg: dict
            message received from Kraken via the websocket connection

        ====== N O T E S ======
        Can be overloaded like in the documentation of this class.
        """
        if self.__callback is not None:
            await self.__callback(msg)
        else:
            logging.warning("Received event but no callback is defined")
            print(msg)

    async def subscribe(self, subscription: dict, pair: List[str] = None) -> None:
        """Subscribe to a channel
        https://docs.kraken.com/websockets-beta/#message-subscribe

        ====== P A R A M E T E R S ======
        subscription: dict
            the subscription to subscribe to
        pair: List[str]
            list of asset pairs or list of a single pair

        ====== E X A M P L E ======
        # ... initialize bot as documented on top of this class.
        await bot.subscribe(subscription={"name": ticker}, pair=["XBTUSD", "DOT/EUR"])

        ====== N O T E S ======
        Success or failures are sent over the websocket connection and can be
        received via the on_message callback function.
        """

        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key."')
        private = bool(subscription["name"] in self.private_sub_names)

        payload = {"event": "subscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise ValueError(
                    'Parameter pair must be type of List[str] (e.g. pair=["XBTUSD"])'
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self.__is_auth:
                raise ValueError(
                    "Cannot subscribe to private feeds without valid credentials!"
                )
            if pair is not None:
                raise ValueError(
                    "Cannot subscribe to private endpoint with specific pair!"
                )
            await self._priv_conn.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self._pub_conn.send_message(sub, private=False)

        else:
            await self._pub_conn.send_message(payload, private=False)

    async def unsubscribe(self, subscription: dict, pair: List[str] = None) -> None:
        """Unsubscribe from a topic
        https://docs.kraken.com/websockets/#message-unsubscribe

        ====== P A R A M E T E R S ======
        subscription: dict
            the subscription to unsubscribe from
        pair: List[str]
            list of asset pairs or list of a single pair

        ====== E X A M P L E ======
        # ... initialize bot as documented on top of this class.
        bot.unsubscribe(subscription={"name": ticker}, pair=["XBTUSD", "DOT/EUR"])

        ====== N O T E S ======
        Success or failures are sent over the websocket connection and can be
        received via the on_message callback function.
        """
        if "name" not in subscription:
            raise AttributeError('Subscription requires a "name" key."')
        private = bool(subscription["name"] in self.private_sub_names)

        payload = {"event": "unsubscribe", "subscription": subscription}
        if pair is not None:
            if not isinstance(pair, list):
                raise ValueError(
                    'Parameter pair must be type of List[str] (e.g. pair=["XBTUSD"])'
                )
            payload["pair"] = pair

        if private:  # private == without pair
            if not self.__is_auth:
                raise ValueError(
                    "Cannot unsubscribe from private feeds without valid credentials!"
                )
            if pair is not None:
                raise ValueError(
                    "Cannot unsubscribe from private endpoint with specific pair!"
                )
            await self._priv_conn.send_message(payload, private=True)

        elif pair is not None:  # public with pair
            for symbol in pair:
                sub = deepcopy(payload)
                sub["pair"] = [symbol]
                await self._pub_conn.send_message(sub, private=False)

        else:
            await self._pub_conn.send_message(payload, private=False)

    @property
    def private_sub_names(self) -> List[str]:
        """Returns the private subscription names"""
        return ["ownTrades", "openOrders"]

    @property
    def public_sub_names(self) -> List[str]:
        """Returns the public subscription names"""
        return ["ticker", "spread", "book", "ohlc", "trade", "*"]

    @property
    def active_public_subscriptions(self) -> List[str]:
        """Returns the active public subscriptions"""
        if self._pub_conn is not None:
            return self._pub_conn.subscriptions
        raise ConnectionError("Public connection does not exist!")

    @property
    def active_private_subscriptions(self) -> List[str]:
        """Returns the active private subscriptions"""
        if self._priv_conn is not None:
            return self._priv_conn.subscriptions
        raise ConnectionError("Private connection does not exist!")
