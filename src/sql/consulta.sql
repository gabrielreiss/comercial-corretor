SELECT *
FROM localizacao
limit 10
;

SELECT 
COUNT(*),
printf('%.2f', COUNT(*)/34591.0) AS perc
FROM localizacao
;

select DISTINCT bairro from localizacao
where bairro is not NULL
;
--34591

/*
select *
from empresas_filtradas2
where Nome <> `NOME:1`
;



select *
from susep
limit 1
;

select *
from empresas_filtradas2
limit 1
;

select *
from Cnaes
where Cnaes.codigo = 6622300
;

select * from sociosfiltrados limit 1;
select * from Qualificacoes limit 1;
select * from Cnaes limit 1;
select * from Paises limit 1;
select * from Motivos limit 5;
select * from Municipios limit 1;
select * from Simples limit 1;
select * from Naturezas limit 1;

*/
/*
select count(*)
from Estabelecimentos
;
*/

/*
PRAGMA journal_mode=DELETE;
PRAGMA temp_store=MEMORY;

CREATE TABLE sociosfiltrados AS
select 
    Socios.*
from Socios
INNER JOIN susep ON Socios.CNPJBASICO = substr(replace(replace(susep.`CPF/CNPJ`, '.', ''), '/', ''), 1, 8)
;
*/

/*
CREATE TABLE empresas AS
SELECT *
FROM empresas_filtradas2 AS T1
LEFT JOIN Cnaes AS T2 ON T1.CNPJBASICO = T2.codigo
*/


