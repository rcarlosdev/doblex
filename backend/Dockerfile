FROM php:8.3-cli

# Instalar dependencias del sistema y extensiones de PHP para PostgreSQL y Laravel
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libzip-dev \
    zip \
    unzip \
    git \
    && docker-php-ext-install pdo pdo_pgsql pgsql bcmath zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Directorio de trabajo
WORKDIR /var/www/html

# Copiar archivos del backend
COPY . .

# Instalar dependencias de Composer optimizadas para producción
RUN composer install --no-dev --optimize-autoloader

# Permisos para storage y bootstrap/cache
RUN chmod -R 777 storage bootstrap/cache

# Puerto expuesto dinámicamente por Render
ENV PORT=10000
EXPOSE ${PORT}

# Comando de inicio
CMD ["sh", "-c", "php artisan config:clear && php artisan serve --host=0.0.0.0 --port=${PORT}"]
