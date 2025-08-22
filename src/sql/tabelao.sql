SELECT 
    T1.`NOME:1` AS NOME,
    T1.`Número de corretor *` AS SUSEP,
    T1.`CPF/CNPJ` AS CNPJ,
    T1.`Microsseguros`,
    T1.`Planos de Capitalização`,
    T1.`Seguros de Pessoas`,
    T1.`Planos de Previdência Complementar`,
    T1.`Seguros de Danos`,
    T1.`CNPJBASICO`,
    T1.CAPITAL,
    T1.PORTE,
    T1.TIPODELOGRADOURO,
    T1.LOGRADOURO,
    T1.NUMERO,
    T1.COMPLEMENTO,
    T1.BAIRRO,
    CAST(printf('%08d', CAST(T1.CEP AS INTEGER)) AS STRING) AS CEP1,
    T1.UF,
    T4.DESCRICAO,
    T1.DDD1,
    T1.TELEFONE1,
    T1.DDD2,
    T1.TELEFONE2,
    T1.DDDDOFAX,
    T1.FAX,
    T1.CORREIOELETRONICO,
    T5.cep,
    T5.endereco,
    T5.cidade,
    T5.estado,
    T5.latitude,
    T5.longitude

FROM empresas_filtradas2 AS T1
--LEFT JOIN Cnaes AS T2 ON T1.CNAEFISCALPRINCIPAL = T2.codigo
--LEFT JOIN Naturezas AS T3 ON T1.`NATUREZA JURIDICA` = T3.codigo
LEFT JOIN Municipios AS T4 ON T1.MUNICIPIO = T4.codigo
--LEFT JOIN Simples AS T5 ON T1.CNPJBASICO = T5.CNPJBASICO
LEFT JOIN localizacao AS T5 ON printf('%08d', CAST(T1.CEP AS INTEGER)) = T5.cep
;

