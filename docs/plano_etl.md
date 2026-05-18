# Plano de ETL

## Objetivo da etapa

Preparar bases tratadas, documentadas e prontas para consumo no Power BI.

## Escopo inicial

Comecar pelo Censo Escolar / INEP, usando anos recentes e filtrando registros relacionados a educacao profissional e tecnica.

## Etapas

1. Baixar os arquivos oficiais do Censo Escolar.
2. Registrar a fonte, ano, data de acesso e link de origem.
3. Inspecionar o dicionario de variaveis da base.
4. Identificar campos de ano, UF, municipio, rede, modalidade/tipo de oferta e matricula.
5. Filtrar registros de educacao profissional e tecnica.
6. Padronizar nomes de colunas.
7. Tratar nulos, duplicidades e categorias inconsistentes.
8. Agregar os dados por ano, regiao, UF, municipio, rede e tipo de oferta.
9. Exportar CSVs finais para `data/processed/`.
10. Atualizar o dicionario de dados.
11. Validar totais e consistencia antes de entregar para Power BI.

## Saidas esperadas

- `data/processed/fato_matriculas_tecnicas.csv`
- `data/processed/dim_localidade.csv`
- `data/processed/dim_tempo.csv`
- `data/processed/dim_rede.csv`
- `docs/dicionario_dados.md`

## Criterios de validacao

- As bases tratadas devem abrir corretamente no Power BI.
- As colunas devem ter nomes claros.
- Nao deve haver limpeza pesada pendente no Power Query.
- O total de matriculas deve ser conferido contra agregacoes da base original.
- O dicionario de dados deve explicar as colunas principais.

