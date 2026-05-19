from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw" / "microdados_censo_escolar_2025" / "dados"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

CURSO_TECNICO_FILE = RAW_DIR / "Tabela_Curso_Tecnico_2025.csv"
ESCOLA_FILE = RAW_DIR / "Tabela_Escola_2025.csv"
OUTPUT_FILE = PROCESSED_DIR / "fato_matriculas_tecnicas_2025.csv"

DEPENDENCIA_MAP = {
    1: "Federal",
    2: "Estadual",
    3: "Municipal",
    4: "Privada",
}

LOCALIZACAO_MAP = {
    1: "Urbana",
    2: "Rural",
}


CURSO_TECNICO_COLUMNS = [
    "NU_ANO_CENSO",
    "CO_ENTIDADE",
    "NO_AREA_CURSO_PROFISSIONAL",
    "ID_AREA_CURSO_PROFISSIONAL",
    "NO_CURSO_EDUC_PROFISSIONAL",
    "CO_CURSO_EDUC_PROFISSIONAL",
    "QT_CURSO_TEC",
    "QT_MAT_CURSO_TEC",
    "QT_MAT_CURSO_TEC_IFTP",
    "QT_MAT_CURSO_TEC_NM",
    "QT_MAT_CURSO_TEC_CONC",
    "QT_MAT_CURSO_TEC_SUBS",
    "QT_MAT_CURSO_TEC_IFTP_CT",
    "QT_MAT_CURSO_TEC_EJA",
]


ESCOLA_COLUMNS = [
    "NU_ANO_CENSO",
    "NO_REGIAO",
    "SG_UF",
    "CO_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "CO_ENTIDADE",
    "NO_ENTIDADE",
    "TP_DEPENDENCIA",
    "TP_LOCALIZACAO",
]


def read_input_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    curso_tecnico = pd.read_csv(
        CURSO_TECNICO_FILE,
        sep=";",
        encoding="latin1",
        usecols=CURSO_TECNICO_COLUMNS,
    )

    escola = pd.read_csv(
        ESCOLA_FILE,
        sep=";",
        encoding="latin1",
        usecols=ESCOLA_COLUMNS,
    )

    return curso_tecnico, escola


def merge_course_and_school_data(
    curso_tecnico: pd.DataFrame,
    escola: pd.DataFrame,
) -> pd.DataFrame:
    merged = curso_tecnico.merge(
        escola,
        on=["NU_ANO_CENSO", "CO_ENTIDADE"],
        how="left",
        indicator=True,
    )

    unmatched_rows = merged["_merge"].ne("both").sum()
    if unmatched_rows:
        raise ValueError(
            f"Join incompleto: {unmatched_rows} linhas de curso tecnico nao encontraram escola."
        )

    return merged.drop(columns=["_merge"])


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    transformed = data.copy()

    transformed["rede"] = transformed["TP_DEPENDENCIA"].map(DEPENDENCIA_MAP)
    transformed["localizacao"] = transformed["TP_LOCALIZACAO"].map(LOCALIZACAO_MAP)

    transformed = transformed.rename(
        columns={
            "NU_ANO_CENSO": "ano",
            "NO_REGIAO": "regiao",
            "SG_UF": "uf",
            "CO_UF": "codigo_uf",
            "NO_MUNICIPIO": "municipio",
            "CO_MUNICIPIO": "codigo_municipio",
            "CO_ENTIDADE": "codigo_entidade",
            "NO_ENTIDADE": "nome_entidade",
            "NO_AREA_CURSO_PROFISSIONAL": "area_curso_profissional",
            "ID_AREA_CURSO_PROFISSIONAL": "codigo_area_curso_profissional",
            "NO_CURSO_EDUC_PROFISSIONAL": "curso_educacao_profissional",
            "CO_CURSO_EDUC_PROFISSIONAL": "codigo_curso_educacao_profissional",
            "QT_CURSO_TEC": "qtd_cursos_tecnicos",
            "QT_MAT_CURSO_TEC": "matriculas_cursos_tecnicos",
            "QT_MAT_CURSO_TEC_IFTP": "matriculas_itinerario_formacao_tecnica_profissional",
            "QT_MAT_CURSO_TEC_NM": "matriculas_curso_tecnico_nivel_medio",
            "QT_MAT_CURSO_TEC_CONC": "matriculas_curso_tecnico_concomitante",
            "QT_MAT_CURSO_TEC_SUBS": "matriculas_curso_tecnico_subsequente",
            "QT_MAT_CURSO_TEC_IFTP_CT": "matriculas_curso_tecnico_itinerario_ct",
            "QT_MAT_CURSO_TEC_EJA": "matriculas_curso_tecnico_eja",
        }
    )

    final_columns = [
        "ano",
        "regiao",
        "uf",
        "codigo_uf",
        "municipio",
        "codigo_municipio",
        "codigo_entidade",
        "nome_entidade",
        "rede",
        "localizacao",
        "area_curso_profissional",
        "codigo_area_curso_profissional",
        "curso_educacao_profissional",
        "codigo_curso_educacao_profissional",
        "qtd_cursos_tecnicos",
        "matriculas_cursos_tecnicos",
        "matriculas_itinerario_formacao_tecnica_profissional",
        "matriculas_curso_tecnico_nivel_medio",
        "matriculas_curso_tecnico_concomitante",
        "matriculas_curso_tecnico_subsequente",
        "matriculas_curso_tecnico_itinerario_ct",
        "matriculas_curso_tecnico_eja",
    ]

    return transformed[final_columns]


def save_output(data: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")


def validate_output(expected_data: pd.DataFrame) -> None:
    saved_data = pd.read_csv(OUTPUT_FILE, encoding="utf-8-sig")

    if saved_data.shape != expected_data.shape:
        raise ValueError(
            f"Arquivo salvo com shape inesperado. Esperado {expected_data.shape}, obtido {saved_data.shape}."
        )

    expected_total = expected_data["matriculas_cursos_tecnicos"].sum()
    saved_total = saved_data["matriculas_cursos_tecnicos"].sum()

    if saved_total != expected_total:
        raise ValueError(
            f"Total de matriculas divergente. Esperado {expected_total}, obtido {saved_total}."
        )


def main() -> None:
    print("ETL Censo Escolar 2025 - Educacao Profissional e Tecnica")
    print(f"Arquivo de cursos tecnicos: {CURSO_TECNICO_FILE}")
    print(f"Arquivo de escolas: {ESCOLA_FILE}")
    print(f"Saida tratada: {OUTPUT_FILE}")

    curso_tecnico, escola = read_input_data()

    print("\nBases carregadas:")
    print(f"- Curso tecnico: {curso_tecnico.shape[0]:,} linhas x {curso_tecnico.shape[1]} colunas")
    print(f"- Escola: {escola.shape[0]:,} linhas x {escola.shape[1]} colunas")

    merged = merge_course_and_school_data(curso_tecnico, escola)

    print("\nJoin validado:")
    print(f"- Base integrada: {merged.shape[0]:,} linhas x {merged.shape[1]} colunas")
    print("- Todas as linhas de curso tecnico encontraram escola correspondente.")

    transformed = transform_data(merged)

    print("\nBase padronizada:")
    print(f"- Base final: {transformed.shape[0]:,} linhas x {transformed.shape[1]} colunas")
    print(f"- Total de matriculas tecnicas: {transformed['matriculas_cursos_tecnicos'].sum():,}")

    save_output(transformed)
    validate_output(transformed)

    print("\nArquivo exportado e validado com sucesso.")
    print(f"- {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
