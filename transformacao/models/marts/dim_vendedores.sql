{{ config(materialized='table') }}

SELECT
    seller_id AS id_vendedor,
    seller_city AS cidade,
    seller_state AS estado,
    seller_zip_code_prefix AS prefixo_cep
FROM {{ source('olist', 'sellers') }}