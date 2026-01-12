# 🎨 Análise Completa e Proposta de Frontend - Sistema de Devocionais

## 📋 ANÁLISE DO SISTEMA ATUAL

### 🔍 O Que o Sistema Faz

O sistema é uma **plataforma de envio automático de devocionais via WhatsApp** que:

1. **Recebe devocionais** gerados por IA (via n8n)
2. **Armazena** no banco de dados
3. **Envia automaticamente** para lista de contatos via WhatsApp
4. **Gerencia múltiplas instâncias** Evolution API
5. **Controla rate limiting** para evitar bloqueios
6. **Rastreia estatísticas** de envios
7. **Gerencia contatos** (adicionar, remover, ativar/desativar)

### 🔄 Como Funciona (Fluxo Completo)

#### **Fluxo 1: Geração e Envio Automático (n8n)**

```
1. n8n gera devocional via IA
   ↓
2. n8n envia para /api/devocional/webhook
   ↓
3. Sistema salva no banco (tabela: devocionais)
   ↓
4. Scheduler verifica horário (06:00 SP)
   ↓
5. Sistema busca devocional do dia
   ↓
6. Sistema busca contatos ativos
   ↓
7. Sistema distribui entre instâncias (round_robin)
   ↓
8. Envia mensagens com delay (3s entre cada)
   ↓
9. Registra cada envio (tabela: devocional_envios)
   ↓
10. Atualiza estatísticas dos contatos
```

#### **Fluxo 2: Envio Manual**

```
1. Usuário escolhe devocional (ou digita mensagem)
   ↓
2. Usuário escolhe contatos (ou todos ativos)
   ↓
3. Sistema envia via API
   ↓
4. Distribui entre instâncias
   ↓
5. Registra envios
```

#### **Fluxo 3: Gerenciamento de Contatos**

```
1. Usuário adiciona contato (telefone + nome)
   ↓
2. Sistema valida e salva
   ↓
3. Contato fica ativo por padrão
   ↓
4. Recebe devocionais automáticos
   ↓
5. Sistema rastreia: total_sent, last_sent
```

### 📊 Entidades do Sistema

#### **1. Devocional**
- ID, título, conteúdo, data
- Versículos (principal e apoio)
- Metadados (autor, tema, palavras-chave)
- Status (enviado, não enviado)
- Total de envios

#### **2. Contato (DevocionalContato)**
- ID, telefone, nome
- Status (ativo/inativo)
- Estatísticas (total_sent, last_sent)
- Timestamps (created_at, updated_at)

#### **3. Envio (DevocionalEnvio)**
- ID, devocional_id, recipient_phone, recipient_name
- Mensagem enviada (texto completo)
- Status (sent, failed, retrying, blocked)
- Instância que enviou
- Erros e retries
- Timestamps

#### **4. Instância Evolution API**
- Nome, URL, API Key
- Status (ACTIVE, INACTIVE, ERROR)
- Estatísticas (mensagens enviadas hoje/hora)
- Limites configurados

---

## 🎯 PROPOSTA DE FRONTEND COMPLETO

### 🏗️ Arquitetura Proposta

**Stack Tecnológico:**
- **Framework**: React 18+ com TypeScript
- **Roteamento**: React Router v6
- **Estado Global**: Zustand ou Context API
- **UI Components**: Shadcn/ui ou Material-UI
- **Formulários**: React Hook Form + Zod
- **Gráficos**: Recharts ou Chart.js
- **Tabelas**: TanStack Table (React Table)
- **Autenticação**: JWT tokens
- **HTTP Client**: Axios
- **Notificações**: React Hot Toast
- **Data Fetching**: React Query (TanStack Query)

### 🔐 Sistema de Autenticação

#### **Backend (a implementar)**
```python
# Novo router: backend/app/routers/auth.py
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh
- GET /api/auth/me
- POST /api/auth/change-password
```

#### **Frontend**
- Tela de Login
- Proteção de rotas
- Refresh token automático
- Logout
- Perfil do usuário

---

## 📱 ESTRUTURA COMPLETA DO FRONTEND

### 🗂️ Módulos e Páginas

#### **1. AUTENTICAÇÃO** 🔐

**1.1. Login (`/login`)**
- Formulário: email/usuário + senha
- Validação de campos
- Mensagens de erro
- "Lembrar-me" (opcional)
- Link "Esqueci minha senha" (futuro)

**1.2. Recuperação de Senha (`/forgot-password`)** (Futuro)
- Formulário: email
- Envio de link de recuperação

---

#### **2. DASHBOARD** 📊

**2.1. Dashboard Principal (`/dashboard`)**

**Cards de Resumo:**
- Total de Contatos (ativos/inativos)
- Devocionais Enviados Hoje
- Taxa de Sucesso (últimas 24h)
- Instâncias Ativas/Total
- Mensagens Enviadas Hoje (por instância)

**Gráficos:**
- Envios por dia (últimos 7/30 dias)
- Taxa de sucesso/falha (pizza)
- Distribuição por instância (barras)
- Horários de envio (heatmap)

**Tabela de Atividades Recentes:**
- Últimos 10 envios
- Status, destinatário, horário
- Link para detalhes

**Alertas/Notificações:**
- Instâncias offline
- Taxa de erro alta
- Limites próximos

---

#### **3. DEVOCIONAIS** 📖

**3.1. Lista de Devocionais (`/devocionais`)**

**Funcionalidades:**
- Tabela com todos os devocionais
- Filtros:
  - Por data (range)
  - Por status (enviado/não enviado)
  - Por autor
  - Por tema
- Busca por texto
- Ordenação (data, título, total de envios)
- Paginação
- Ações:
  - Ver detalhes
  - Editar (se não enviado)
  - Enviar agora
  - Duplicar
  - Excluir (se não enviado)

**Colunas da Tabela:**
- Data
- Título
- Autor
- Tema
- Status (enviado/não enviado)
- Total de Envios
- Ações

**3.2. Detalhes do Devocional (`/devocionais/:id`)**

**Visualização:**
- Título, conteúdo formatado
- Versículos (principal e apoio)
- Metadados (autor, tema, palavras-chave)
- Data de criação
- Status e estatísticas

**Ações:**
- Editar (se não enviado)
- Enviar agora
- Ver histórico de envios
- Duplicar

**3.3. Criar/Editar Devocional (`/devocionais/novo`, `/devocionais/:id/editar`)**

**Formulário:**
- Título (texto)
- Conteúdo (textarea rico ou markdown)
- Versículo Principal:
  - Texto
  - Referência
- Versículo de Apoio:
  - Texto
  - Referência
- Metadados:
  - Autor (select ou texto)
  - Tema (texto)
  - Palavras-chave (tags)
- Data (date picker)
- Preview da mensagem formatada
- Validação de campos

**3.4. Enviar Devocional (`/devocionais/:id/enviar`)**

**Formulário de Envio:**
- Seleção de contatos:
  - Todos ativos
  - Seleção manual (checkboxes ou multi-select)
  - Filtros (tags, grupos)
- Opções:
  - Delay entre mensagens (slider)
  - Instância específica (ou automática)
  - Agendar envio (date/time picker)
- Preview: quantos contatos receberão
- Botão "Enviar Agora" ou "Agendar"
- Progresso do envio (modal)

---

#### **4. CONTATOS** 👥

**4.1. Lista de Contatos (`/contatos`)**

**Funcionalidades:**
- Tabela com todos os contatos
- Filtros:
  - Status (ativo/inativo)
  - Tags
  - Último envio (range de datas)
  - Busca por nome/telefone
- Ordenação (nome, telefone, total_sent, last_sent)
- Paginação
- Seleção múltipla
- Ações em massa:
  - Ativar/Desativar
  - Adicionar tag
  - Remover tag
  - Excluir
  - Enviar mensagem personalizada

**Colunas da Tabela:**
- Checkbox (seleção)
- Nome
- Telefone (formatado)
- Status (badge ativo/inativo)
- Total de Envios
- Último Envio
- Tags (chips)
- Ações (menu)

**4.2. Adicionar Contato (`/contatos/novo`)**

**Formulário:**
- Nome (texto, obrigatório)
- Telefone (máscara, obrigatório, validação)
- Tags (multi-select ou input tags)
- Status (ativo por padrão)
- Notas (textarea opcional)
- Validação de telefone único

**4.3. Editar Contato (`/contatos/:id/editar`)**

**Formulário:**
- Mesmos campos do criar
- Histórico de envios (tabela)
- Estatísticas:
  - Total de envios
  - Taxa de sucesso
  - Último envio
  - Primeiro envio

**4.4. Detalhes do Contato (`/contatos/:id`)**

**Visualização:**
- Informações do contato
- Estatísticas
- Histórico de envios (tabela)
- Gráfico de envios ao longo do tempo
- Tags
- Ações:
  - Editar
  - Ativar/Desativar
  - Enviar mensagem
  - Excluir

**4.5. Importar Contatos (`/contatos/importar`)**

**Funcionalidades:**
- Upload de CSV/Excel
- Template para download
- Preview dos dados
- Validação antes de importar
- Mapeamento de colunas
- Opções:
  - Atualizar existentes
  - Pular duplicados
  - Adicionar tags

---

#### **5. ENVIOS** 📤

**5.1. Histórico de Envios (`/envios`)**

**Funcionalidades:**
- Tabela com todos os envios
- Filtros:
  - Por status (sent, failed, retrying, blocked)
  - Por data (range)
  - Por destinatário
  - Por devocional
  - Por instância
- Busca
- Ordenação
- Paginação

**Colunas da Tabela:**
- Data/Hora
- Destinatário (nome + telefone)
- Devocional (link)
- Status (badge colorido)
- Instância
- Mensagem (truncada, expandir)
- Erro (se houver)
- Retries
- Ações (ver detalhes, reenviar)

**5.2. Detalhes do Envio (`/envios/:id`)**

**Visualização:**
- Informações completas do envio
- Mensagem completa
- Logs de tentativas
- Erros detalhados
- Ação: Reenviar

**5.3. Envio Manual (`/envios/novo`)**

**Formulário:**
- Seleção de mensagem:
  - Usar devocional existente (select)
  - Ou digitar mensagem personalizada (textarea)
- Seleção de destinatários:
  - Todos ativos
  - Seleção manual
  - Filtros
- Opções:
  - Delay
  - Instância
  - Agendar
- Enviar

---

#### **6. INSTÂNCIAS** 🔌

**6.1. Gerenciar Instâncias (`/instancias`)**

**Funcionalidades:**
- Lista de instâncias configuradas
- Status de cada instância (cards ou tabela)
- Health check manual
- Estatísticas por instância:
  - Mensagens enviadas hoje
  - Mensagens enviadas nesta hora
  - Limites configurados
  - Taxa de sucesso
- Ações:
  - Ver detalhes
  - Configurar perfil
  - Testar conexão
  - Editar configuração (futuro)

**6.2. Detalhes da Instância (`/instancias/:nome`)**

**Visualização:**
- Nome, URL, status
- Estatísticas detalhadas
- Gráfico de uso ao longo do tempo
- Histórico de erros
- Configurações:
  - Display name
  - Limites (hora/dia)
  - Prioridade
  - Enabled/Disabled

**6.3. Configurar Instâncias (`/instancias/configurar`)** (Futuro)

**Formulário:**
- Adicionar/Editar instância
- Campos: nome, URL, API Key, display_name, limites, prioridade
- Validação
- Teste de conexão

---

#### **7. ESTATÍSTICAS** 📈

**7.1. Relatórios (`/estatisticas`)**

**Gráficos e Métricas:**
- Envios por período (linha)
- Taxa de sucesso/falha (pizza)
- Distribuição por instância (barras)
- Top destinatários (tabela)
- Horários de maior envio (heatmap)
- Evolução de contatos (área)
- Taxa de crescimento

**Filtros:**
- Período (hoje, semana, mês, customizado)
- Instância específica
- Status

**Exportação:**
- PDF
- Excel/CSV
- Compartilhar link

---

#### **8. CONFIGURAÇÕES** ⚙️

**8.1. Configurações Gerais (`/configuracoes`)**

**Aba: Sistema**
- Horário de envio automático (time picker)
- Delay entre mensagens (slider)
- Limites globais (hora/dia)
- Estratégia de distribuição (select)
- vCard automático (toggle)
- Webhook secret (input password)

**Aba: Instâncias**
- Lista de instâncias
- Adicionar/Editar/Remover
- Configurações individuais

**Aba: Notificações** (Futuro)
- Email de alertas
- Webhooks
- Integrações

**Aba: Usuários** (Futuro)
- Lista de usuários
- Permissões
- Roles

**8.2. Perfil do Usuário (`/perfil`)**

**Formulário:**
- Nome
- Email
- Foto (upload)
- Alterar senha
- Preferências (tema, idioma)

---

#### **9. TAGS E SEGMENTAÇÃO** 🏷️ (Futuro - Mini CRM)

**9.1. Gerenciar Tags (`/tags`)**

**Funcionalidades:**
- Lista de tags
- Criar/Editar/Excluir
- Cor da tag
- Contatos por tag
- Estatísticas por tag

**9.2. Segmentação (`/segmentos`)**

**Funcionalidades:**
- Criar segmentos (grupos de contatos)
- Filtros avançados:
  - Por tags
  - Por estatísticas
  - Por data de último envio
  - Por status
- Salvar segmentos
- Enviar para segmento

---

### 🎨 Design System

#### **Cores Principais**
- Primária: Azul espiritual (#1E3A8A)
- Secundária: Verde esperança (#10B981)
- Sucesso: Verde (#22C55E)
- Erro: Vermelho (#EF4444)
- Aviso: Amarelo (#F59E0B)
- Info: Azul (#3B82F6)

#### **Componentes Reutilizáveis**
- Button (variantes: primary, secondary, danger, ghost)
- Input (text, number, email, phone, date, time)
- Select (single, multi)
- Table (com sorting, filtering, pagination)
- Card
- Modal/Dialog
- Toast/Notification
- Badge
- Tabs
- Form (com validação)
- Loading/Spinner
- Empty State
- Error Boundary

---

### 📱 Responsividade

- **Desktop**: Layout completo com sidebar
- **Tablet**: Sidebar colapsável
- **Mobile**: Menu hambúrguer, cards ao invés de tabelas

---

### 🔒 Segurança

- Autenticação JWT
- Refresh tokens
- Proteção de rotas
- Validação de inputs
- Sanitização de dados
- HTTPS obrigatório
- Rate limiting no frontend (opcional)

---

### 🚀 Performance

- Code splitting por rota
- Lazy loading de componentes
- Cache de dados (React Query)
- Otimização de imagens
- Debounce em buscas
- Virtualização de listas grandes

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### **Fase 1: Base e Autenticação**
- [ ] Setup do projeto (React + TypeScript + Vite)
- [ ] Configuração de roteamento
- [ ] Sistema de autenticação (backend + frontend)
- [ ] Tela de login
- [ ] Proteção de rotas
- [ ] Layout base (header, sidebar, footer)

### **Fase 2: Módulos Principais**
- [ ] Dashboard
- [ ] Lista de Devocionais
- [ ] Criar/Editar Devocional
- [ ] Lista de Contatos
- [ ] Criar/Editar Contato
- [ ] Histórico de Envios

### **Fase 3: Funcionalidades Avançadas**
- [ ] Envio manual
- [ ] Gerenciamento de Instâncias
- [ ] Estatísticas e Relatórios
- [ ] Configurações

### **Fase 4: Melhorias**
- [ ] Tags e Segmentação
- Importação de contatos
- Exportação de relatórios
- Notificações em tempo real
- Dark mode

---

## 🎯 PRÓXIMOS PASSOS

1. **Revisar esta proposta** e decidir o que implementar
2. **Priorizar funcionalidades** (MVP vs Completo)
3. **Definir design** (mockups ou usar template)
4. **Implementar autenticação no backend**
5. **Começar pelo Dashboard** e módulos principais

---

**Esta é uma proposta completa. Podemos ajustar conforme suas necessidades!** 🚀

