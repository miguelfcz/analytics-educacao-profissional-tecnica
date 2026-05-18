# Dicionario de dados

## Dataset tratado

Arquivo:

`data/processed/fato_matriculas_tecnicas_2025.csv`

## Descricao

Base tratada com informacoes de cursos tecnicos e matriculas tecnicas do Censo Escolar 2025. O dataset foi gerado a partir da juncao entre:

- `Tabela_Curso_Tecnico_2025.csv`
- `Tabela_Escola_2025.csv`

A chave de integracao usada foi:

- `NU_ANO_CENSO`
- `CO_ENTIDADE`

## Granularidade

Cada linha representa um curso tecnico ofertado por uma escola/unidade em 2025, com informacoes territoriais, rede de ensino, localizacao, area profissional, curso e quantidades de matriculas.

## Resumo tecnico

| Indicador | Valor |
|---|---:|
| Linhas | 32.136 |
| Colunas | 22 |
| Total de matriculas tecnicas | 2.490.145 |
| Ano | 2025 |
| Fonte | Censo Escolar / INEP |

## Colunas

| Coluna | Tipo | Descricao | Origem |
|---|---|---|---|
| `ano` | inteiro | Ano de referencia do Censo Escolar. | `NU_ANO_CENSO` |
| `regiao` | texto | Regiao geografica do Brasil onde a escola esta localizada. | `NO_REGIAO` |
| `uf` | texto | Sigla da unidade federativa. | `SG_UF` |
| `codigo_uf` | inteiro | Codigo da unidade federativa no padrao IBGE/INEP. | `CO_UF` |
| `municipio` | texto | Nome do municipio da escola/unidade. | `NO_MUNICIPIO` |
| `codigo_municipio` | inteiro | Codigo do municipio no padrao IBGE/INEP. | `CO_MUNICIPIO` |
| `codigo_entidade` | inteiro | Codigo da escola/unidade no Censo Escolar. | `CO_ENTIDADE` |
| `nome_entidade` | texto | Nome da escola/unidade. | `NO_ENTIDADE` |
| `rede` | texto | Rede/dependencia administrativa da escola: Federal, Estadual, Municipal ou Privada. | `TP_DEPENDENCIA` |
| `localizacao` | texto | Localizacao da escola: Urbana ou Rural. | `TP_LOCALIZACAO` |
| `area_curso_profissional` | texto | Area profissional do curso tecnico. | `NO_AREA_CURSO_PROFISSIONAL` |
| `codigo_area_curso_profissional` | inteiro | Codigo da area profissional do curso tecnico. | `ID_AREA_CURSO_PROFISSIONAL` |
| `curso_educacao_profissional` | texto | Nome do curso de educacao profissional. | `NO_CURSO_EDUC_PROFISSIONAL` |
| `codigo_curso_educacao_profissional` | inteiro | Codigo do curso de educacao profissional. | `CO_CURSO_EDUC_PROFISSIONAL` |
| `qtd_cursos_tecnicos` | inteiro | Quantidade de cursos tecnicos registrados para a escola/curso. | `QT_CURSO_TEC` |
| `matriculas_cursos_tecnicos` | inteiro | Total de matriculas em cursos tecnicos. | `QT_MAT_CURSO_TEC` |
| `matriculas_itinerario_formacao_tecnica_profissional` | inteiro | Matriculas em cursos tecnicos relacionadas ao itinerario de formacao tecnica e profissional. | `QT_MAT_CURSO_TEC_IFTP` |
| `matriculas_curso_tecnico_nivel_medio` | inteiro | Matriculas em curso tecnico de nivel medio, conforme classificacao do Censo Escolar. | `QT_MAT_CURSO_TEC_NM` |
| `matriculas_curso_tecnico_concomitante` | inteiro | Matriculas em curso tecnico concomitante. | `QT_MAT_CURSO_TEC_CONC` |
| `matriculas_curso_tecnico_subsequente` | inteiro | Matriculas em curso tecnico subsequente. | `QT_MAT_CURSO_TEC_SUBS` |
| `matriculas_curso_tecnico_itinerario_ct` | inteiro | Matriculas em curso tecnico associado ao itinerario tecnico-profissional, conforme coluna original do INEP. | `QT_MAT_CURSO_TEC_IFTP_CT` |
| `matriculas_curso_tecnico_eja` | inteiro | Matriculas em curso tecnico integrado ou relacionado a EJA. | `QT_MAT_CURSO_TEC_EJA` |

## Mapeamentos aplicados

### Rede/dependencia administrativa

Coluna original: `TP_DEPENDENCIA`

| Codigo | Valor tratado |
|---:|---|
| 1 | Federal |
| 2 | Estadual |
| 3 | Municipal |
| 4 | Privada |

### Localizacao

Coluna original: `TP_LOCALIZACAO`

| Codigo | Valor tratado |
|---:|---|
| 1 | Urbana |
| 2 | Rural |

## Observacoes

- Os arquivos brutos permanecem em `data/raw/` e nao sao versionados no Git por causa do tamanho.
- O dataset tratado em `data/processed/` pode ser usado diretamente no Power BI.
- A base atual cobre somente o ano de 2025. O ETL pode ser expandido futuramente para outros anos seguindo a mesma logica.

