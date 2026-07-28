# WIN/WDO Quant Research Lab

> Framework de pesquisa quantitativa orientado à auditoria para testar estratégias sistemáticas nos minicontratos futuros da B3.

**Status do projeto:** pesquisa ativa · publicação aberta em preparação · uso apenas em pesquisa/shadow

## Visão geral

O WIN/WDO Quant Research Lab é um projeto de pesquisa quantitativa voltado ao minicontrato futuro de índice (**WIN**) e ao minicontrato futuro de dólar (**WDO**) negociados na B3, utilizando principalmente dados de cinco minutos.

O projeto reúne:

- pesquisa de estratégias orientada por hipóteses;
- backtests históricos;
- premissas realistas de execução e custos;
- controles contra lookahead e sobreajuste;
- análise de correlação e risco incremental na carteira;
- acompanhamento em modo shadow por MetaTrader 5;
- implementações e especificações de referência em NTSL/Profit;
- documentação explícita de hipóteses aprovadas e reprovadas.

O objetivo não é gerar muitas ideias de operação nem apresentar backtests atraentes. O objetivo é construir um processo reproduzível que dificulte a aprovação de falsos positivos.

## Princípio central

> Toda hipótese nasce falsa.  
> O processo de pesquisa deve tentar destruí-la antes de tratá-la como candidata.

Um backtest lucrativo de forma isolada não é suficiente. A candidata precisa continuar defensável após custos realistas, testes de estresse, perturbações de parâmetros, confirmação fora da amostra, revisão da execução e comparação com a carteira existente.

## Escopo

- **Mercados:** futuros WIN e WDO negociados na B3
- **Timeframe principal:** M5
- **Dados auxiliares:** D1 e séries de outros ativos quando houver justificativa econômica
- **Linguagem de pesquisa:** Python
- **Integração operacional/shadow:** MetaTrader 5
- **Referência para transferência de plataforma:** NTSL para Profit/Nelogica
- **Ambiente:** principalmente Windows, devido às dependências do MetaTrader 5 e do Profit

Este repositório é um ambiente de pesquisa e validação. Ele **não** é uma corretora, serviço de sinais, sistema de recomendação de investimentos ou garantia de desempenho futuro.

## Protocolo de pesquisa

O protocolo atual separa pesquisa, confirmação e holdout intocado.

### 1. Separação temporal

- O desenvolvimento de hipóteses fica limitado aos dados encerrados em **31/12/2025**.
- Dentro do período de desenvolvimento, **2021–2023** é usado como amostra de desenvolvimento e **2024–2025** como confirmação fora da amostra.
- Um holdout fisicamente separado, de **02/01/2026 a 02/07/2026**, permanece fora da criação de variáveis, escolha de thresholds e aprovação das estratégias.

O holdout não deve funcionar como uma segunda base de otimização. Ele é reservado para uma avaliação posterior, única e regida por protocolo previamente definido.

### 2. Integridade da execução

A pesquisa deve evitar preenchimentos idealizados. Conforme a estratégia, a implementação exige confirmação negociável e utiliza o próximo preço executável disponível, em vez de um nível teórico conhecido apenas após o fechamento da barra.

As verificações incluem:

- ausência de informação de barras futuras;
- ausência de inconsistência entre decisão e execução na mesma barra;
- tratamento explícito de sessão e fuso horário;
- inicialização a frio sem estado histórico oculto;
- reconciliação entre sinais e trades;
- reprodução na plataforma de destino quando houver intenção de uso em NTSL/Profit.

### 3. Custos e robustez

As candidatas são avaliadas com:

- custos de transação de referência;
- **estresse de custos de 2×**;
- perturbações de parâmetros, geralmente em torno de **±20%**;
- resultados anuais e mensais;
- desempenho excluindo o melhor ano;
- testes de recência e regimes;
- revisão do pior trade, drawdown e excursão adversa quando pertinente.

### 4. Controles e placebos

Estratégias direcionais devem incluir, quando aplicável:

- controle passivo, operando o mesmo lado e janela sem o filtro proposto;
- controle espelho, operando o lado oposto com gatilho invertido;
- placebo específico para o mecanismo;
- testes demonstrando que o resultado não é apenas deriva de mercado, artefato de horário ou cópia disfarçada de estratégia existente.

### 5. Validação em carteira

A estratégia é analisada como parte da carteira, e não apenas isoladamente.

As verificações relevantes incluem:

- correlação com os agentes existentes;
- sobreposição de trades e mecanismos;
- contribuição incremental para o Sharpe;
- impacto no drawdown agregado;
- concentração de risco por ativo, direção e janela;
- existência de uma fonte realmente nova de retorno ajustado ao risco.

Uma candidata lucrativa pode ser rejeitada caso duplique uma estratégia existente ou piore a carteira combinada.

## Os status de validação são explícitos

| Status | Significado |
|---|---|
| **Pesquisa** | A hipótese ainda está sendo estudada e pode conter fragilidades não resolvidas. |
| **Shadow** | Os sinais são registrados sem execução automática com dinheiro real. |
| **Simulação** | A candidata passou por verificações adicionais, mas permanece sob observação controlada. |
| **Validada na plataforma** | O comportamento em Python/MT5 foi reconciliado com a plataforma de destino. |
| **Reprovada** | A candidata falhou em algum gate obrigatório ou foi substituída; o resultado negativo é preservado. |

Uma estratégia validada no Python não é automaticamente considerada válida no Profit/NTSL. Diferenças de barras, horários, construção de símbolos e preenchimentos podem invalidar um edge aparente.

## Componentes principais

O projeto de trabalho está organizado em torno dos seguintes componentes:

```text
.
├── motor_multi.py                 # Motor multiagente em modo shadow
├── painel_shadow.py               # Painel de acompanhamento shadow
├── backtest_carteira.py           # Análise da carteira
├── backtest_candidatos_v10.py     # Biblioteca de pesquisa
├── backtest_candidatos_v13.py     # Biblioteca posterior de pesquisa
├── backtest_filtros_v12.py        # Filtros de pesquisa
├── analise_alvos_sweep.py         # Análise de alvos e saídas
├── analise_eventos.py             # Análise de eventos
├── pesquisa/                      # Scripts de pesquisa e validação
├── robos_ntsl/                    # Implementações de referência em NTSL
├── docs/                          # Arquitetura, auditorias e processo
├── requirements.txt               # Dependências Python
├── package.json                   # Serviço opcional de alertas em Node.js
├── .env.example                   # Modelo público de configuração
└── .gitignore                     # Exclusões de arquivos privados/gerados
```

O repositório público poderá conter uma versão menor e higienizada do arquivo interno de pesquisa. Arquivos antigos só devem permanecer quando tiverem valor de auditoria e estiverem claramente identificados.

## Dados

Os dados históricos brutos não são redistribuídos neste repositório, pois podem ter licença, grande volume ou informações operacionalmente sensíveis.

Os scripts de pesquisa atualmente esperam arquivos locais como:

```text
win_M5_full.csv
wdo_M5_full.csv
win_D1_full.csv
wdo_D1_full.csv
```

Séries externas ou de outros ativos podem ser utilizadas quando a hipótese possuir um mecanismo econômico declarado.

A documentação pública do esquema dos dados e uma base sintética de exemplo fazem parte do roadmap. Até lá, cada pessoa deverá fornecer dados obtidos legalmente e verificar se horários, sessões, rolagens e convenções de símbolos correspondem às premissas do estudo.

## Instalação

### Pré-requisitos

- Windows 10 ou superior para o fluxo completo com MT5/Profit
- Python 3.10+
- Node.js 18+ somente para o serviço local opcional de alertas
- MetaTrader 5 somente para acompanhamento de dados em modo shadow
- Profit/Nelogica somente para conferir a transferência para NTSL

### Ambiente Python

```bash
python -m venv .venv
```

No Windows:

```bat
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Serviço opcional em Node.js

```bash
npm install
```

### Configuração

Copie o modelo público de ambiente:

```bat
copy .env.example .env
```

Mantenha configurações seguras durante os testes:

```dotenv
MODO_SHADOW=true
ENVIAR_WHATSAPP=false
```

Nunca versione `.env`, sessões de autenticação, bancos de dados, identificadores de conta, logs com informações privadas ou chaves de API.

## Executando pesquisas

Execute os scripts de pesquisa a partir da raiz do repositório, pois vários deles utilizam caminhos relativos:

```bash
python pesquisa/<nome_do_script>.py
```

Exemplo de análise da carteira:

```bash
python backtest_carteira.py
```

Motor shadow, após configurar o MetaTrader 5:

```bash
python motor_multi.py
```

O motor shadow foi criado para registrar e comparar sinais. Ele não deve ser interpretado como autorização para operar com dinheiro real.

## Padrão de reprodutibilidade

Um resultado de pesquisa deve incluir, quando aplicável:

- especificação escrita antes da confirmação final;
- intervalo dos dados e definição dos símbolos;
- regras de entrada, saída, stop e preenchimento;
- taxas, slippage e premissas de estresse;
- quantidade de operações;
- resultados anuais e mensais;
- separação entre amostra de desenvolvimento e confirmação;
- robustez dos parâmetros;
- controles passivo, espelho e placebo;
- drawdown máximo e pior trade;
- correlação e impacto incremental na carteira;
- veredito claro: próxima etapa, somente shadow ou reprovação.

Resultados que não puderem ser reproduzidos são tratados como não verificados, ainda que pareçam plausíveis.

## Limitações conhecidas

- A base de código cresceu a partir de um ambiente operacional e ainda possui scripts legados.
- Alguns scripts dependem de CSVs localizados na raiz.
- O acompanhamento shadow completo depende de Windows e MetaTrader 5.
- Diferenças de dados podem impedir a transferência dos resultados de Python/MT5 para Profit/Nelogica.
- Os resultados históricos são sensíveis à qualidade dos dados, rolagens, custos e premissas de execução.
- Mesmo um backtest cuidadosamente validado não garante rentabilidade futura.
- Nem toda estratégia, base de dados ou integração operacional interna é adequada para publicação.

## Roadmap de publicação — próximos seis meses

O projeto pretende:

1. separar o núcleo reutilizável de pesquisa das integrações operacionais privadas;
2. congelar e documentar as dependências;
3. criar testes automatizados para lookahead, horários, preenchimentos, custos e inicialização de estado;
4. publicar o esquema dos CSVs e uma base sintética de exemplo;
5. criar exemplos reproduzíveis em linha de comando;
6. implantar integração contínua para testes e qualidade do código;
7. publicar registros de decisão, incluindo hipóteses reprovadas e os motivos;
8. melhorar a documentação em português e inglês;
9. adicionar orientações de contribuição e modelos de issues;
10. facilitar a auditoria dos relatórios sem expor dados licenciados ou credenciais.

## Uso de inteligência artificial no desenvolvimento

Ferramentas de IA podem ser utilizadas para:

- compreender e navegar em uma base grande de código;
- propor refatorações;
- gerar casos de teste;
- revisar documentação;
- identificar casos extremos;
- comparar implementações;
- organizar relatórios de experimentos.

Código ou análise produzidos por IA não são aceitos como evidência por si só. As alterações são revisadas, executadas e validadas localmente. Nenhuma métrica de desempenho é considerada real antes de ser reproduzida pelo código do projeto e submetida aos mesmos gates aplicados aos demais resultados.

## Como contribuir

São bem-vindas contribuições que melhorem:

- reprodutibilidade;
- testes;
- validação de dados;
- realismo de execução;
- documentação;
- registro dos experimentos;
- controles estatísticos;
- conferência da transferência entre plataformas.

Evite pull requests baseados apenas em uma curva de capital atraente ou em uma busca de parâmetros sem documentação. A contribuição deve explicar o mecanismo proposto, as premissas dos dados, a metodologia de validação e as falhas conhecidas.

## Segurança e privacidade

Nunca devem ser versionados:

- arquivos `.env` e chaves de API;
- sessões de autenticação do WhatsApp ou navegador;
- credenciais de conta ou corretora;
- bancos de dados e estados operacionais;
- logs e capturas privadas;
- backups;
- dados de mercado licenciados que não possam ser redistribuídos.

Caso uma credencial tenha sido incluída em algum arquivo ou commit, remover o arquivo não é suficiente: a credencial também deve ser revogada e substituída.

## Licença

Uma licença open source aprovada pela OSI deverá ser escolhida antes da primeira versão pública marcada.

Até que um arquivo de licença seja adicionado, o código poderá estar visível para análise, mas ninguém deverá presumir autorização para copiar, modificar ou redistribuir.

## Aviso

Este projeto é disponibilizado exclusivamente para pesquisa e educação. Ele não constitui recomendação financeira, indicação de investimento ou promessa de retorno. A negociação de contratos futuros envolve risco elevado, e resultados históricos não preveem resultados futuros.
