# WOCT - Wealth Operations Control Tower

## Visão geral

O **Wealth Operations Control Tower** é um projeto autoral de análise e controle operacional desenvolvido para simular uma estrutura de monitoramento de operações financeiras em um ambiente de Wealth Management.

O projeto representa uma camada de controle operacional capaz de:

- Monitorar operações financeiras;
- Acompanhar o ciclo de vida das transações;
- Identificar operações pendentes;
- Medir tempo de processamento;
- Avaliar cumprimento de SLA;
- Classificar riscos operacionais;
- Identificar exceções;
- Preparar dados para dashboards e indicadores;
- Apoiar decisões operacionais com base em dados.

Todos os dados utilizados inicialmente são **fictícios e gerados localmente**, sem utilização de informações reais de clientes, instituições financeiras ou operações de mercado.

---

## Objetivo do projeto

O objetivo é demonstrar como dados operacionais podem ser transformados em informações úteis para uma equipe de Operations, Middle Office, Settlement ou Reconciliation.

Em ambientes financeiros, não basta saber que uma operação foi recebida. É necessário acompanhar:

1. Quando a operação foi recebida;
2. Qual é o tipo de operação;
3. Qual ativo ou classe de ativo está envolvido;
4. Qual é o valor financeiro;
5. Em qual etapa do processo a operação está;
6. Qual equipe é responsável;
7. Se existem pendências ou exceções;
8. Se a operação está dentro do SLA;
9. Se existe risco operacional;
10. Se a operação foi concluída e reconciliada corretamente.

O projeto foi criado para simular esse fluxo de controle.

---

## Problema de negócio

Operações financeiras podem passar por diversas etapas antes de serem concluídas.

Quando o acompanhamento é realizado manualmente, podem surgir problemas como:

- Falta de visibilidade sobre operações pendentes;
- Dificuldade para identificar atrasos;
- Falta de padronização na classificação de status;
- Exceções não tratadas;
- Divergências entre sistemas;
- Falta de clareza sobre o responsável por cada operação;
- Dificuldade para medir o cumprimento de SLA;
- Indicadores construídos manualmente;
- Risco de perda de prazos de liquidação;
- Baixa rastreabilidade do ciclo de vida da operação.

O Wealth Operations Control Tower busca resolver esse problema criando uma estrutura simples de dados, regras de negócio e indicadores operacionais.

---

## Fluxo geral do projeto

O fluxo atual é:

```text
Geração de dados fictícios
        ↓
Arquivo de operações brutas
        ↓
Validação da qualidade dos dados
        ↓
Aplicação das regras de negócio
        ↓
Cálculo de métricas operacionais
        ↓
Classificação de SLA e risco
        ↓
Arquivo de operações enriquecidas
        ↓
Reconciliação
        ↓
Consultas SQL
        ↓
Dashboard operacional
