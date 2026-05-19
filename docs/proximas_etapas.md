# Proximas etapas do projeto

Este documento orienta a continuidade do projeto apos a entrega da etapa de dados e ETL.

## Estado atual do projeto

A etapa de dados/ETL ja entregou os CSVs tratados em `data/processed/`, prontos para serem importados no Power BI.

Arquivos disponiveis:

| Arquivo | Descricao | Principal uso |
|---|---|---|
| `data/processed/fato_matriculas_tecnicas_2025.csv` | Base detalhada de cursos tecnicos, escolas, territorio, rede e matriculas | Modelo principal do Power BI |
| `data/processed/dim_populacao_municipio_2022.csv` | Populacao residente por municipio via IBGE/SIDRA | Indicadores proporcionais |
| `data/processed/indicadores_municipais_educacao_tecnica_2025.csv` | Base agregada por municipio com taxa por 100 mil habitantes | Mapas e rankings territoriais |

Documentos de apoio:

| Documento | Uso |
|---|---|
| `docs/entrega_etl.md` | Explica a entrega da etapa de ETL |
| `docs/dicionario_dados.md` | Descreve as colunas dos datasets tratados |
| `docs/fontes_dados.md` | Lista as fontes publicas usadas |
| `docs/inspecao_censo_escolar.md` | Registra a inspecao inicial da base do INEP |

## Divisao das proximas etapas

## Pessoa 2 - Modelagem e KPIs no Power BI

### Objetivo

Criar o arquivo base do Power BI, importar os datasets tratados, organizar o modelo e criar as medidas/KPIs principais.

### Arquivos que deve usar

Importar no Power BI:

- `data/processed/fato_matriculas_tecnicas_2025.csv`
- `data/processed/dim_populacao_municipio_2022.csv`
- `data/processed/indicadores_municipais_educacao_tecnica_2025.csv`

### O que fazer

1. Criar o arquivo Power BI principal em `dashboard/`.
2. Importar os tres CSVs tratados.
3. Conferir tipos de dados:
   - codigos como numero inteiro ou texto, conforme a necessidade;
   - metricas como numero inteiro/decimal;
   - campos categoricos como texto.
4. Criar relacionamentos quando necessario:
   - `fato_matriculas_tecnicas_2025[codigo_municipio]` com `dim_populacao_municipio_2022[codigo_municipio]`;
   - `fato_matriculas_tecnicas_2025[codigo_municipio]` com `indicadores_municipais_educacao_tecnica_2025[codigo_municipio]`, se fizer sentido no modelo.
5. Criar medidas DAX principais.
6. Criar um tema visual base: cores, fontes, cards e padrao de filtros.
7. Salvar o arquivo `.pbix` em `dashboard/`.

### KPIs sugeridos

Medidas recomendadas:

- Total de matriculas tecnicas.
- Total de cursos tecnicos.
- Total de escolas/unidades com curso tecnico.
- Total de cursos distintos.
- Matriculas por 100 mil habitantes.
- Participacao por rede.
- Participacao por regiao.
- Participacao por area profissional.

Exemplos de formulas DAX:

```DAX
Total Matriculas Tecnicas =
SUM(fato_matriculas_tecnicas_2025[matriculas_cursos_tecnicos])
```

```DAX
Total Cursos Tecnicos =
SUM(fato_matriculas_tecnicas_2025[qtd_cursos_tecnicos])
```

```DAX
Escolas com Curso Tecnico =
DISTINCTCOUNT(fato_matriculas_tecnicas_2025[codigo_entidade])
```

```DAX
Cursos Distintos =
DISTINCTCOUNT(fato_matriculas_tecnicas_2025[codigo_curso_educacao_profissional])
```

```DAX
Matriculas por 100 mil hab =
DIVIDE(
    SUM(indicadores_municipais_educacao_tecnica_2025[matriculas_cursos_tecnicos]),
    SUM(indicadores_municipais_educacao_tecnica_2025[populacao_residente])
) * 100000
```

### Entregaveis

- `dashboard/educacao_profissional_tecnica.pbix`
- lista de KPIs/medidas usadas, preferencialmente em `docs/kpis_powerbi.md`
- modelo com relacionamentos revisados
- arquivo base pronto para Pessoas 3 e 4 criarem as paginas

## Pessoa 3 - Dashboard paginas 1 e 2

### Objetivo

Construir as paginas de visao geral e distribuicao territorial no Power BI.

### Pagina 1 - Visao Geral

Deve responder:

- Qual o total de matriculas tecnicas no Brasil?
- Como essas matriculas se distribuem por regiao e UF?
- Quais areas/cursos aparecem com mais matriculas?
- Quais redes concentram mais oferta?

Visuais sugeridos:

- Cards:
  - Total de matriculas tecnicas;
  - Total de escolas/unidades;
  - Total de cursos distintos;
  - Total de cursos tecnicos.
- Grafico de barras por regiao.
- Ranking de UFs.
- Grafico por rede.
- Grafico por area profissional.
- Filtros:
  - regiao;
  - UF;
  - rede;
  - area profissional.

### Pagina 2 - Distribuicao Territorial

Deve responder:

- Onde a oferta de educacao tecnica esta mais concentrada?
- Quais municipios tem maior volume absoluto?
- Quais municipios tem maior taxa por 100 mil habitantes?

Visuais sugeridos:

- Mapa por UF ou municipio.
- Ranking de municipios por matriculas tecnicas.
- Ranking de municipios por matriculas por 100 mil habitantes.
- Tabela com municipio, UF, matriculas, populacao e taxa.
- Filtros por regiao e UF.

### Cuidados

- A taxa por 100 mil habitantes pode ficar muito alta em municipios pequenos.
- Sempre mostrar a taxa junto com o total absoluto de matriculas.
- Evitar conclusoes fortes baseadas apenas na taxa proporcional.

### Entregaveis

- Paginas 1 e 2 no `.pbix`.
- Prints em `images/dashboard/`.
- 3 a 5 achados preliminares dessas paginas.

## Pessoa 4 - Dashboard paginas 3 e 4

### Objetivo

Construir as paginas de perfil da oferta e analise de areas/cursos.

Observacao: originalmente a pagina 4 poderia usar Plataforma Nilo Pecanha. Como a etapa de ETL atual ainda nao incluiu PNP, a Pessoa 4 deve usar a base do Censo Escolar para analisar areas profissionais e cursos tecnicos. A PNP pode ficar como evolucao futura, caso o grupo decida incluir depois.

### Pagina 3 - Perfil da Oferta

Deve responder:

- Quais redes ofertam mais educacao tecnica?
- Como a oferta se divide entre federal, estadual, municipal e privada?
- A oferta e mais urbana ou rural?
- Quais tipos de curso tecnico concentram mais matriculas?

Visuais sugeridos:

- Barras ou rosca por rede.
- Barras por localizacao urbana/rural.
- Matriculas por tipo:
  - concomitante;
  - subsequente;
  - EJA;
  - itinerario de formacao tecnica e profissional.
- Ranking por rede e UF.
- Filtros por UF, regiao e area profissional.

### Pagina 4 - Areas e Cursos Tecnicos

Deve responder:

- Quais areas profissionais concentram mais matriculas?
- Quais cursos tecnicos tem maior volume?
- Existem diferencas de perfil por regiao ou rede?

Visuais sugeridos:

- Ranking de areas profissionais.
- Ranking de cursos tecnicos.
- Matriz area x regiao.
- Matriz curso x rede.
- Tabela detalhada de cursos.

### Entregaveis

- Paginas 3 e 4 no `.pbix`.
- Prints em `images/dashboard/`.
- 3 a 5 achados preliminares dessas paginas.

## Pessoa 5 - Documentacao, slides, insights e GitHub

### Objetivo

Consolidar a entrega final do projeto, transformar os dados e dashboards em narrativa e garantir que o trabalho siga o roteiro do professor.

### O que fazer

1. Atualizar o README final do projeto.
2. Organizar os prints do dashboard em `images/dashboard/`.
3. Consolidar os insights das quatro paginas do Power BI.
4. Escrever recomendacoes baseadas nos dados.
5. Documentar limitacoes.
6. Montar a apresentacao final em `slides/`.
7. Conferir se os entregaveis pedidos pelo professor estao completos.

### Slides que devem ser cobertos

O roteiro do professor pede:

- Contexto do problema.
- Objetivos.
- Fonte de dados.
- Arquitetura da solucao.
- ETL.
- Modelagem de dados.
- KPIs.
- Construcao do dashboard.
- Demonstracao do dashboard.
- Insights.
- Tomada de decisao/recomendacoes.
- Desafios e limitacoes.
- Conclusao e proximos passos.
- Equipe e entregaveis.

### Entregaveis

- README final.
- Apresentacao final em `slides/`.
- Prints do dashboard.
- Texto de insights.
- Texto de recomendacoes.
- Checklist final dos entregaveis.

## Fluxo recomendado de trabalho

1. Pessoa 2 cria o `.pbix` base com modelo e KPIs.
2. Pessoa 3 cria paginas 1 e 2.
3. Pessoa 4 cria paginas 3 e 4.
4. Pessoa 5 documenta em paralelo, mas finaliza depois dos prints do dashboard.
5. Grupo revisa o dashboard completo.
6. Grupo revisa slides e README.
7. Grupo faz o merge final na `main`.

## Padrao de Git recomendado

Cada pessoa deve trabalhar em uma branch propria:

| Pessoa | Branch sugerida |
|---|---|
| Pessoa 2 | `modelagem-kpis-powerbi` |
| Pessoa 3 | `dashboard-paginas-1-2` |
| Pessoa 4 | `dashboard-paginas-3-4` |
| Pessoa 5 | `docs-slides-insights` |

Evitar commits diretos na `main`.

## Checklist geral antes da entrega

- [ ] CSVs tratados estao em `data/processed/`.
- [ ] Arquivo `.pbix` esta em `dashboard/`.
- [ ] Prints do dashboard estao em `images/dashboard/`.
- [ ] README explica objetivo, fontes, metodologia e como reproduzir.
- [ ] Dicionario de dados esta atualizado.
- [ ] Slides seguem o roteiro do professor.
- [ ] Insights e recomendacoes sao baseados nos dados.
- [ ] Limitacoes estao documentadas.
- [ ] Repositorio esta organizado no GitHub.

