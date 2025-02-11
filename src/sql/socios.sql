SELECT 
    distinct socios.CNPJBASICO,
    empresas.nome AS CORRETORA,
    socios.NOMEDOSOCIO AS SOCIO,
    socios.DESCRICAO AS CARGO 
FROM socios
LEFT JOIN empresas ON socios.CNPJBASICO = empresas.CNPJBASICO
;