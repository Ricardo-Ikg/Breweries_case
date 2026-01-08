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

Durante o desenvolvimento, algumas decisões foram tomadas considerando **escopo, tempo e budget**.

### Armazenamento

* **Atual:** armazenamento local
* **Trade-off:** simplicidade vs. escalabilidade
* **Justificativa:** evitar custos de cloud para um case técnico

### Observabilidade

* **Atual:** logs e status de tarefas via Airflow
* **Trade-off:** implementação simples vs. stack completa de monitoramento
* **Justificativa:** foco no pipeline funcional e correto

### Tecnologias

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

### 📊 Observabilidade

* Integração com Prometheus / Grafana
* Alertas de falha de pipeline
* Métricas de qualidade de dados

### ☁️ Cloud Storage

* Armazenamento das camadas Bronze/Silver/Gold em S3, GCS ou ADLS
* Separação entre compute e storage
* Maior escalabilidade e resiliência

### 🔁 Evolução de Schema

* Controle de versões
* Processamento incremental

### 🚀 CI/CD

* GitHub Actions para testes automatizados
* Deploy automatizado de DAGs

Essas melhorias não foram implementadas por **restrições de budget**, conforme permitido pelo case.

---

## 📌 Considerações Finais

Este projeto demonstra uma abordagem sólida de Engenharia de Dados, com foco em organização, qualidade, clareza arquitetural e boas práticas de mercado.
