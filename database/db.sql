-- 1. Tablas de Referencia (Maestras)
CREATE TABLE roles (
    name TEXT PRIMARY KEY
);

CREATE TABLE order_states (
    state TEXT PRIMARY KEY
);

CREATE TABLE pricing (
    pricing_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- 2. Entidades Principales
CREATE TABLE users (
    user_id UUID PRIMARY KEY, -- Generado en Backend (v7)
    name TEXT NOT NULL,
    mail TEXT NOT NULL UNIQUE,
    pwd TEXT NOT NULL,
    role TEXT REFERENCES roles(name),
    is_active BOOLEAN DEFAULT TRUE,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cards (
    card_id UUID PRIMARY KEY, -- Generado en Backend (v7)
    name TEXT NOT NULL,
    details TEXT NOT NULL,
    is_visible BOOLEAN DEFAULT TRUE,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE card_images (
    img_id UUID PRIMARY KEY, -- Generado en Backend (v7)
    card_id UUID NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE
);

-- 3. Transaccionales
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id),
    card_content TEXT NOT NULL DEFAULT 'Esperando sugerencia',
    to_name TEXT NOT NULL,
    location TEXT NOT NULL,
    reference TEXT,
    details TEXT,
    state TEXT NOT NULL REFERENCES order_states(state),
    pricing_id INTEGER NOT NULL REFERENCES pricing(pricing_id),
    is_visible BOOLEAN DEFAULT TRUE,
    created TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    constancy TEXT,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE
);