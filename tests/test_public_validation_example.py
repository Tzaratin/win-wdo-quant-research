"""Testes do exemplo público de validação quantitativa."""

import sys
from pathlib import Path

# Permite importar o arquivo que está na pasta examples.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = PROJECT_ROOT / "examples"

if str(EXAMPLES_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLES_DIR))

from public_validation_example import (  # noqa: E402
    Bar,
    mirror_control,
    run_backtest,
)


def test_signal_is_executed_only_on_next_bar() -> None:
    """
    O sinal da segunda barra não pode capturar o movimento
    que já aconteceu dentro dela.
    """

    bars = [
        Bar(open=100.0, close=100.0),
        Bar(open=100.0, close=110.0),
        Bar(open=110.0, close=110.0),
    ]

    signals = [0, 1, 0]

    result = run_backtest(
        bars,
        signals,
        name="anti_lookahead_test",
        cost_per_trade=0.0,
    )

    assert result.trades == 1
    assert result.net_pnl == 0.0


def test_cost_is_deducted_from_each_trade() -> None:
    bars = [
        Bar(open=100.0, close=100.0),
        Bar(open=100.0, close=105.0),
    ]

    signals = [1, 0]

    result = run_backtest(
        bars,
        signals,
        name="cost_test",
        cost_per_trade=1.0,
    )

    assert result.trades == 1
    assert result.gross_pnl == 5.0
    assert result.net_pnl == 4.0


def test_mirror_control_reverses_the_direction() -> None:
    signals = [1, 0, -1, 1]

    assert mirror_control(signals) == [-1, 0, 1, -1]


def test_cost_stress_reduces_result() -> None:
    bars = [
        Bar(open=100.0, close=100.0),
        Bar(open=100.0, close=104.0),
        Bar(open=104.0, close=106.0),
    ]

    signals = [1, 1, 0]

    normal_cost = run_backtest(
        bars,
        signals,
        name="normal_cost",
        cost_per_trade=0.25,
    )

    double_cost = run_backtest(
        bars,
        signals,
        name="double_cost",
        cost_per_trade=0.50,
    )

    assert double_cost.net_pnl < normal_cost.net_pnl
