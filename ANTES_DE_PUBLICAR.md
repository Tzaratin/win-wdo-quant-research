# Antes de publicar o projeto no GitHub

## Não envie o ZIP inteiro

O arquivo interno do projeto contém componentes que não devem ser publicados diretamente. Crie uma pasta limpa e copie apenas o que for destinado ao repositório público.

## Remover ou manter fora do Git

- `.env`
- `.wwebjs_cache/`
- `.wwebjs_auth/`
- `wa-session/`
- `node_modules/`
- `estado_agentes/`
- `multi_sinais.db` e qualquer outro banco
- `backups/`
- `debug_capturas/`
- logs
- históricos operacionais
- identificadores de contas
- chaves e tokens
- dados de mercado sem autorização para redistribuição
- arquivos antigos que contenham credenciais, mesmo que comentadas

## Atenção especial

O README antigo dentro de `docs/` contém referência a uma chave que já teria sido exposta anteriormente. Não publique esse documento sem removê-la. Caso a chave ainda exista, ela precisa ser revogada e substituída.

## Estrutura mínima recomendada para a candidatura

```text
README.md
README.pt-BR.md
LICENSE
requirements.txt
package.json
.env.example
.gitignore
motor_multi.py
painel_shadow.py
backtest_carteira.py
backtest_candidatos_v10.py
backtest_candidatos_v13.py
backtest_filtros_v12.py
analise_alvos_sweep.py
analise_eventos.py
pesquisa/
robos_ntsl/
docs/
```

Publique somente scripts que estejam claramente classificados como atuais, históricos ou reprovados.

## Antes de enviar a candidatura

1. Escolha e adicione uma licença open source.
2. Confira se o repositório abre sem dados privados.
3. Inclua pelo menos um exemplo reproduzível com dados sintéticos ou pequenos dados autorizados.
4. Adicione um teste simples que demonstre a proteção contra lookahead ou preenchimento idealizado.
5. Crie de três a cinco issues públicas correspondentes ao roadmap.
6. Verifique todo o histórico do Git, não apenas os arquivos atuais.
7. Rode uma busca por possíveis segredos antes do primeiro push.
8. Abra o repositório em uma janela anônima e confirme o que qualquer pessoa consegue visualizar.
