# Analytics - Educacao Profissional e Tecnica no Brasil

Projeto de analytics e dashboard sobre a distribuicao da educacao profissional e tecnica no Brasil, usando bases publicas e gratuitas.

## Tema

**Educacao Profissional e Tecnica no Brasil**

Titulo sugerido: **Educacao Tecnica no Brasil: onde estao as oportunidades de formacao profissional?**

## Pergunta central

Como a educacao profissional e tecnica esta distribuida no Brasil, e quais desigualdades aparecem por regiao, UF, municipio, rede de ensino e tipo de curso?

## Objetivo

Construir uma solucao de analytics end-to-end para transformar dados publicos em indicadores, dashboard, insights e recomendacoes sobre a oferta de educacao profissional e tecnica no Brasil.

## Fontes de dados previstas

- Censo Escolar / INEP: base principal do projeto.
- Plataforma Nilo Pecanha / MEC: aprofundamento sobre a Rede Federal.
- IBGE / SIDRA: populacao para indicadores proporcionais.

Detalhes das fontes estao em [`docs/fontes_dados.md`](docs/fontes_dados.md).

## Estrutura do projeto

```text
Analytics/
  data/
    raw/          # dados brutos baixados das fontes oficiais
    processed/    # dados tratados prontos para Power BI
  docs/           # documentacao, fontes e dicionario de dados
  notebooks/      # notebooks de exploracao e ETL
  scripts/        # scripts reutilizaveis de ETL
  dashboard/      # arquivos do Power BI
  slides/         # apresentacao final
  images/         # prints do dashboard
```

## Ambiente Python

Crie e ative o ambiente virtual local:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Validacao rapida:

```powershell
python -c "import pandas, numpy, requests, openpyxl; print('imports ok')"
```

## Status

Etapa atual: preparacao do ambiente e planejamento do ETL.
