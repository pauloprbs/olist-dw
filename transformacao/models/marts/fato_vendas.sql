{{ config(materialized='table') }}

WITH itens AS (
    SELECT * FROM {{ source('olist', 'order_items') }}
),
pedidos AS (
    SELECT * FROM {{ source('olist', 'orders') }}
)

SELECT
    itens.order_id AS id_pedido,
    itens.order_item_id AS nro_item,
    itens.product_id AS id_produto,
    itens.seller_id AS id_vendedor,
    pedidos.customer_id AS id_cliente_pedido,
    
    TO_CHAR(pedidos.order_purchase_timestamp::DATE, 'YYYYMMDD')::INTEGER AS id_data_compra,
    
    pedidos.order_purchase_timestamp::DATE AS data_pedido, 

    itens.price AS valor_item,
    itens.freight_value AS valor_frete,
    (itens.price + itens.freight_value) AS valor_total,
    
    pedidos.order_status AS status_pedido
FROM itens
JOIN pedidos ON itens.order_id = pedidos.order_id
WHERE pedidos.order_purchase_timestamp IS NOT NULL