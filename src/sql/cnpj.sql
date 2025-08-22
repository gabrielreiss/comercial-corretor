select 
    substr(replace(replace(`CPF/CNPJ`, '.', ''), '/', ''), 1, 8) AS CNPJ_LIMPO
from susep

WHERE `CPF/CNPJ` not like '%*%'
AND `CPF/CNPJ` not NULL
--limit 100
;