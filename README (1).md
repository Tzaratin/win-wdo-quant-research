# WIN/WDO Quant Research Lab

> An audit-first research framework for testing systematic strategies in Brazilian B3 mini futures.

**Project status:** active research · public release in progress · research/shadow use only

## Overview

WIN/WDO Quant Research Lab is a quantitative research project focused on the Brazilian mini-index futures contract (**WIN**) and mini-US-dollar futures contract (**WDO**), primarily using five-minute market data.

The project combines:

- hypothesis-driven strategy research;
- historical backtesting;
- realistic execution and transaction-cost assumptions;
- anti-lookahead and anti-overfitting controls;
- portfolio-level correlation and incremental-risk analysis;
- shadow monitoring with MetaTrader 5;
- reference implementations and specifications for NTSL/Profit;
- explicit documentation of both accepted and rejected hypotheses.

The goal is not to generate frequent trading ideas or present attractive backtests. The goal is to build a reproducible process that makes false positives difficult to approve.

## Core principle

> Every hypothesis starts false.  
> The research process must try to break it before treating it as a candidate.

A profitable standalone backtest is not enough. A candidate must remain credible after realistic costs, stress tests, parameter perturbations, out-of-sample confirmation, execution review, and comparison with the existing portfolio.

## Scope

- **Markets:** WIN and WDO futures traded on B3
- **Primary timeframe:** M5
- **Supporting data:** D1 and selected cross-asset series when economically justified
- **Research language:** Python
- **Operational/shadow integration:** MetaTrader 5
- **Platform-transfer reference:** NTSL for Profit/Nelogica
- **Environment:** primarily Windows because of MetaTrader 5 and Profit dependencies

This repository is a research and validation environment. It is **not** a brokerage service, signal-selling product, investment recommendation system, or guarantee of future performance.

## Research protocol

The current protocol separates research, confirmation, and untouched holdout data.

### 1. Time separation

- Hypothesis development is limited to data ending on **2025-12-31**.
- Inside the development period, **2021–2023** is used for in-sample research and **2024–2025** for out-of-sample confirmation.
- A physically separated holdout covering **2026-01-02 through 2026-07-02** is kept outside feature design, threshold selection, and strategy approval.

The holdout is not a second optimization set. It is intended for a later, one-time assessment under a predefined protocol.

### 2. Execution integrity

Research must avoid idealized fills. Depending on the strategy, the implementation requires a tradable confirmation and uses the next available executable price rather than a theoretical level known only after the bar closes.

Checks include:

- no future-bar information;
- no same-bar decision/fill inconsistency;
- explicit session and timezone handling;
- cold-start behavior without hidden historical state;
- signal-to-trade reconciliation;
- target-platform reproduction when the strategy is intended for NTSL/Profit.

### 3. Cost and robustness testing

Candidates are evaluated with:

- baseline transaction costs;
- a **2× cost stress**;
- parameter perturbations, generally around **±20%**;
- yearly and monthly breakdowns;
- performance excluding the best year;
- recency and regime checks;
- worst trade, drawdown, and adverse-excursion review when relevant.

### 4. Controls and placebos

Directional strategies should include, when applicable:

- a passive control operating the same side and time window without the proposed filter;
- a mirror control using the opposite side with an inverted trigger;
- a mechanism-specific placebo;
- tests showing that the result is not only market drift, a timestamp artifact, or a disguised copy of an existing strategy.

### 5. Portfolio validation

A strategy is evaluated as part of a portfolio, not only in isolation.

Relevant checks include:

- correlation with existing agents;
- overlapping trades and mechanisms;
- incremental Sharpe contribution;
- impact on aggregate drawdown;
- risk concentration by asset, direction, and time window;
- whether the candidate adds a genuinely new source of risk-adjusted return.

A profitable candidate may still be rejected when it duplicates an existing strategy or worsens the combined portfolio.

## Validation status is explicit

The project separates the following states:

| Status | Meaning |
|---|---|
| **Research** | Hypothesis is being studied and may still contain unresolved weaknesses. |
| **Shadow** | Signals are recorded without automatic real-money execution. |
| **Simulation** | Candidate has passed additional checks but remains under controlled observation. |
| **Platform-validated** | Python/MT5 behavior has been reconciled with the intended target platform. |
| **Rejected** | Candidate failed a required gate or was superseded; the negative result is preserved. |

A strategy validated in Python is not automatically considered valid in Profit/NTSL. Differences in bars, timestamps, symbol construction, and fill behavior can invalidate an apparent edge.

## Main components

The working project is organized around the following components:

```text
.
├── motor_multi.py                 # Multi-agent shadow runtime
├── painel_shadow.py               # Shadow monitoring panel
├── backtest_carteira.py           # Portfolio-level analysis
├── backtest_candidatos_v10.py     # Backtest research library
├── backtest_candidatos_v13.py     # Later backtest research library
├── backtest_filtros_v12.py        # Research filters
├── analise_alvos_sweep.py         # Target/exit analysis
├── analise_eventos.py             # Event analysis
├── pesquisa/                      # Research and validation scripts
├── robos_ntsl/                    # NTSL reference implementations
├── docs/                          # Architecture, audit, and process notes
├── requirements.txt               # Python dependencies
├── package.json                   # Optional Node.js alert service
├── .env.example                   # Public configuration template
└── .gitignore                     # Private/generated-file exclusions
```

The public repository may contain a smaller, cleaned subset of the internal research archive. Legacy files are retained only when they provide audit value and are clearly labeled.

## Data

Raw historical market data is not redistributed in this repository because it may be licensed, large, or operationally sensitive.

Research scripts currently expect local files such as:

```text
win_M5_full.csv
wdo_M5_full.csv
win_D1_full.csv
wdo_D1_full.csv
```

Selected external or cross-asset series may also be used when the hypothesis has a stated economic mechanism.

A public data-schema document and synthetic sample dataset are part of the release roadmap. Until then, users must supply legally obtained data and verify that timestamps, session boundaries, rollover treatment, and symbol conventions match the assumptions of each study.

## Installation

### Prerequisites

- Windows 10 or later for the full MT5/Profit workflow
- Python 3.10+
- Node.js 18+ only for the optional local alert service
- MetaTrader 5 only for live-data/shadow monitoring
- Profit/Nelogica only for NTSL transfer checks

### Python environment

```bash
python -m venv .venv
```

On Windows:

```bat
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Optional Node.js service

```bash
npm install
```

### Configuration

Copy the public environment template:

```bat
copy .env.example .env
```

Keep safe defaults while testing:

```dotenv
MODO_SHADOW=true
ENVIAR_WHATSAPP=false
```

Never commit `.env`, authentication sessions, databases, account identifiers, logs containing private information, or API keys.

## Running research

Run research scripts from the repository root because several scripts use relative paths:

```bash
python pesquisa/<script_name>.py
```

Example portfolio analysis:

```bash
python backtest_carteira.py
```

Shadow runtime, after configuring MetaTrader 5:

```bash
python motor_multi.py
```

The shadow runtime is intended to record and compare signals. It should not be interpreted as authorization for real-money trading.

## Reproducibility standard

A research result should include, whenever applicable:

- strategy specification written before final confirmation;
- data range and symbol definition;
- entry, exit, stop, and fill rules;
- fees, slippage, and stress assumptions;
- number of trades;
- yearly and monthly results;
- in-sample and out-of-sample separation;
- parameter-robustness results;
- passive, mirror, and placebo controls;
- maximum drawdown and worst-trade information;
- correlation and incremental portfolio impact;
- a clear final verdict: approved for the next stage, shadow only, or rejected.

Results that cannot be reproduced are treated as unverified, regardless of how plausible they appear.

## Known limitations

- The current codebase grew from an operational research environment and still contains legacy scripts.
- Some scripts depend on root-relative CSV paths.
- Full shadow monitoring depends on Windows and MetaTrader 5.
- Market-data differences can prevent Python/MT5 results from transferring to Profit/Nelogica.
- Historical results are sensitive to data quality, rollover conventions, costs, and fill assumptions.
- A backtest, even when carefully validated, does not guarantee future profitability.
- Not every internal strategy, dataset, or operational component is suitable for public release.

## Public-release roadmap

During the next six months, the project aims to:

1. separate the reusable research core from private operational integrations;
2. freeze and document dependencies;
3. add automated tests for lookahead, bar timing, fills, costs, and state initialization;
4. publish a documented CSV schema and synthetic sample dataset;
5. create reproducible command-line examples for representative studies;
6. add continuous integration for tests and code quality;
7. publish decision logs that include rejected hypotheses and reasons for rejection;
8. improve English and Portuguese documentation;
9. add contribution guidelines and issue templates;
10. make research reports easier to audit without exposing licensed data or private credentials.

## Use of AI-assisted development

AI tools may be used for:

- navigating and understanding a large codebase;
- proposing refactors;
- generating test cases;
- reviewing documentation;
- identifying edge cases;
- comparing implementations;
- organizing experiment reports.

AI-generated code or analysis is not accepted as evidence by itself. Suggested changes are reviewed, executed, and validated locally. No performance metric is considered real until it is reproduced by the project’s own code and passes the same validation gates as any other result.

## Contributing

Contributions are welcome when they improve:

- reproducibility;
- tests;
- data validation;
- execution realism;
- documentation;
- experiment tracking;
- statistical controls;
- platform-transfer checks.

Please avoid pull requests based only on an attractive equity curve or an undocumented parameter search. A contribution should explain the proposed mechanism, data assumptions, validation method, and known failure modes.

## Security and privacy

The following must never be committed:

- `.env` files and API keys;
- WhatsApp or browser authentication sessions;
- account or broker credentials;
- operational databases and state files;
- private logs and screenshots;
- backups;
- licensed market data that cannot be redistributed.

If a credential was ever included in a file or commit, removing the file is not enough: the credential must also be revoked and replaced.

## License

An OSI-approved open-source license must be selected before the first tagged public release.

Until a license file is added, the source may be visible for review, but no permission to copy, modify, or redistribute it should be assumed.

## Disclaimer

This project is provided for research and educational purposes only. It is not financial advice, an investment recommendation, or a promise of returns. Futures trading involves substantial risk, and historical performance does not predict future results.
