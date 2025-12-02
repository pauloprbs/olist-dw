{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ source('olist', 'customers') }}
)

SELECT
    customer_id AS id_cliente_pedido,
    customer_unique_id AS id_cliente_unico,
    customer_city AS cidade,
    customer_state AS estado,
    customer_zip_code_prefix AS prefixo_cep
FROM source