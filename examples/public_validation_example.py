"""
Exemplo público e sintético dos controles de validação utilizados
no projeto de pesquisa quantitativa WIN/WDO.

Não contém dados reais, credenciais, parâmetros operacionais
ou estratégias utilizadas em produção.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Bar:
    open: float
    close: float


@dataclass(frozen=True)
class BacktestResult:
    name: str
    trades: int
    gross_pnl: float
    net_pnl: float
    profit_factor: float


def calculate_profit_factor(results: Iterable[float]) -> float:
    values = list(results)

    gains = sum(value for value in values if value > 0)
    losses = -sum(value for value in values if value < 0)

    if losses == 0:
        return float("inf") if gains > 0 else 0.0

    return gains / losses


def run_backtest(
    bars: list[Bar],
    signals: list[int],
    name: str,
    cost_per_trade: float = 1.0,
) -> BacktestResult:
    """
    O sinal produzido na barra atual somente é executado
    na abertura da barra seguinte.

    Essa regra evita o uso indevido de informações do futuro
    ou preenchimentos idealizados dentro da mesma barra.
    """

    if len(bars) != len(signals):
        raise ValueError("Bars e signals precisam ter o mesmo tamanho.")

    if cost_per_trade < 0:
        raise ValueError("O custo por operação não pode ser negativo.")

    trade_results: list[float] = []

    for index in range(1, len(bars)):
        previous_signal = signals[index - 1]

        if previous_signal == 0:
            continue

        current_bar = bars[index]

        gross_result = previous_signal * (
            current_bar.close - current_bar.open
        )

        net_result = gross_result - cost_per_trade
        trade_results.append(net_result)

    return BacktestResult(
        name=name,
        trades=len(trade_results),
        gross_pnl=sum(trade_results) + len(trade_results) * cost_per_trade,
        net_pnl=sum(trade_results),
        profit_factor=calculate_profit_factor(trade_results),
    )


def mirror_control(signals: list[int]) -> list[int]:
    """Controle que opera o lado oposto ao da hipótese."""

    return [-signal for signal in signals]


def passive_control(number_of_bars: int) -> list[int]:
    """Controle comprado sem o filtro proposto pela estratégia."""

    return [1] * number_of_bars


def main() -> None:
    synthetic_bars = [
        Bar(open=100.0, close=101.0),
        Bar(open=101.0, close=103.0),
        Bar(open=103.0, close=102.0),
        Bar(open=102.0, close=104.0),
        Bar(open=104.0, close=103.0),
        Bar(open=103.0, close=105.0),
    ]

    candidate_signals = [0, 1, -1, 1, -1, 0]

    candidate = run_backtest(
        synthetic_bars,
        candidate_signals,
        name="candidate",
        cost_per_trade=0.25,
    )

    cost_stress = run_backtest(
        synthetic_bars,
        candidate_signals,
        name="candidate_cost_2x",
        cost_per_trade=0.50,
    )

    mirror = run_backtest(
        synthetic_bars,
        mirror_control(candidate_signals),
        name="mirror_control",
        cost_per_trade=0.25,
    )

    passive = run_backtest(
        synthetic_bars,
        passive_control(len(synthetic_bars)),
        name="passive_control",
        cost_per_trade=0.25,
    )

    print(candidate)
    print(cost_stress)
    print(mirror)
    print(passive)

    approved_for_next_stage = (
        candidate.net_pnl > 0
        and cost_stress.net_pnl > 0
        and candidate.net_pnl > mirror.net_pnl
        and candidate.net_pnl > passive.net_pnl
    )

    print("Approved for next stage:", approved_for_next_stage)


if __name__ == "__main__":
    main()
