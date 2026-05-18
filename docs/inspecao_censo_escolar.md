# Inspecao inicial - Censo Escolar 2025

## Objetivo

Registrar a primeira analise da base extraida do Censo Escolar 2025, identificando quais arquivos serao usados no ETL de educacao profissional e tecnica.

## Fonte

- Base: Microdados do Censo Escolar 2025
- Orgao: INEP
- Pasta local: `data/raw/microdados_censo_escolar_2025/`
- Arquivo bruto: `data/raw/microdados_censo_escolar_2025_.zip`

Os arquivos brutos ficam em `data/raw/` e nao devem ser versionados no Git, pois podem ser grandes. O repositorio deve guardar os scripts, documentacao e datasets tratados.

## Arquivos encontrados

Na pasta `dados/`, os principais arquivos extraidos foram:

| Arquivo | Tamanho aproximado | Uso potencial |
|---|---:|---|
| `Tabela_Curso_Tecnico_2025.csv` | 2,8 MB | Base principal para cursos tecnicos e matriculas tecnicas por curso |
| `Tabela_Matricula_2025.csv` | 95,3 MB | Base agregada de matriculas por escola e modalidade |
| `Tabela_Escola_2025.csv` | 164,6 MB | Localidade, rede/dependencia, escola e caracteristicas da unidade |
| `Tabela_Turma_2025.csv` | 71,2 MB | Turmas por etapa/modalidade |
| `Tabela_Docente_2025.csv` | 59,6 MB | Docentes |
| `Tabela_Gestor_Escolar_2025.csv` | 25,3 MB | Gestores escolares |

## Decisao inicial de modelagem

Para o primeiro ETL, a melhor base principal e:

**`Tabela_Curso_Tecnico_2025.csv`**

Motivo: ela ja esta diretamente ligada ao tema do projeto e possui colunas especificas de cursos tecnicos, area profissional, curso e quantidade de matriculas.

Para enriquecer a base com territorio e rede, sera feito join com:

**`Tabela_Escola_2025.csv`**

Chaves de ligacao:

- `NU_ANO_CENSO`
- `CO_ENTIDADE`

Resultado da validacao do join:

- Linhas em `Tabela_Curso_Tecnico_2025.csv`: 32.136
- Linhas encontradas na tabela de escola: 32.136
- Linhas sem correspondencia: 0

Ou seja, o join com a tabela de escolas e viavel.

## Colunas importantes

### Tabela_Curso_Tecnico_2025.csv

Colunas candidatas para o dataset final:

| Coluna | Uso previsto |
|---|---|
| `NU_ANO_CENSO` | Ano de referencia |
| `CO_ENTIDADE` | Chave da escola/unidade |
| `NO_AREA_CURSO_PROFISSIONAL` | Area/eixo profissional do curso |
| `ID_AREA_CURSO_PROFISSIONAL` | Codigo da area/eixo profissional |
| `NO_CURSO_EDUC_PROFISSIONAL` | Nome do curso tecnico |
| `CO_CURSO_EDUC_PROFISSIONAL` | Codigo do curso tecnico |
| `QT_CURSO_TEC` | Quantidade de cursos tecnicos |
| `QT_MAT_CURSO_TEC` | Total de matriculas em cursos tecnicos |
| `QT_MAT_CURSO_TEC_IFTP` | Matriculas em itinerario de formacao tecnica e profissional |
| `QT_MAT_CURSO_TEC_NM` | Matriculas em curso tecnico normal/medio, conforme dicionario oficial |
| `QT_MAT_CURSO_TEC_CONC` | Matriculas em curso tecnico concomitante |
| `QT_MAT_CURSO_TEC_SUBS` | Matriculas em curso tecnico subsequente |
| `QT_MAT_CURSO_TEC_IFTP_CT` | Matriculas em curso tecnico associado ao itinerario tecnico-profissional |
| `QT_MAT_CURSO_TEC_EJA` | Matriculas em curso tecnico integrado a EJA |

### Tabela_Escola_2025.csv

Colunas candidatas para dimensao de localidade/rede:

| Coluna | Uso previsto |
|---|---|
| `NU_ANO_CENSO` | Ano de referencia |
| `NO_REGIAO` | Regiao do Brasil |
| `SG_UF` | Sigla da UF |
| `CO_UF` | Codigo da UF |
| `NO_MUNICIPIO` | Nome do municipio |
| `CO_MUNICIPIO` | Codigo do municipio |
| `NO_ENTIDADE` | Nome da escola/unidade |
| `CO_ENTIDADE` | Codigo da escola/unidade |
| `TP_DEPENDENCIA` | Rede/dependencia administrativa |
| `TP_LOCALIZACAO` | Localizacao urbana/rural |

Mapeamento inicial de `TP_DEPENDENCIA`:

| Codigo | Rede |
|---:|---|
| 1 | Federal |
| 2 | Estadual |
| 3 | Municipal |
| 4 | Privada |

Mapeamento inicial de `TP_LOCALIZACAO`:

| Codigo | Localizacao |
|---:|---|
| 1 | Urbana |
| 2 | Rural |

Esses mapeamentos devem ser conferidos no dicionario oficial antes do ETL final.

## Totais iniciais

Total de matriculas em cursos tecnicos em 2025:

**2.490.145 matriculas**

Totais por tipo de coluna de matricula na tabela de curso tecnico:

| Coluna | Total |
|---|---:|
| `QT_MAT_CURSO_TEC` | 2.490.145 |
| `QT_MAT_CURSO_TEC_IFTP` | 1.200.606 |
| `QT_MAT_CURSO_TEC_NM` | 32.529 |
| `QT_MAT_CURSO_TEC_CONC` | 348.446 |
| `QT_MAT_CURSO_TEC_SUBS` | 832.032 |
| `QT_MAT_CURSO_TEC_IFTP_CT` | 19.586 |
| `QT_MAT_CURSO_TEC_EJA` | 56.946 |

Totais por regiao, usando `QT_MAT_CURSO_TEC`:

| Regiao | Matriculas |
|---|---:|
| Sudeste | 1.059.055 |
| Nordeste | 737.597 |
| Sul | 410.821 |
| Centro-Oeste | 142.578 |
| Norte | 140.094 |

Totais por rede/dependencia, usando `QT_MAT_CURSO_TEC`:

| Rede | Matriculas |
|---|---:|
| Estadual | 1.289.453 |
| Privada | 846.095 |
| Federal | 330.505 |
| Municipal | 24.092 |

Top 10 UFs por matriculas tecnicas:

| UF | Matriculas |
|---|---:|
| SP | 574.838 |
| MG | 268.243 |
| BA | 187.131 |
| PR | 174.385 |
| RJ | 154.386 |
| RS | 148.571 |
| CE | 121.510 |
| PI | 106.251 |
| SC | 87.865 |
| PE | 87.848 |

## Encaminhamento para o ETL

O primeiro dataset tratado deve partir de `Tabela_Curso_Tecnico_2025.csv` e fazer join com campos selecionados de `Tabela_Escola_2025.csv`.

Saida inicial sugerida:

`data/processed/fato_matriculas_tecnicas_2025.csv`

Granularidade proposta:

- ano
- escola/unidade
- municipio
- UF
- regiao
- rede
- localizacao
- area/eixo profissional
- curso tecnico

Metricas:

- quantidade de cursos tecnicos
- total de matriculas tecnicas
- matriculas por tipo de oferta tecnica

## Pendencias

- Conferir os mapeamentos de `TP_DEPENDENCIA` e `TP_LOCALIZACAO` no dicionario oficial.
- Definir se o projeto usara apenas 2025 no piloto ou se replicara o ETL para anos anteriores.
- Decidir se a tabela de matricula tambem sera usada para comparar `QT_MAT_PROF_TEC` com `QT_MAT_CURSO_TEC`.
- Avaliar inclusao posterior do IBGE/SIDRA para criar indicador proporcional.

