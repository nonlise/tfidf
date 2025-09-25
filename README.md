# TF-IDF Analyzer Web Application

## Описание

Это веб-приложение на Flask для анализа текстовых файлов. Оно вычисляет и отображает:

- 50 самых частых слов из загруженного текста
- TF (Term Frequency) - частоту встречаемости слова в документе
- IDF (Inverse Document Frequency) - обратную частоту документа

Приложение имеет простой и интуитивно понятный интерфейс для загрузки файлов и просмотра результатов анализа.

## Основные функции

1. Загрузка текстовых файлов (.txt) через веб-интерфейс
2. Автоматическая обработка текста (удаление пунктуации, приведение к нижнему регистру)
3. Расчет статистических показателей TF и IDF
4. Отображение результатов в виде сортированной таблицы
5. Возможность вернуться к форме загрузки нового файла

## Скриншоты интерфейса

### Страница загрузки файла

[Здесь будет скриншот главной страницы с формой загрузки]

### Страница с результатами анализа

[Здесь будет скриншот таблицы с результатами TF-IDF]

## Как использовать

1. Перейдите на главную страницу приложения
2. Нажмите "Выберите файл" и укажите текстовый файл для анализа
3. Нажмите кнопку "Анализировать"
4. Просмотрите результаты в виде таблицы
5. Для нового анализа нажмите "Назад к форме загрузки"

## Технические детали

Приложение обрабатывает текст следующим образом:
- Удаляет всю пунктуацию
- Приводит слова к нижнему регистру
- Игнорирует стоп-слова (если реализовано)
- Считает частоту каждого слова
- Сортирует слова по частоте встречаемости
- Вычисляет TF и IDF для каждого слова

👨‍💻 Разработано для тестового задания по python+flask(fastapi,django). 🚀
---

⚡ **Автор:** *[nonlise]*  
📅 **Дата создания:** *[31.03.2025]*  

# Концептуальная ER-диаграмма: Система оплаты заказов

## Сущности и их атрибуты

### 1. ПОКУПАТЕЛЬ (CUSTOMER)
**Первичный ключ:** `customer_id`  
**Атрибуты:**
- `email` (VARCHAR, UNIQUE, NOT NULL)
- `phone` (VARCHAR, UNIQUE)
- `first_name` (VARCHAR, NOT NULL)
- `last_name` (VARCHAR, NOT NULL)
- `registration_date` (DATETIME)
- `last_login` (DATETIME)
- `status` (ENUM: 'active', 'inactive', 'blocked')

### 2. ЗАКАЗ (ORDER)
**Первичный ключ:** `order_id`  
**Внешние ключи:**
- `customer_id` → ПОКУПАТЕЛЬ
- `payment_method_id` → СПОСОБ_ОПЛАТЫ

**Атрибуты:**
- `order_number` (VARCHAR, UNIQUE)
- `total_amount` (DECIMAL(10,2))
- `currency` (VARCHAR, DEFAULT 'RUB')
- `order_date` (DATETIME)
- `status` (ENUM: 'created', 'pending', 'paid', 'shipped', 'delivered', 'cancelled')
- `delivery_address` (TEXT)

### 3. ТОВАР (PRODUCT)
**Первичный ключ:** `product_id`  
**Атрибуты:**
- `name` (VARCHAR, NOT NULL)
- `description` (TEXT)
- `price` (DECIMAL(10,2))
- `sku` (VARCHAR, UNIQUE)
- `stock_quantity` (INT)
- `category_id` (INT)

### 4. ПОЗИЦИЯ_ЗАКАЗА (ORDER_ITEM)
**Первичный ключ:** `order_item_id`  
**Внешние ключи:**
- `order_id` → ЗАКАЗ
- `product_id` → ТОВАР

**Атрибуты:**
- `quantity` (INT)
- `unit_price` (DECIMAL(10,2))
- `subtotal` (DECIMAL(10,2))

### 5. ПЛАТЕЖ (PAYMENT)
**Первичный ключ:** `payment_id`  
**Внешние ключи:**
- `order_id` → ЗАКАЗ
- `payment_gateway_id` → ПЛАТЕЖНЫЙ_ШЛЮЗ

**Атрибуты:**
- `transaction_id` (VARCHAR, UNIQUE)
- `amount` (DECIMAL(10,2))
- `payment_date` (DATETIME)
- `status` (ENUM: 'pending', 'processing', 'completed', 'failed', 'refunded')
- `gateway_response` (JSON)

### 6. ПЛАТЕЖНЫЙ_ШЛЮЗ (PAYMENT_GATEWAY)
**Первичный ключ:** `gateway_id`  
**Атрибуты:**
- `name` (VARCHAR) - "ИПА", "CloudPayments", и т.д.
- `api_key` (VARCHAR)
- `secret_key` (VARCHAR)
- `is_active` (BOOLEAN)
- `test_mode` (BOOLEAN)

### 7. СПОСОБ_ОПЛАТЫ (PAYMENT_METHOD)
**Первичный ключ:** `payment_method_id`  
**Атрибуты:**
- `method_name` (VARCHAR) - "Карта", "Электронный кошелек", "Наложенный платеж"
- `description` (TEXT)
- `is_available` (BOOLEAN)

### 8. БАНКОВСКАЯ_КАРТА (BANK_CARD)
**Первичный ключ:** `card_id`  
**Внешние ключи:**
- `customer_id` → ПОКУПАТЕЛЬ

**Атрибуты:**
- `card_number_hash` (VARCHAR) - захешированный номер
- `card_last_four` (VARCHAR(4))
- `expiry_month` (INT)
- `expiry_year` (INT)
- `cardholder_name` (VARCHAR)
- `is_default` (BOOLEAN)

### 9. ЧЕК (RECEIPT)
**Первичный ключ:** `receipt_id`  
**Внешние ключи:**
- `payment_id` → ПЛАТЕЖ

**Атрибуты:**
- `receipt_number` (VARCHAR, UNIQUE)
- `receipt_date` (DATETIME)
- `fiscal_data` (JSON) - фискальные данные
- `email_sent` (BOOLEAN)
- `sms_sent` (BOOLEAN)

### 10. ВОЗВРАТ (REFUND)
**Первичный ключ:** `refund_id`  
**Внешние ключи:**
- `payment_id` → ПЛАТЕЖ

**Атрибуты:**
- `refund_amount` (DECIMAL(10,2))
- `refund_date` (DATETIME)
- `reason` (TEXT)
- `status` (ENUM: 'requested', 'processed', 'completed')

## Связи между сущностями

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--o{ BANK_CARD : has
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in
    ORDER ||--|| PAYMENT : has
    PAYMENT_METHOD ||--o{ ORDER : used_in
    PAYMENT_GATEWAY ||--o{ PAYMENT : processes
    PAYMENT ||--|| RECEIPT : generates
    PAYMENT ||--o{ REFUND : has
    
    CUSTOMER {
        string customer_id PK
        string email UK
        string phone UK
        string first_name
        string last_name
        datetime registration_date
        datetime last_login
        string status
    }
    
    ORDER {
        string order_id PK
        string customer_id FK
        string payment_method_id FK
        string order_number UK
        decimal total_amount
        string currency
        datetime order_date
        string status
        text delivery_address
    }
    
    PRODUCT {
        string product_id PK
        string name
        text description
        decimal price
        string sku UK
        int stock_quantity
        int category_id
    }
    
    ORDER_ITEM {
        string order_item_id PK
        string order_id FK
        string product_id FK
        int quantity
        decimal unit_price
        decimal subtotal
    }
    
    PAYMENT {
        string payment_id PK
        string order_id FK
        string payment_gateway_id FK
        string transaction_id UK
        decimal amount
        datetime payment_date
        string status
        json gateway_response
    }
    
    PAYMENT_GATEWAY {
        string gateway_id PK
        string name
        string api_key
        string secret_key
        boolean is_active
        boolean test_mode
    }
    
    PAYMENT_METHOD {
        string payment_method_id PK
        string method_name
        text description
        boolean is_available
    }
    
    BANK_CARD {
        string card_id PK
        string customer_id FK
        string card_number_hash
        string card_last_four
        int expiry_month
        int expiry_year
        string cardholder_name
        boolean is_default
    }
    
    RECEIPT {
        string receipt_id PK
        string payment_id FK
        string receipt_number UK
        datetime receipt_date
        json fiscal_data
        boolean email_sent
        boolean sms_sent
    }
    
    REFUND {
        string refund_id PK
        string payment_id FK
        decimal refund_amount
        datetime refund_date
        text reason
        string status
    }
