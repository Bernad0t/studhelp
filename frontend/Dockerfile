# Используем node.js для разработки и сборки
FROM node:16 AS builder

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package.json package-lock.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код проекта
COPY . .

# Строим проект для продакшена
RUN npm run build

# Production stage
FROM nginx:alpine

# Указываем рабочую директорию Nginx
WORKDIR /usr/share/nginx/html

# Удаляем дефолтную статику Nginx
RUN rm -rf ./*

# Копируем построенные файлы React
COPY --from=builder /app/build .

# Копируем файл конфигурации Nginx (если требуется)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Указываем рабочий порт
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
