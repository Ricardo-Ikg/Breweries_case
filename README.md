# 🍺 Breweries Data Engineering Case

Este repositório contém a solução para o **BEES Data Engineering – Breweries Case**, cujo objetivo é demonstrar a construção de um pipeline de dados completo a partir do consumo de uma API pública, seguindo o padrão de **arquitetura Medallion (Bronze / Silver / Gold)**, com orquestração, testes e documentação adequada fileciteturn0file0.

---

## 🎯 Objetivo do Case

O objetivo do projeto é:

* Consumir dados da **Open Brewery DB API**
* Persistir os dados em um *data lake* seguindo o padrão **Medallion Architecture**
* Orquestrar o pipeline utilizando uma ferramenta de mercado
* Aplicar transformações, qualidade de dados e agregações
* Disponibilizar uma camada analítica pronta para consumo

---

## 🧩 Visão Geral da Arquitetura

O pipeline foi desenhado seguindo o conceito de camadas de dados (*Medallion Architecture*), com responsabilidades bem definidas, baixo acoplamento entre etapas e foco em reprocessamento e confiabilidade.

### 📐 Diagrama de Arquitetura (Arquitetura + Ferramentas)

O diagrama abaixo representa não apenas o fluxo lógico da arquitetura Medallion, mas também **as ferramentas utilizadas em cada etapa do pipeline**, deixando explícito o papel de cada tecnologia dentro da solução.

```
┌──────────────────────────────────────────────┐
│            Open Brewery DB API               │
│        (Fonte externa de dados REST)         │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                Apache Airflow                │
│        Orquestração e agendamento             │
│  - Scheduling                                 │
│  - Retries                                   │
│  - Error handling                             │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                 Bronze Layer                 │
│         Armazenamento Local (Docker)          │
│  - Python                                    │
│  - Requests                                  │
│  - Dados brutos (raw JSON)                   │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                 Silver Layer                 │
│         Armazenamento Local (Docker)          │
│  - Python                                    │
│  - Pandas                                    │
│  - Limpeza e padronização                    │
│  - Validação de schema                       │
│  - Organização por localização               │
└───────────────────────┬──────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                  Gold Layer                  │
│         Armazenamento Local (Docker)          │
│  - Python                                    │
│  - Agregações analíticas                     │
│  - Breweries por tipo e localização           │
└──────────────────────────────────────────────┘
```

📌 **Observação:** Todas as camadas de dados são atualmente persistidas em armazenamento local, executando dentro de containers Docker. Essa decisão foi tomada para evitar custos de cloud, mas a arquitetura foi pensada para permitir substituição direta por serviços como **S3 / GCS / ADLS** sem grandes mudanças estruturais.

---

## 🏗️ Camadas do Data Lake

### 🟤 Bronze Layer

**Responsabilidade:**

* Ingestão dos dados diretamente da API
* Persistência no formato bruto, sem transformações estruturais

**Decisões:**

* Manter o dado o mais próximo possível da fonte
* Facilitar reprocessamentos futuros

---

### ⚪ Silver Layer

**Responsabilidade:**

* Limpeza e padronização dos dados
* Aplicação de regras de qualidade
* Transformação para estrutura tabular
* Organização lógica para consumo posterior

**Transformações realizadas:**

* Seleção e normalização de colunas
* Validações de schema
* Tratamento de valores nulos
* Organização por atributos de localização

---

### 🟡 Gold Layer

**Responsabilidade:**

* Criação de uma visão analítica agregada

**Resultado:**

* Quantidade de cervejarias por **tipo** e **localização**
* Dataset pronto para consumo por ferramentas analíticas ou BI

---

## 🔄 Orquestração

O pipeline é orquestrado utilizando **Apache Airflow**, escolhido por:

* Ampla adoção no mercado
* Facilidade de observabilidade via UI
* Suporte nativo a retries, SLA e dependências
* Clareza na modelagem do fluxo de dados

As DAGs estão organizadas de forma modular, refletindo as camadas do data lake.

---

## 🧪 Testes

O projeto contempla testes automatizados, organizados em:

* **Testes unitários**: validação de funções isoladas
* **Testes de integração**: validação do fluxo entre camadas
* **Testes de DAGs**: verificação da estrutura e dependências do Airflow

Isso garante maior confiabilidade, facilidade de manutenção e segurança para refatorações.

---

## 🐳 Containerização

Todo o ambiente é executado via **Docker**, o que garante:

* Reprodutibilidade
* Facilidade de setup
* Isolamento de dependências

A escolha por Docker também atende ao critério de modularização solicitado no case fileciteturn0file0.

---

## ⚖️ Trade-offs e Decisões de Engenharia

Durante o desenvolvimento, algumas decisões foram tomadas considerando **escopo, tempo, custo e simplicidade operacional**, conforme esperado para um case técnico.

---

### 🗄️ Trade-off: SQLite vs PostgreSQL (Metadata / Airflow)

No ambiente atual do projeto, foi utilizado **SQLite** como banco de metadados do Airflow.

**Decisão tomada:**

* Utilizar SQLite em vez de PostgreSQL

**Motivos:**

* Simplicidade de setup e execução local
* Redução de dependências e configuração adicional
* Facilidade de reprodução do ambiente para avaliadores

**Trade-off assumido:**

* SQLite **não é recomendado para ambientes produtivos** ou de alta concorrência
* Limitações de escalabilidade e concorrência

**Cenário de produção:**

* A escolha adequada seria **PostgreSQL**, garantindo:

  * Maior robustez
  * Melhor suporte a concorrência
  * Maior confiabilidade para execução paralela de DAGs

Essa decisão foi consciente e alinhada ao escopo do case, priorizando clareza e reprodutibilidade.

---

### ☁️ Armazenamento

* **Atual:** armazenamento local
* **Trade-off:** simplicidade vs. escalabilidade
* **Justificativa:** evitar custos de cloud para um case técnico

---

### 📊 Observabilidade

* **Atual:** logs e status nativos do Airflow
* **Trade-off:** implementação simples vs. stack completa de monitoramento
* **Justificativa:** foco no pipeline funcional e correto

---

### ⚙️ Tecnologias

* Não foram utilizadas ferramentas como Delta Lake, Great Expectations ou serviços cloud gerenciados para manter o projeto acessível e reproduzível localmente.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Docker
* Docker Compose

### Passos

```bash
# Clonar o repositório
git clone https://github.com/Ricardo-Ikg/Breweries_case.git

# Entrar no projeto
cd Breweries_case

# Subir os containers
docker compose up -d
```

A interface do Airflow ficará disponível em:

```
http://localhost:8080
```

---

## 🔮 Melhorias Futuras

Esta seção descreve evoluções naturais do pipeline para um ambiente de produção, considerando **boas práticas de Engenharia de Dados**, bem como os **trade-offs de escopo, custo e complexidade** discutidos durante o desenvolvimento do case.

---

### 📊 Data Quality (Qualidade de Dados)

O pipeline já possui um **primeiro nível de Data Quality** por meio do uso de validações de schema e regras implementadas com **Pandera**, garantindo:

* Conformidade de tipos de dados
* Presença de colunas obrigatórias
* Regras básicas de consistência antes da promoção dos dados

Esse uso do Pandera pode ser considerado um **início de Data Quality**, focado em validações estruturais e de schema.

Como evolução futura, o processo poderia ser expandido para incluir:

* Métricas quantitativas de qualidade, como:

  * Percentual de registros inválidos
  * Percentual de valores nulos por coluna
  * Distribuição de valores inesperados
* Persistência dessas métricas para análise histórica
* Definição de **quality gates** entre Silver e Gold

Essas melhorias aumentariam significativamente a **confiabilidade, governança e observabilidade dos dados**.

---

### 📈 Monitoramento e Alertas

Em um cenário produtivo, o monitoramento poderia ser expandido para incluir:

* Métricas de execução das DAGs:

  * Tempo de execução por tarefa
  * Volume de dados processados
  * Taxa de falhas
* Alertas automáticos para:

  * Falhas de DAG
  * Quebra de SLA
  * Anomalias de qualidade de dados

Exemplos de implementação:

* Integração com **Datadog** para observabilidade centralizada (métricas, logs e alertas)
* Alternativamente, uso de **Prometheus + Grafana** para coleta e visualização de métricas
* Alertas via e-mail, Slack ou ferramentas corporativas

No escopo do case, optou-se por utilizar os **logs e status nativos do Airflow**, evitando aumento de complexidade operacional e custos adicionais.

---

### ☁️ Armazenamento em Cloud (ADLS / S3 / GCS)

Uma evolução natural do projeto seria mover o armazenamento local para um **data lake em cloud**, como:

* Azure Data Lake Storage (ADLS)
* Amazon S3
* Google Cloud Storage

Benefícios:

* Separação clara entre **compute e storage**
* Escalabilidade
* Maior resiliência

A não implementação no case se deu por **restrição de budget**, mantendo o projeto facilmente reproduzível em ambiente local.

---

### ⚙️ Trade-off: Spark dentro do Airflow

Durante o desenho da solução, foi considerado o uso de **Apache Spark** para processamento distribuído.

**Decisão tomada:**

* Não utilizar Spark neste case

**Motivos:**

* Volume de dados reduzido, não justificando processamento distribuído
* Aumento significativo de complexidade operacional
* Overhead desnecessário para um pipeline batch simples

O Airflow foi utilizado **exclusivamente como orquestrador**, enquanto o processamento foi mantido em Python, respeitando o princípio de simplicidade e adequação ao problema.

---

### ☸️ Trade-off: Não utilização de Kubernetes

Embora Kubernetes seja amplamente utilizado em ambientes de dados modernos, ele não foi adotado neste projeto pelos seguintes motivos:

* Complexidade operacional elevada para o escopo do case
* Overhead de setup e manutenção
* Ausência de benefícios claros para um pipeline de batch simples

A escolha por **Docker Compose** garantiu:

* Reprodutibilidade
* Facilidade de execução local
* Menor curva de aprendizado para avaliadores

Em um ambiente corporativo de larga escala, Kubernetes poderia ser considerado para:

* Alta disponibilidade
* Escalonamento automático
* Ambientes multi-tenant

---

## 📌 Considerações Finais

Este projeto demonstra uma abordagem sólida de Engenharia de Dados, com foco em organização, qualidade, clareza arquitetural e boas práticas de mercado.
