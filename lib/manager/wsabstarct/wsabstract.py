# import typing as ty
# from fastapi import WebSocket

# class WS:
#     __instance: WebSocket | None = None
#     __message_subscriptions = set()

#     @classmethod
#     def get(cls):
#         if cls.__instance is None:
#             cls.__instance = WebSocket()
