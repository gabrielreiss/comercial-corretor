# Projeto para Estratégia de Vendas em Seguros, Previdência e Planos de Saúde

### Base de dados
Os dados foram obtidos da base de corretores da SUSEP, com o cruzamento da base da receita federal e posteriormente com as localizações de latitude e longitude dos CEP's.

### Apresentação dos dados
Os dados são apresentados em um dashboard utilizando a biblioteca streamlit do python.
Os dados foram minerados, tratados e persistidos em sqlite utilizando Python e SQL.

### Planos de negócios
Sabemos que os custos de aquisição de novos clientes podem a ser até 21 vezes mais caro que a renovação de clientes. Podemos fazer um paralelo com o mercado de seguros de Portugal, o estudo de DA SILVA (2018) mostra que o mercado está competitivo e as seguradoras estão focadas em entender e atender às necessidades dos clientes. Isso implica que reter os clientes existentes (renovação) é crucial, pois a competição por novos clientes é acirrada e, portanto, mais custosa.

Seguro é um produto elástico, os clientes são sensíveis ao preço. Isso significa que atrair novos clientes exigirá estratégias de preços competitivas e, potencialmente, descontos e promoções dispendiosas. Manter o relacionamento com os clientes existentes, evitando ações que os afastem (como aumentos de preços inesperados), é uma forma mais econômica de garantir receita.

GUIDI (2018), ressalta que entender o cliente e fazer segmentação aumentar a eficiência na aquisição e conversão de clientes. O estudo foi focado em crédito pessoal, porém podemos também aproveitar a ideia de segmentação e as ferramentas que a ciência de dados, como clusterização e random florest, para diferenciar bons e maus riscos.

Em Silva (2024), foca em análisar os indicadores estratégicos de Custo de Aquisição do Cliente (CAC) e Lifetime Value (LTV), essenciais para avaliar a eficácia dos investimentos em marketing e vendas. Esses indicadores permitem à empresa compreender o valor que cada cliente agrega ao longo do tempo, bem como os custos associados à sua aquisição, possibilitando uma gestão mais precisa e orientada por dados. O CAC é, por definição, o custo para adquirir. O LTV é o valor que esse cliente gera ao longo do tempo. O fato de a empresa estar focando em ambos os indicadores mostra que ela está tentando equilibrar o quanto gasta para conseguir um cliente com o quanto ela vai ganhar com esse cliente no futuro. Se a renovação fosse mais cara, a empresa se preocuparia menos com o LTV. Portanto esse artigo mostra que é mais fácil e mais rentável manter um cliente do que adquirir um novo, ajudar a reduzir o churn e reter clientes.

Portanto é necessário engajar os corretores a participarem da captação de perfis de bons riscos incentiv...(IDEIA CENSURADA, PRECISO PAGAR AS MINHAS CONTAS TAMBÉM).

#### Referências
DA SILVA, Carolina Ferreira Duarte. Modelação da elasticidade do preço na renovação Automóvel. 2018. Dissertação de Mestrado. Universidade de Lisboa (Portugal).

GUIDI, Carlos Eduardo Guglielme. Análise de segmentação aplicada à aquisição de clientes no setor de crédito pessoal. 2018. Tese de Doutorado.

SILVA, Larissa Beatriz Santos. Implementação e Análise de Indicadores Estratégicos de Custo de Aquisição do Cliente (CAC) e LifeTime Value (LTV) Em Uma Empresa de ERP. 2024. 19 f. Trabalho de Conclusão de Curso (Graduação em Gestão da Informação) – Universidade Federal de Uberlândia, Uberlândia, 2024.
