#!/usr/bin/env python3
import pandas as pd
import pytest
from supermercado import (
    bubble_sort,
    ordenar_por_sucursal,
    calcular_importe,
    resumen_por_producto,
    resumen_por_sucursal,
    resumen_general,
    procesar
)


@pytest.fixture
def df_ordenado():
    return pd.DataFrame({
        "PRSUC":  ["SUC01", "SUC01", "SUC02"],
        "PRCOD":  ["P100",  "P100",  "P200"],
        "PRFEC":  ["2025-01-01", "2025-01-05", "2025-01-01"],
        "PRPROV": ["PROV01", "PROV02", "PROV01"],
        "PRCANT": [10, 5, 20],
        "PRPRE":  [100.0, 200.0, 50.0],
    })


@pytest.fixture
def df_con_importe(df_ordenado):
    return calcular_importe(df_ordenado)


def test_bubble_sort():
    data = [["SUC02", 2], ["SUC01", 1], ["SUC03", 3]]
    resultado = bubble_sort(data, 0)
    assert resultado[0][0] == "SUC01"
    assert resultado[1][0] == "SUC02"
    assert resultado[2][0] == "SUC03"


def test_ordenar_por_sucursal():
    df = pd.DataFrame({
        "PRSUC":  ["SUC03", "SUC01", "SUC02"],
        "PRCOD":  ["P100",  "P200",  "P300"],
        "PRFEC":  ["2025-01-01"] * 3,
        "PRPROV": ["PROV01"] * 3,
        "PRCANT": [1, 2, 3],
        "PRPRE":  [10.0, 20.0, 30.0],
    })
    resultado = ordenar_por_sucursal(df)
    assert list(resultado["PRSUC"]) == ["SUC01", "SUC02", "SUC03"]


def test_calcular_importe(df_ordenado):
    resultado = calcular_importe(df_ordenado)
    assert "PRIMPORTE" in resultado.columns
    assert list(resultado["PRIMPORTE"]) == [1000.0, 1000.0, 1000.0]


def test_resumen_por_producto(df_con_importe):
    resultado = resumen_por_producto(df_con_importe)
    assert len(resultado) == 2
    fila_suc01 = resultado[resultado["PRSUC"] == "SUC01"].iloc[0]
    assert fila_suc01["TOTUNI"] == 15
    assert fila_suc01["TOTPES"] == 2000.0


def test_resumen_por_sucursal(df_con_importe):
    resultado = resumen_por_sucursal(df_con_importe)
    assert len(resultado) == 2
    fila = resultado[resultado["PRSUC"] == "SUC01"].iloc[0]
    assert fila["TOTSUC"] == 15


def test_resumen_general(df_con_importe):
    resultado = resumen_general(df_con_importe)
    assert resultado["CANSUC"] == 2
    assert resultado["TOTALIMP"] == 3000.0

