from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

MATRICULAS_FILE = PROCESSED_DIR / "fato_matriculas_tecnicas_2025.csv"
POPULACAO_FILE = PROCESSED_DIR / "dim_populacao_municipio_2022.csv"
OUTPUT_FILE = PROCESSED_DIR / "indicadores_municipais_educacao_tecnica_2025.csv"


def read_input_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    matriculas = pd.read_csv(MATRICULAS_FILE, encoding="utf-8-sig")
    populacao = pd.read_csv(POPULACAO_FILE, encoding="utf-8-sig")
    return matriculas, populacao


def build_municipal_indicators(
    matriculas: pd.DataFrame,
    populacao: pd.DataFrame,
) -> pd.DataFrame:
    aggregated = (
        matriculas.groupby(
            ["regiao", "uf", "codigo_uf", "municipio", "codigo_municipio"],
            as_index=False,
        )
        .agg(
            matriculas_cursos_tecnicos=("matriculas_cursos_tecnicos", "sum"),
            qtd_cursos_tecnicos=("qtd_cursos_tecnicos", "sum"),
            qtd_escolas_com_curso_tecnico=("codigo_entidade", "nunique"),
            qtd_cursos_distintos=("codigo_curso_educacao_profissional", "nunique"),
        )
    )

    indicators = aggregated.merge(
        populacao[["codigo_municipio", "ano_populacao", "populacao_residente"]],
        on="codigo_municipio",
        how="left",
    )

    indicators["matriculas_tecnicas_por_100_mil_hab"] = (
        indicators["matriculas_cursos_tecnicos"]
        / indicators["populacao_residente"]
        * 100_000
    ).round(2)

    final_columns = [
        "regiao",
        "uf",
        "codigo_uf",
        "municipio",
        "codigo_municipio",
        "matriculas_cursos_tecnicos",
        "qtd_cursos_tecnicos",
        "qtd_escolas_com_curso_tecnico",
        "qtd_cursos_distintos",
        "ano_populacao",
        "populacao_residente",
        "matriculas_tecnicas_por_100_mil_hab",
    ]

    return indicators[final_columns]


def validate_data(data: pd.DataFrame) -> None:
    if data.empty:
        raise ValueError("Dataset de indicadores municipais vazio.")

    if data["codigo_municipio"].duplicated().any():
        raise ValueError("Existem municipios duplicados no dataset final.")

    if data["populacao_residente"].isna().any():
        raise ValueError("Existem municipios sem populacao residente.")

    if data["matriculas_tecnicas_por_100_mil_hab"].isna().any():
        raise ValueError("Existem indicadores proporcionais nulos.")

    if len(data) != 3_385:
        raise ValueError(f"Quantidade inesperada de municipios: {len(data)}.")

    total_matriculas = int(data["matriculas_cursos_tecnicos"].sum())
    if total_matriculas != 2_490_145:
        raise ValueError(f"Total de matriculas inesperado: {total_matriculas}.")


def save_output(data: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")


def main() -> None:
    print("ETL - Indicadores municipais de educacao tecnica 2025")
    print(f"Base de matriculas: {MATRICULAS_FILE}")
    print(f"Base de populacao: {POPULACAO_FILE}")
    print(f"Saida tratada: {OUTPUT_FILE}")

    matriculas, populacao = read_input_data()
    indicators = build_municipal_indicators(matriculas, populacao)
    validate_data(indicators)
    save_output(indicators)

    print("\nArquivo exportado com sucesso.")
    print(f"- Municipios com matriculas tecnicas: {len(indicators):,}")
    print(f"- Total de matriculas tecnicas: {indicators['matriculas_cursos_tecnicos'].sum():,}")
    print(f"- {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
