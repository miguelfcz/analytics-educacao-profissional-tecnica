from pathlib import Path

import pandas as pd
import requests


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "dim_populacao_municipio_2022.csv"

SIDRA_URL = (
    "https://apisidra.ibge.gov.br/values/"
    "t/4714/n6/all/v/93/p/2022?formato=json"
)


def fetch_sidra_data() -> list[dict]:
    response = requests.get(SIDRA_URL, timeout=120)
    response.raise_for_status()
    return response.json()


def transform_data(raw_data: list[dict]) -> pd.DataFrame:
    # A primeira linha da API SIDRA traz metadados/cabecalhos, nao dados.
    records = raw_data[1:]
    data = pd.DataFrame(records)

    transformed = pd.DataFrame(
        {
            "ano_populacao": data["D3C"].astype(int),
            "codigo_municipio": data["D1C"].astype(int),
            "municipio_uf": data["D1N"],
            "populacao_residente": pd.to_numeric(data["V"], errors="coerce").astype("Int64"),
            "fonte_populacao": "IBGE/SIDRA - Censo Demografico 2022, tabela 4714, variavel 93",
        }
    )

    transformed[["municipio", "uf"]] = transformed["municipio_uf"].str.extract(
        r"^(.*) - ([A-Z]{2})$"
    )

    final_columns = [
        "ano_populacao",
        "codigo_municipio",
        "municipio",
        "uf",
        "populacao_residente",
        "fonte_populacao",
    ]

    return transformed[final_columns]


def validate_data(data: pd.DataFrame) -> None:
    if data.empty:
        raise ValueError("Dataset de populacao vazio.")

    if data["codigo_municipio"].duplicated().any():
        raise ValueError("Existem codigos de municipio duplicados.")

    if data["populacao_residente"].isna().any():
        raise ValueError("Existem valores nulos em populacao_residente.")

    if data["municipio"].isna().any() or data["uf"].isna().any():
        raise ValueError("Falha ao separar municipio e UF.")

    if len(data) < 5_000:
        raise ValueError(f"Quantidade de municipios inesperada: {len(data)}.")


def save_output(data: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")


def main() -> None:
    print("ETL IBGE/SIDRA - Populacao municipal 2022")
    print(f"Fonte: {SIDRA_URL}")
    print(f"Saida tratada: {OUTPUT_FILE}")

    raw_data = fetch_sidra_data()
    transformed = transform_data(raw_data)
    validate_data(transformed)
    save_output(transformed)

    print("\nArquivo exportado com sucesso.")
    print(f"- Municipios: {len(transformed):,}")
    print(f"- Populacao total: {transformed['populacao_residente'].sum():,}")
    print(f"- {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
