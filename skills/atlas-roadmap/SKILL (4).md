---
name: atlas-roadmap
description: Skill do projeto Atlas Voice. Use sempre que o JP mencionar fases, roadmap, próximos passos, V2, V3, expansão, visão do projeto, ou quando for tomar decisões sobre o que construir a seguir. Esta skill contém o mapa completo de evolução do Atlas Voice — fases, critérios de avanço, e a visão de longo prazo.
---

# Atlas Roadmap — Fases e Visão

## A Visão

> "O Atlas Voice não é um app. É uma presença."
> "Presença contínua, não uma ferramenta."
> "O futuro não é importado. O futuro é criado por quem acredita."

Atlas Voice é o primeiro ecossistema brasileiro de inteligência por voz.  
Uma plataforma — não um produto isolado.  
Feita para qualquer pessoa, qualquer classe social.

**Quem manda:** sempre o usuário. O Atlas serve, sugere, executa — nunca decide sozinho.

---

## Níveis de Atuação — Visão Final

| Nível | Escopo |
|---|---|
| Pessoal | Rotina, saúde, foco, companheirismo |
| Doméstico | Controle da casa, segurança, câmeras |
| Segurança | Vigilância em tempo real, acionar serviços, decisões autônomas |
| Empresarial | Defesa, monitoramento, gestão |

---

## Fases do Projeto

### V1 — Fundação ← FASE ATUAL
**Status:** ✅ Funcional — em validação com uso real

**O que foi entregue:**
- Login seguro (bcrypt)
- Perfil por usuário
- Atlas e Lyra respondendo
- Troca de núcleo por comando
- Alarmes completos (criar, cancelar, monitorar)
- Lembretes com prioridade
- Memória entre sessões
- Histórico de interações
- Interface CLI

**Critério para avançar:**
```
JP usa o V1 no dia a dia real
→ anota o que falta ou incomoda
→ bugs do uso real corrigidos
→ sistema estável e confiável
→ só então inicia V2
```

**Limitações atuais:**
- Sem IA externa — respostas limitadas
- Sem internet
- Só texto — sem voz ainda
- Interface CLI — sem visual ainda

---

### V2 — Inteligência
**Status:** 🔜 Próxima fase

**O que será construído:**
- Integração com IA externa (Claude API)
- Atlas responde qualquer pergunta com inteligência real
- Memória de longo prazo real
- Interface web — painel de controle, menus, login visual
- Atlas e Lyra com identidade visual

**Stack adicional V2:**
- Claude API (Anthropic)
- Framework web (a definir — Flask ou FastAPI)
- Frontend simples (HTML/CSS ou React básico)

**Critério para avançar:**
```
Interface web funcional
→ IA respondendo de forma inteligente
→ memória persistindo entre sessões com IA
→ JP usando no dia a dia pela web
→ só então inicia V3
```

---

### V3 — Expansão Mobile
**Status:** Futuro

**O que será construído:**
- App Android nativo
- Voz real como entrada — STT com Whisper
- Voz real como saída — TTS com ElevenLabs
- 7 dias gratuitos de onboarding para novos usuários
- Experiência completa mobile-first

**Stack adicional V3:**
- Whisper (OpenAI) — Speech-to-Text
- ElevenLabs — Text-to-Speech
- Android (Kotlin ou React Native — a definir)

---

### V4 — Ecossistema
**Status:** Futuro

**O que será construído:**
- Integração IoT — controle da casa, câmeras
- Módulo saúde — Google Fit / HealthKit
- Módulo emergência — acionar contatos, serviços
- Módulo navegação — GPS e rotas
- n8n para automações complementares

---

### V5 — Escala Nacional
**Status:** Visão de médio prazo

**O que será construído:**
- Produto público — lançamento Brasil
- Modelo freemium + B2B
- Licenciamento de voz
- Custo estimado MVP: R$ 300–R$ 2.400/mês

---

### V6+ — Presença Total
**Status:** Visão de longo prazo

**O que será construído:**
- Multi-dispositivo — celular, PC, casa, carro
- Segurança e vigilância autônoma
- Robótica
- Tradução em tempo real
- Presença contínua — sempre disponível, sempre aprendendo

---

## Decisões Tomadas — Não Renegociar

| Decisão | Motivo |
|---|---|
| Interface web primeiro, app depois | Mais rápido de construir e validar |
| IA externa — não construir do zero | Velocidade e qualidade garantida |
| n8n como complemento — não substituto | Automação de fluxos, não inteligência |
| Voz é o objetivo — texto é fallback | A identidade do produto é voz |
| Validar V1 antes de avançar para V2 | Não construir sobre areia |
| Usuário sempre comanda | Princípio inegociável do produto |

---

## Regras de Avanço de Fase

```
1. Nunca iniciar fase nova sem fechar a atual
2. Critério de conclusão deve ser cumprido — não estimado
3. Backup completo antes de iniciar nova fase
4. Documento mestre atualizado antes de avançar
5. O que foi construído não pode quebrar na fase seguinte
```

---

## Próximos Passos Imediatos

1. JP usa o Atlas V1 no dia a dia real
2. Anotar o que falta ou incomoda no uso
3. Corrigir o que o uso real mostrar
4. Atualizar o documento mestre com os bugs corrigidos
5. Só depois: iniciar V2

---

## Propósito Social

Atlas Voice é para qualquer pessoa — não só para quem tem dinheiro ou formação técnica.

A visão é que uma pessoa simples, em Manaus ou em qualquer cidade do Brasil, tenha acesso ao mesmo nível de presença inteligente que grandes empresas têm com suas ferramentas.

**Isso não é só um produto. É uma missão.**

---

*Atlas Voice — Roadmap — JP Silva — Manaus, Brasil*  
*Atualizar a cada fase concluída*
