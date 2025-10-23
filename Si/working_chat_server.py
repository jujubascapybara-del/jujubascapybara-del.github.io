#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import websockets
import json
import datetime

class WorkingChatServer:
    def __init__(self):
        self.clients = set()
        self.usernames = {}

    async def register_client(self, websocket):
        """Регистрация нового клиента"""
        self.clients.add(websocket)
        print(f"Новый клиент подключен. Всего клиентов: {len(self.clients)}")

    async def unregister_client(self, websocket):
        """Отключение клиента"""
        if websocket in self.clients:
            self.clients.remove(websocket)
            if websocket in self.usernames:
                username = self.usernames[websocket]
                del self.usernames[websocket]
                await self.broadcast_user_left(username)
        print(f"Клиент отключен. Всего клиентов: {len(self.clients)}")

    async def handle_message(self, websocket, message):
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
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")

    async def handle_join(self, websocket, data):
        """Обработка присоединения пользователя"""
        username = data.get('username', '').strip()
        print(f"Пользователь присоединяется: {username}")
        
        if not username:
            await self.send_error(websocket, "Имя пользователя не может быть пустым")
            return
            
        if len(username) > 20:
            await self.send_error(websocket, "Имя пользователя слишком длинное")
            return
            
        # Проверяем, не занято ли имя
        if username in self.usernames.values():
            await self.send_error(websocket, f"Имя '{username}' уже занято")
            return
            
        # Регистрируем пользователя
        self.usernames[websocket] = username
        
        # Отправляем приветствие
        welcome_message = {
            "type": "welcome",
            "username": username,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        try:
            await websocket.send(json.dumps(welcome_message, ensure_ascii=False))
            print(f"Приветствие отправлено пользователю {username}")
            
            # Уведомляем других пользователей
            await self.broadcast_user_joined(username)
        except Exception as e:
            print(f"Ошибка отправки приветствия: {e}")

    async def handle_chat_message(self, websocket, data):
        """Обработка сообщения чата"""
        if websocket not in self.usernames:
            await self.send_error(websocket, "Сначала введите ваше имя")
            return
            
        message = data.get('message', '').strip()
        username = self.usernames[websocket]
        
        if not message:
            return
            
        if len(message) > 500:
            await self.send_error(websocket, "Сообщение слишком длинное")
            return
        
        print(f"Сообщение от {username}: {message}")
        
        # Отправляем сообщение всем клиентам
        message_data = {
            "type": "message",
            "username": username,
            "message": message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        await self.broadcast_message(message_data)

    async def handle_typing(self, websocket, data):
        """Обработка индикатора печати"""
        if websocket not in self.usernames:
            return
            
        username = self.usernames[websocket]
        
        # Уведомляем других пользователей
        typing_data = {
            "type": "typing",
            "username": username
        }
        
        await self.broadcast_typing(typing_data, exclude=websocket)

    async def send_error(self, websocket, error_message):
        """Отправка ошибки клиенту"""
        error_data = {
            "type": "error",
            "message": error_message
        }
        try:
            await websocket.send(json.dumps(error_data, ensure_ascii=False))
        except Exception as e:
            print(f"Ошибка отправки ошибки: {e}")

    async def broadcast_message(self, message_data):
        """Отправка сообщения всем клиентам"""
        if not self.clients:
            return
            
        message_json = json.dumps(message_data, ensure_ascii=False)
        disconnected = set()
        
        for client in self.clients:
            try:
                await client.send(message_json)
            except Exception as e:
                print(f"Ошибка отправки клиенту: {e}")
                disconnected.add(client)
                
        # Удаляем отключенных клиентов
        for client in disconnected:
            await self.unregister_client(client)

    async def broadcast_typing(self, typing_data, exclude=None):
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
            except Exception as e:
                print(f"Ошибка отправки индикатора печати: {e}")
                disconnected.add(client)
                
        # Удаляем отключенных клиентов
        for client in disconnected:
            await self.unregister_client(client)

    async def broadcast_user_joined(self, username):
        """Уведомление о присоединении пользователя"""
        message_data = {
            "type": "user_joined",
            "username": username,
            "timestamp": datetime.datetime.now().isoformat()
        }
        await self.broadcast_message(message_data)

    async def broadcast_user_left(self, username):
        """Уведомление о выходе пользователя"""
        message_data = {
            "type": "user_left",
            "username": username,
            "timestamp": datetime.datetime.now().isoformat()
        }
        await self.broadcast_message(message_data)

    async def handle_client(self, websocket, path):
        """Обработка подключения клиента"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print("Соединение закрыто клиентом")
        except Exception as e:
            print(f"Ошибка обработки клиента: {e}")
        finally:
            await self.unregister_client(websocket)

    async def start_server(self, host="localhost", port=8765):
        """Запуск сервера"""
        print(f"Запуск WebSocket сервера на {host}:{port}")
        print("Для остановки нажмите Ctrl+C")
        
        async with websockets.serve(self.handle_client, host, port):
            await asyncio.Future()  # Запуск навсегда

def main():
    """Главная функция"""
    server = WorkingChatServer()
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")

if __name__ == "__main__":
    main()
