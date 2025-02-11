SELECT 
    DISTINCT CAST(printf('%09d', CAST(`Número de corretor *` AS INTEGER)) AS STRING) AS COD_SUSEP,
    Nome,
    `CPF/CNPJ` AS CPF_anonimizado
FROM cpf
ORDER BY CAST(printf('%09d', CAST(`Número de corretor *` AS INTEGER)) AS STRING)
;