---
name: atlas-guardiao
description: Skill do projeto Atlas Voice. Use sempre que JP mencionar Modo Guardião, segurança, sentinela, câmeras, rastreamento, modo roubado, proteção familiar, áreas seguras, Pulse, localização de dispositivos, ou qualquer funcionalidade de segurança e vigilância do Atlas Voice. Esta skill contém a especificação completa e fechada do Modo Guardião — pronto para desenvolvimento na V4.
---

# Atlas Guardião — Especificação Final e Fechada

**Status:** ✅ Documentado e pronto para desenvolvimento  
**Fase de desenvolvimento:** V4 — Ecossistema  
**Núcleos ativos:** ATLAS (segurança e decisão) + LYRA (família e cuidado)

---

## Propósito

O Modo Guardião é a camada de proteção do Atlas Voice.  
Funciona 24h, silenciosamente, sem depender do usuário pedir.

Três pilares:
1. Localizar rapidamente qualquer dispositivo do usuário
2. Proteger a família e ambientes pessoais (carro, casa, filhos)
3. Atuar como sistema de segurança pessoal e digital

---

## Ativação

O usuário pode ativar por três formas — todas equivalentes:

| Forma | Como |
|---|---|
| **Voz** | "Atlas, modo sentinela" |
| **Toque longo** | Segurar o ícone flutuante por 2 segundos |
| **Digitação** | Digitar o comando — fallback total |

---

## Núcleos Internos (Arquitetura Fechada)

### GPS Core Engine
- Localização contínua com atualização automática
- Precisão híbrida: GPS + A-GPS + GLONASS + Galileo + Wi-Fi Positioning + BLE + triangulação de torres
- Trilha completa das últimas 24h

### Secure ID
- Detecção de troca de chip (SIM swap)
- Proteção contra tentativas de desligamento
- Monitoramento de acesso suspeito
- Criptografia AES 256
- Protocolo seguro AtlasLink

### Family Mesh
- Rede silenciosa sincronizada entre dispositivos familiares
- Checagem Pulse — verificação automática silenciosa
- Alertas de entrada/saída de zonas seguras

### BlueWave UI
- Visual definitivo: fundo azul profundo, ondulação suave, brilho minimalista
- Ícone flutuante overlay — sempre visível sobre qualquer app

### Guardian Voice Commands
- Todos os comandos ativos e prontos para uso imediato

### Guardian Cloud
- Histórico de rastreamento: 24h / 7 dias / 30 dias / 90 dias
- Atlas Signal — comunicação entre dispositivos mesmo com bateria baixa

---

## Funções Ativas (Completas e Fechadas)

### Localização em Tempo Real
- Qualquer dispositivo cadastrado
- Precisão híbrida
- Trilha de 24h
- Status online/offline, distância do usuário, última atualização

### Modo Roubado
- Rastreio contínuo a cada 10 segundos
- Tela invisível (modo stealth)
- Trava remota do dispositivo
- Alertas automáticos
- Registro de tentativas de desligamento
- Registro de SIM swap
- Compartilhamento rápido com contato confiável
- Envio de localização direto para a polícia

### Áreas Seguras
- Criação de zonas com raio configurável (50m–2km)
- Nomear áreas (Casa, Trabalho, Escola)
- Associar pessoas monitoradas
- Alertas automáticos de entrada e saída

### Proteção Familiar
- Cadastro: filhos, parceiros, pais
- Localização atual + histórico + status de bateria
- Pulse — checagem silenciosa automática
- Botão de emergência individual por pessoa

### Proteção Digital
- Bloqueio remoto de apps e dados
- Monitoramento de acessos estranhos
- Anti-SIM swap ativo

### Alertas Inteligentes (Todos Fechados)
| Alerta | Gatilho |
|---|---|
| Saída de área segura | Dispositivo sai da zona definida |
| Entrada em área segura | Dispositivo entra na zona definida |
| Dispositivo offline | Sem sinal por tempo configurável |
| Aproximação suspeita | Dispositivo desconhecido se aproxima repetidamente |
| Risco de troca de chip | Detecção de SIM swap |
| Movimentação incomum | Padrão fora do normal |
| Bateria crítica | Nível baixo de bateria |

---

## Telas do App (8 Telas — Versão Definitiva)

1. **Abertura** — "Bem-vindo ao Modo Guardião. Sua proteção começa aqui." + Botão Ativar
2. **Cadastro de Dispositivos** — lista automática + adicionar por QR
3. **Mapa de Localização em Tempo Real** — pontos luminosos azuis, ações rápidas
4. **Modo Roubado** — tela própria com confirmação + todas as ações
5. **Áreas Seguras** — mapa, criação, edição, alertas
6. **Proteção Familiar** — lista de pessoas + Pulse + emergência
7. **Central de Alertas** — feed limpo e direto
8. **Configurações Avançadas** — frequência, stealth, bloqueio, histórico, atalhos de voz

---

## Comandos de Voz (Prontos para Produção)

### Localização
- "Atlas, onde está meu aparelho?"
- "Atlas, mostra no mapa."
- "Atlas, última localização."

### Emergência
- "Atlas, emergência agora!"
- "Atlas, ativar Modo Roubado."
- "Atlas, manda localização pra minha família."

### Família
- "Atlas, meus filhos chegaram na escola?"
- "Atlas, ativa o Pulse."

### Segurança Digital
- "Atlas, bloqueia tudo."
- "Atlas, alerta de segurança."

### Sentinela
- "Atlas, modo sentinela."

---

## Status Final

| Item | Status |
|---|---|
| Arquitetura | ✅ Finalizada |
| Telas (8) | ✅ Finalizadas |
| Funções | ✅ Finalizadas |
| Fluxos | ✅ Finalizados |
| Comandos de voz | ✅ Finalizados |
| Segurança | ✅ Finalizada |
| Visual BlueWave | ✅ Finalizado |
| Lógica | ✅ Finalizada |
| Operação | ✅ Finalizada |

---

## Posição no Roadmap

| Fase | Entrega do Guardião |
|---|---|
| V3 | Overlay no Android, ativação por voz/toque/texto |
| V4 | Guardião completo — GPS, família, câmeras, emergência |
| V6+ | Sentinela nas ruas, vigilância empresarial, presença total |

---

## Regra de Desenvolvimento

Nenhuma função do Guardião começa antes da V3 estar fechada.  
O documento está pronto — o código segue quando a fase chegar.

---

## Declaração de Produção

Este módulo está em estado de produção imediata.  
Se entregue a uma equipe de desenvolvimento hoje, a implementação pode iniciar sem perguntas.  
Nada falta. Nada está pendente. O ciclo está fechado.

---

*Atlas Voice — Modo Guardião — Especificação Final*  
*JP Silva — Manaus, Brasil*  
*Skill viva — atualizada conforme o desenvolvimento avança*
