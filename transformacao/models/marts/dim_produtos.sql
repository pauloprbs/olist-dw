{{ config(materialized='table') }}

WITH produtos AS (
    SELECT * FROM {{ source('olist', 'products') }}
),
traducao AS (
    SELECT * FROM {{ source('olist', 'product_category_name_translation') }}
)

SELECT
    p.product_id AS id_produto,
    COALESCE(t.product_category_name_english, p.product_category_name, 'N/A') AS categoria,
    p.product_photos_qty AS qtd_fotos,
    p.product_weight_g AS peso_g,
    p.product_length_cm AS comprimento_cm,
    p.product_height_cm AS altura_cm,
    p.product_width_cm AS largura_cm
FROM produtos p
LEFT JOIN traducao t
    ON p.product_category_name = t.product_category_name