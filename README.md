# woct
Wealth Operations Control Tower - tem como objetivo dar visibilidade ao ciclo de vida das operações de Wealth Management, identificar riscos antes que se tornem problemas e apoiar a resolução de exceções.

┌──────────────────────────────────────┐
│         FONTES DE DADOS              │
│ CSV / Excel / dados simulados        │
└──────────────────┬───────────────────┘
                   ↓
┌──────────────────────────────────────┐
│       PROCESSAMENTO E QUALIDADE      │
│ Python + SQL                         │
│ Padronização · validações · regras   │
└──────────────────┬───────────────────┘
                   ↓
┌──────────────────────────────────────┐
│       CONTROLE OPERACIONAL           │
│ Status · SLA · exceções · aging      │
│ reconciliação · priorização          │
└──────────────────┬───────────────────┘
                   ↓
┌──────────────────────────────────────┐
│          CAMADA ANALÍTICA            │
│ Power BI                             │
│ KPIs · backlog · riscos · tendências │
└──────────────────────────────────────┘
