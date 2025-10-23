#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import datetime
from typing import Set, Dict, Any

class ChatServer:
    def __init__(self):
        self.clients: Set[Any] = set()
        self.usernames: Dict[Any, str] = {}
        self.typing_users: Set[str] = set()

    async def register_client(self, websocket: Any):
        """Регистрация нового клиента"""
        self.clients.add(websocket)
        print(f"Новый клиент подключен. Всего клиентов: {len(self.clients)}")

    async def unregister_client(self, websocket: Any):
        """Отключение клиента"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            
            # Уведомляем других пользователей о выходе
            if websocket in self.usernames:
                username = self.usernames[websocket]
                del self.usernames[websocket]
                await self.broadcast_user_left(username)
                
        print(f"Клиент отключен. Всего клиентов: {len(self.clients)}")

    async def handle_message(self, websocket: Any, message: str):
        """Обработка сообщения от клиента"""
        try:
            print(f"Получено сообщение: {message}")
            data = json.loads(message)
            message_type = data.get('type')
            print(f"Тип сообщения: {message_type}")
            
            if message_type == 'join':
                await self.handle_join(websocket, data)
            elif message_type == 'message':
                await self.handle_chat_message(websocket, data)
            elif message_type == 'typing':
                await self.handle_typing(websocket, data)
            else:
                print(f"Неизвестный тип сообщения: {message_type}")
                
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON: {e}")
            await self.send_error(websocket, "Неверный формат сообщения")
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")
            await self.send_error(websocket, "Ошибка сервера")

    async def handle_join(self, websocket: Any, data: dict):
        """Обработка присоединения пользователя"""
        username = data.get('username', '').strip()
        
        if not username:
            await self.send_error(websocket, "Имя пользователя не может быть пустым")
            return
            
        if len(username) > 20:
            await self.send_error(websocket, "Имя пользователя слишком длинное (максимум 20 символов)")
            return
            
        # Проверяем, не занято ли имя
        if username in self.usernames.values():
            await self.send_error(websocket, f"Имя '{username}' уже занято")
            return
            
        try:
            # Регистрируем пользователя
            self.usernames[websocket] = username
            
            # Отправляем приветствие
            welcome_message = {
                "type": "welcome",
                "username": username,
                "timestamp": datetime.datetime.now().isoformat()
            }
            await websocket.send(json.dumps(welcome_message, ensure_ascii=False))
            
            # Уведомляем других пользователей
            await self.broadcast_user_joined(username)
        except Exception as e:
            print(f"Ошибка при обработке join: {e}")
            if websocket in self.usernames:
                del self.usernames[websocket]

    async def handle_chat_message(self, websocket: Any, data: dict):
        """Обработка сообщения чата"""
        if websocket not in self.usernames:
            await self.send_error(websocket, "Сначала введите ваше имя")
            return
            
        message = data.get('message', '').strip()
        if not message:
            return
            
        if len(message) > 500:
            await self.send_error(websocket, "Сообщение слишком длинное (максимум 500 символов)")
            return
            
        username = self.usernames[websocket]
        
        # Отправляем сообщение всем клиентам
        message_data = {
            "type": "message",
            "username": username,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        await self.broadcast_message(message_data)

    async def handle_typing(self, websocket: Any, data: dict):
        """Обработка индикатора печати"""
        if websocket not in self.usernames:
            return
            
        username = self.usernames[websocket]
        
        # Добавляем пользователя в список печатающих
        self.typing_users.add(username)
        
        # Уведомляем других пользователей
        typing_data = {
            "type": "typing",
            "username": username
        }
        
        await self.broadcast_typing(typing_data, exclude=websocket)
        
        # Удаляем пользователя из списка печатающих через 3 секунды
        await asyncio.sleep(3)
        self.typing_users.discard(username)

    async def send_error(self, websocket: Any, error_message: str):
        """Отправка ошибки клиенту"""
        error_data = {
            "type": "error",
            "message": error_message
        }
        await websocket.send(json.dumps(error_data, ensure_ascii=False))

    async def broadcast_message(self, message_data: dict):
        """Отправка сообщения всем клиентам"""
        if not self.clients:
            return
            
        message_json = json.dumps(message_data, ensure_ascii=False)
        disconnected = set()
        
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
                
        # Удаляем отключенных клиентов
        for client in disconnected:
            await self.unregister_client(client)

    async def broadcast_typing(self, typing_data: dict, exclude: Any = None):
        """Отправка индикатора печати всем клиентам кроме указанного"""
        if not self.clients:
            return
            
        typing_json = json.dumps(typing_data, ensure_ascii=False)
        disconnected = set()
        
        for client in self.clients:
            if client == exclude:
                continue
                
            try:
                await client.send(typing_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
                
        # Удаляем отключенных клиентов
        for client in disconnected:
            await self.unregister_client(client)

    async def broadcast_user_joined(self, username: str):
        """Уведомление о присоединении пользователя"""
        message_data = {
            "type": "user_joined",
            "username": username,
            "timestamp": datetime.datetime.now().isoformat()
        }
        await self.broadcast_message(message_data)

    async def broadcast_user_left(self, username: str):
        """Уведомление о выходе пользователя"""
        message_data = {
            "type": "user_left",
            "username": username,
            "timestamp": datetime.datetime.now().isoformat()
        }
        await self.broadcast_message(message_data)

    async def handle_client(self, websocket: Any, path: str):
        """Обработка подключения клиента"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)

    async def start_server(self, host: str = "localhost", port: int = 8765):
        """Запуск сервера"""
        print(f"Запуск WebSocket сервера на {host}:{port}")
        print("Для остановки нажмите Ctrl+C")
        
        # Добавляем обработку CORS
        async def handle_client_with_cors(websocket, path):
            # Добавляем заголовки CORS
            try:
                await self.handle_client(websocket, path)
            except Exception as e:
                print(f"Ошибка обработки клиента: {e}")
        
        async with websockets.serve(handle_client_with_cors, host, port, ping_interval=20, ping_timeout=10):
            await asyncio.Future()  # Запуск навсегда

def main():
    """Главная функция"""
    server = ChatServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")

if __name__ == "__main__":
    main()





