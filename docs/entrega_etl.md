# Entrega da etapa ETL

## Responsavel

Pessoa 1 - Dados e ETL completo.

## Objetivo da etapa

Preparar dados publicos, tratados e documentados para que a etapa seguinte possa importar os CSVs no Power BI e construir a modelagem analitica.

## Fontes usadas

### Censo Escolar 2025 / INEP

Base publica usada como fonte principal do projeto.

Uso:

- cursos tecnicos;
- matriculas tecnicas;
- escolas/unidades;
- municipio;
- UF;
- regiao;
- rede/dependencia administrativa;
- localizacao urbana/rural.

Arquivo bruto usado localmente:

`data/raw/microdados_censo_escolar_2025/`

Observacao: os arquivos brutos do INEP nao sao versionados no GitHub por causa do tamanho. Para reproduzir o ETL, e necessario baixar os microdados no site oficial do INEP e extrair a pasta em `data/raw/`.

### IBGE / SIDRA

Base publica usada para populacao municipal.

Uso:

- populacao residente por municipio;
- calculo de matriculas tecnicas por 100 mil habitantes.

Essa base e coletada automaticamente via API publica do IBGE/SIDRA pelo script `scripts/etl_ibge_populacao_2022.py`.

## Scripts entregues

### 1. `scripts/etl_censo_escolar_2025.py`

Le os arquivos do Censo Escolar 2025:

- `Tabela_Curso_Tecnico_2025.csv`
- `Tabela_Escola_2025.csv`

Processo:

1. le apenas as colunas necessarias;
2. faz join por `NU_ANO_CENSO` e `CO_ENTIDADE`;
3. valida se todas as linhas de curso tecnico encontraram escola;
4. traduz codigos de rede e localizacao;
5. renomeia colunas;
6. exporta o CSV tratado.

Saida:

`data/processed/fato_matriculas_tecnicas_2025.csv`

### 2. `scripts/etl_ibge_populacao_2022.py`

Coleta dados da API SIDRA/IBGE.

Processo:

1. acessa a API publica do SIDRA;
2. baixa populacao residente municipal de 2022;
3. separa municipio e UF;
4. valida duplicidades, nulos e quantidade minima de municipios;
5. exporta o CSV tratado.

Saida:

`data/processed/dim_populacao_municipio_2022.csv`

### 3. `scripts/etl_indicadores_municipais_2025.py`

Cria uma base agregada por municipio.

Processo:

1. le a base de matriculas tecnicas tratada;
2. le a base de populacao municipal;
3. agrega matriculas por municipio;
4. calcula quantidade de cursos, escolas/unidades e cursos distintos;
5. calcula matriculas tecnicas por 100 mil habitantes;
6. exporta o CSV tratado.

Saida:

`data/processed/indicadores_municipais_educacao_tecnica_2025.csv`

## Datasets tratados entregues

| Arquivo | Descricao | Uso esperado |
|---|---|---|
| `data/processed/fato_matriculas_tecnicas_2025.csv` | Base principal de cursos tecnicos e matriculas por escola/curso | Base detalhada para Power BI |
| `data/processed/dim_populacao_municipio_2022.csv` | Populacao residente por municipio | Apoio para indicadores proporcionais |
| `data/processed/indicadores_municipais_educacao_tecnica_2025.csv` | Indicadores agregados por municipio | Mapas, rankings territoriais e taxa por 100 mil habitantes |

## Como a proxima etapa deve usar os dados

A Pessoa 2, responsavel por modelagem e KPIs no Power BI, pode importar diretamente os CSVs em `data/processed/`.

Ela nao precisa rodar Python se os CSVs ja estiverem no repositorio.

Os scripts Python existem para reprodutibilidade, auditoria e atualizacao futura dos dados.

## Como reproduzir o ETL

### 1. Preparar ambiente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Baixar base do INEP

Baixar os microdados do Censo Escolar 2025 no site oficial do INEP e extrair em:

```text
data/raw/microdados_censo_escolar_2025/
```

### 3. Rodar scripts

```powershell
python scripts/etl_censo_escolar_2025.py
python scripts/etl_ibge_populacao_2022.py
python scripts/etl_indicadores_municipais_2025.py
```

## Validacoes realizadas

### Censo Escolar 2025

- Linhas na tabela de cursos tecnicos: 32.136
- Linhas integradas com a tabela de escolas: 32.136
- Linhas sem escola correspondente: 0
- Total de matriculas tecnicas: 2.490.145

### Populacao IBGE/SIDRA

- Municipios na base de populacao: 5.570
- Populacao total: 203.080.756
- Municipios com matriculas tecnicas sem populacao correspondente: 0

### Indicadores municipais

- Municipios com matriculas tecnicas: 3.385
- Total de matriculas tecnicas preservado: 2.490.145
- Indicador criado: `matriculas_tecnicas_por_100_mil_hab`

## Limitacoes

- O Censo Escolar usado nesta entrega cobre o ano de 2025.
- A populacao usada e de 2022, por ser a referencia do Censo Demografico disponivel no SIDRA.
- Municipios pequenos podem apresentar taxa por 100 mil habitantes muito alta. No dashboard, esse indicador deve ser analisado junto com o total absoluto de matriculas.
- Os arquivos brutos do INEP precisam ser baixados manualmente para reproduzir o primeiro ETL.

## Como explicar na apresentacao

O ETL foi dividido em tres partes. Primeiro, usamos a tabela de cursos tecnicos do Censo Escolar como base principal e juntamos com a tabela de escolas para adicionar informacoes de territorio, rede e localizacao. Depois, coletamos dados de populacao municipal pela API publica do IBGE/SIDRA. Por fim, criamos uma base agregada por municipio com matriculas tecnicas e o indicador de matriculas por 100 mil habitantes. Assim, a equipe de Power BI recebe CSVs tratados e prontos para modelagem.

