# 📊 Desafio Técnico – Projeto de Risco Bancário

## Contexto

Você está alocado em um projeto de suporte analítico a uma equipe que desenvolve projeções de risco para um banco. Seu objetivo é explorar a base de contratos bancários e gerar **features analíticas** para alimentar um módulo preditivo.

---

## 📁 Dataset

Você tem à disposição um arquivo `contratos_clientes.csv` com aproximadamente 100 mil linhas e 7 colunas:

- `id_cliente`
- `data_contrato`
- `valor_contrato`
- `prazo_meses`
- `produto`
- `score_risco`
- `inadimplente`

---

## 🛠️ Tarefas

### 1. **Feature Engineering**

Crie uma tabela agregada com as seguintes informações por `id_cliente`:

- Quantidade total de contratos
- Soma dos valores contratados
- Prazo médio dos contratos
- Score de risco médio
- Percentual de contratos inadimplentes
- Mês do contrato mais recente

---

### 2. **Segmentação de Risco**

Agrupe os clientes em 3 faixas de risco:

- **Baixo risco**: score médio ≤ 0.4  
- **Médio risco**: 0.4 < score médio ≤ 0.7  
- **Alto risco**: score médio > 0.7

Para cada grupo, calcule:

- Número total de clientes
- Taxa média de inadimplência
- Valor médio de contrato

---

### 3. **Pré-processamento para Modelo**

Crie um dataset final com as colunas:

- `id_cliente`
- `faixa_risco`
- `qtd_contratos`
- `valor_total`
- `percentual_inadimplencia`
- `prazo_medio`
- `mes_ultimo_contrato`

Salve como `dataset_final.csv`.

---

### 4. **(Opcional / Bônus)**

Liste 3 outras features que poderiam ser úteis num modelo de previsão de inadimplência. Justifique suas escolhas em um parágrafo curto.

---

## ✅ Entrega Esperada

Você deve entregar os seguintes itens:

- Um script `.py` ou notebook `.ipynb` com o código
- O arquivo `dataset_final.csv` com o resultado
- Um arquivo `resumo.md` explicando suas decisões (máximo 1 página)
- Um vídeo curto (3–5 min, link do Drive ou YouTube não listado) com explicação das suas escolhas e raciocínio

---

## 🚀 Como Entregar

1. Faça um **fork** deste repositório.
2. Suba sua solução no seu fork.
3. Preencha o `resumo.md` explicando suas decisões técnicas.
4. Envie o **link do seu repositório público** com a solução final.

> **⚠️ Importante:** *Não envie pull request para este repositório.* Apenas compartilhe o link do seu fork com a solução implementada.

---

## 🧐 O que será avaliado

- Clareza e organização do código
- Correção dos cálculos
- Raciocínio lógico e capacidade de manipular dados
- Qualidade das features criadas
- Capacidade de lidar com datas, tipos, agregações e problemas reais
