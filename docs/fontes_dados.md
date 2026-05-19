# Fontes de dados

## 1. Censo Escolar / INEP

Fonte principal do projeto.

- Orgao: INEP
- Tipo: microdados publicos
- Formatos esperados: CSV dentro de arquivos compactados
- Uso no projeto: matriculas, escolas, municipio, UF, rede de ensino e caracteristicas da educacao profissional
- Link: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar

## 2. Plataforma Nilo Pecanha / MEC

Fonte complementar para aprofundar a analise da Rede Federal de Educacao Profissional, Cientifica e Tecnologica.

- Orgao: MEC
- Tipo: dados abertos
- Formatos esperados: CSV, JSON ou arquivos exportados pelo portal
- Uso no projeto: instituicoes, unidades, cursos, eixos tecnologicos e matriculas da Rede Federal
- Link: https://dadosabertos.mec.gov.br/pnp

## 3. IBGE / SIDRA

Fonte complementar para populacao.

- Orgao: IBGE
- Tipo: API/tabelas publicas
- Uso no projeto: calcular indicadores proporcionais, como matriculas tecnicas por 100 mil jovens
- Link: https://sidra.ibge.gov.br/
- Tabela usada no ETL: 4714 - Populacao residente, area territorial e densidade demografica
- Variavel usada no ETL: 93 - Populacao residente
- Periodo usado no ETL: 2022
- Nivel territorial usado no ETL: municipio
- URL da API usada: https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022?formato=json

## 4. RAIS/CAGED

Fonte opcional. Deve ficar como evolucao futura, pois aumenta bastante a complexidade do projeto.

- Orgao: Ministerio do Trabalho e Emprego
- Tipo: microdados publicos
- Uso possivel: relacionar oferta de educacao tecnica com mercado de trabalho formal
- Link: https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho
