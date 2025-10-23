# Развертывание WebSocket Чата

## Проблема с GitHub Pages

GitHub Pages может только раздавать статические файлы (HTML, CSS, JS), но не может запускать серверные приложения (Python, Node.js и т.д.). Поэтому WebSocket сервер нужно размещать отдельно.

## Варианты размещения WebSocket сервера

### 1. Heroku (Рекомендуется)

1. **Создайте аккаунт на Heroku**: https://heroku.com
2. **Установите Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Создайте файлы для Heroku**:

#### Procfile
```
web: python working_chat_server.py
```

#### runtime.txt
```
python-3.11.0
```

#### requirements.txt
```
websockets==11.0.3
```

4. **Развертывание**:
```bash
# В папке с проектом
git init
git add .
git commit -m "Initial commit"

# Создайте приложение на Heroku
heroku create your-chat-app-name

# Разверните
git push heroku main
```

5. **Получите URL**: `wss://your-chat-app-name.herokuapp.com`

### 2. Railway

1. **Создайте аккаунт**: https://railway.app
2. **Подключите GitHub репозиторий**
3. **Настройте переменные окружения**:
   - `PORT`: 8765
4. **Получите URL**: `wss://your-app.railway.app`

### 3. Render

1. **Создайте аккаунт**: https://render.com
2. **Создайте новый Web Service**
3. **Подключите репозиторий**
4. **Настройки**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python working_chat_server.py`
5. **Получите URL**: `wss://your-app.onrender.com`

### 4. PythonAnywhere

1. **Создайте аккаунт**: https://pythonanywhere.com
2. **Загрузите файлы через Files**
3. **Создайте Web App** с Flask
4. **Настройте WebSocket** в настройках
5. **Получите URL**: `wss://your-username.pythonanywhere.com`

## Настройка клиента

После развертывания сервера:

1. **Используйте файл `index_hosted.html`** вместо `index.html`
2. **Введите URL вашего WebSocket сервера** в поле "Адрес сервера"
3. **Нажмите "Подключиться к серверу"**

## Примеры URL для разных хостингов

- **Heroku**: `wss://your-app-name.herokuapp.com`
- **Railway**: `wss://your-app.railway.app`
- **Render**: `wss://your-app.onrender.com`
- **PythonAnywhere**: `wss://your-username.pythonanywhere.com`

## Локальное тестирование

Для тестирования на локальном сервере:

1. Запустите `working_chat_server.py`
2. Откройте `index_hosted.html`
3. Введите `ws://localhost:8765` в поле сервера
4. Нажмите "Подключиться к серверу"

## Безопасность

⚠️ **Важно**: При развертывании на публичном хостинге:

1. **Используйте HTTPS/WSS** для безопасности
2. **Добавьте аутентификацию** если нужно
3. **Ограничьте количество подключений**
4. **Добавьте логирование** для мониторинга

## Мониторинг

Добавьте в сервер логирование для отслеживания:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# В методах сервера
logger.info(f"Пользователь {username} присоединился")
```
