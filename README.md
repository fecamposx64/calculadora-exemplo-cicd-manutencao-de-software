# Calculadora API — Projeto-demo de CI/CD

Projeto-exemplo para a mini-aula sobre **Integração Contínua (CI)** e
**Entrega/Implantação Contínua (CD)** usando **GitHub Actions**.

> 🎯 Este README é o **guia de execução do demo ao vivo**.
> Todos os comandos, falas sugeridas e amarrações com a teoria estão aqui.
> Use junto com o `ROTEIRO-DE-FALA.md` da pasta-mãe.

---

## 📂 Estrutura

```
demo-projeto/
├── app/
│   ├── calculator.py          # Lógica de negócio (testável isoladamente)
│   └── main.py                # API FastAPI
├── tests/
│   ├── test_calculator.py     # Testes unitários puros
│   └── test_main.py           # Testes de integração (HTTP)
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # ⭐ O coração do demo: o pipeline
├── pyproject.toml             # Config do ruff + pytest
└── requirements.txt
```

A separação **lógica de negócio (`calculator.py`) ↔ camada HTTP (`main.py`)**
é proposital: permite testes unitários rapidíssimos e mostra uma boa
prática de arquitetura. Vale mencionar isso na hora.

---

## 🚀 Setup local (faça **antes** da aula)

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Validar tudo (mesmo que o pipeline vai rodar)
ruff check app tests
ruff format --check app tests
pytest

# 4. Subir o servidor pra confirmar que sobe
uvicorn app.main:app --reload
# Acesse: http://localhost:8000/docs
```

Se passou tudo localmente, vai passar no GitHub. **Nunca dê push sem
rodar local antes** — isso é a regra mais básica de quem usa CI/CD bem.

---

## 🎯 O Pipeline — visão geral

O arquivo `.github/workflows/ci-cd.yml` define **4 jobs**:

```
   ┌──────────┐    ┌──────────┐
   │   lint   │    │   test   │   ← rodam em paralelo (rápido!)
   └────┬─────┘    └─────┬────┘
        └────────┬───────┘
                 ▼
            ┌─────────┐
            │  build  │              ← só roda se lint+test passaram
            └────┬────┘
                 ▼
            ┌─────────┐
            │ deploy  │              ← só em push na main
            └─────────┘
```

| Job | O que faz | Bloqueia o quê |
|-----|-----------|-----------------|
| **lint** | `ruff check` + `ruff format --check` em segundos | Build, test, deploy |
| **test** | pytest em **Python 3.11 e 3.12** simultaneamente (matrix) | Build, deploy |
| **build** | Sobe o servidor e bate em `/health` e `/add` | Deploy |
| **deploy** | Simula deploy em produção | — (último) |

---

## ⚙️ Setup pré-aula no GitHub (uma única vez)

Faça isso **uma vez**, antes da primeira apresentação:

1. **Crie um repositório público** no GitHub e faça push deste projeto:
   ```bash
   git init
   git add .
   git commit -m "chore: setup inicial do projeto demo"
   git branch -M main
   git remote add origin git@github.com:SEU-USUARIO/SEU-REPO.git
   git push -u origin main
   ```

2. **Confirme que o pipeline rodou**: abra a aba **Actions** do repo e
   espere o primeiro run da `main` ficar verde ✅.

3. **Habilite branch protection na `main`** — *etapa crítica para o
   Cenário 2 funcionar*:
   - Vá em **Settings → Branches → Add branch ruleset** (ou *Add rule*
     na interface antiga)
   - Branch name pattern: `main`
   - Marque ✅ **Require status checks to pass**
   - Em "Status checks that are required", adicione: `lint`, `test (3.11)`,
     `test (3.12)`, `build` (eles aparecem só depois do primeiro run)
   - Marque ✅ **Require a pull request before merging**
   - Salve

4. **(Opcional) Crie o environment `production`**:
   - Settings → Environments → New environment → `production`
   - Isso habilita a aba "Environments" no run do deploy (visualmente fica bonito)

---

## ✅ Checklist 5 minutos antes de começar

Ter tudo isso aberto antes da aula evita 2-3 minutos de fricção
constrangedora na frente da turma:

- [ ] Aba 1 do navegador → página principal do repo
- [ ] Aba 2 → aba **Actions**
- [ ] Aba 3 (plano B) → um run antigo verde
- [ ] Aba 4 (plano B) → um PR antigo com pipeline vermelho
- [ ] Terminal aberto na pasta, com `git status` limpo na `main`
- [ ] Editor aberto na pasta, fonte aumentada
- [ ] `git pull` recente
- [ ] Wifi confirmado
- [ ] Notificações silenciadas

---

# 🎬 ROTEIRO DOS 3 CENÁRIOS DO DEMO

> Tempo total: **12-15 minutos**.
> Cenário 1: ≈5-6 min · Cenário 2: ≈3-4 min · Cenário 3: ≈2-3 min.

## Quadro-resumo

| # | Cenário | Mensagem central | Slide que ele "prova" |
|---|---------|------------------|-----------------------|
| 1 | **Caminho feliz** | Push limpo → CI valida → CD entrega, sem ninguém clicar em nada | Slide 6 (Pipeline) |
| 2 | **PR com bug** | O CI segura a porteira: bug ruim **não chega em produção** | Slide 8 (Benefícios) |
| 3 | **Hotfix express** | Do `git push` até deploy em segundos = lead time de time elite | Slide 10 (DORA) |

---

## 🟢 CENÁRIO 1 — O caminho feliz (≈5-6 min)

> 💬 **Frase de abertura:** "Vou fazer uma alteração simples e mostrar o pipeline rodar do início ao fim, sem eu tocar em nada depois do push."

### Conceitos demonstrados

- ✓ Trigger por evento (push)
- ✓ Jobs paralelos (lint + test ao mesmo tempo)
- ✓ Matrix strategy (mesmo job em 2 versões do Python)
- ✓ Dependência entre jobs (`needs:`)
- ✓ Deploy condicional (`if:`)
- ✓ Status checks bloqueando merge

### Passo a passo

#### 1.1 Tour pelo projeto (~45s)

🖥️ **Ação:** No editor, mostre rapidamente os 4 arquivos-chave:
- `app/calculator.py`
- `app/main.py`
- `tests/test_calculator.py`
- `.github/workflows/ci-cd.yml` ⭐

🗣️ **Fala sugerida:**
> "Esse é o projeto. Calculadora simples em Python: lógica em `calculator.py`,
> API em `main.py`, testes em `tests/`. Mas a estrela é esse aqui:
> `.github/workflows/ci-cd.yml`. **Esse arquivo É o pipeline.**"

#### 1.2 Tour pelo `.yml` (~1 min)

🖥️ **Ação:** Abra o `.github/workflows/ci-cd.yml` no editor.

👀 **Aponte 3 coisas (sem entrar em detalhe):**
1. Bloco `on:` no topo → "**gatilho**"
2. Os 4 `jobs:` → "as **etapas**"
3. As linhas `needs:` e `if:` → "o que **encadeia** as etapas"

🗣️ **Fala sugerida:**
> "Arquivo grande, ideia simples. `on:` define quando rodar — todo push e
> todo PR. Aqui temos 4 jobs: `lint`, `test`, `build`, `deploy` — exatamente
> as etapas do slide do pipeline. E essa palavra `needs` aqui? Ela diz
> 'só rode esse job depois que os outros passaram'. **Vamos ver rodar.**"

🔗 **Conexão com a teoria:** Slide 6 (Pipeline) — o desenho dos slides
agora está em código.

#### 1.3 Criar branch + adicionar feature (~1 min)

🖥️ **Terminal:**
```bash
git checkout -b feat/endpoint-power
```

🖥️ **Editor:** Em `app/calculator.py`, adicione ao final:
```python
def power(a: float, b: float) -> float:
    """Eleva a à potência b."""
    return a ** b
```

🖥️ **Editor:** Em `tests/test_calculator.py`, adicione ao final:
```python
class TestPower:
    def test_power_basico(self):
        assert calculator.power(2, 10) == 1024

    def test_power_zero(self):
        assert calculator.power(5, 0) == 1
```

🗣️ **Fala (enquanto digita):**
> "Branch nova, função nova, **e o teste junto**. Sem teste, o CI não
> tem como te dar feedback de nada."

#### 1.4 Commit + push (~30s)

🖥️ **Terminal:**
```bash
git add .
git commit -m "feat: adiciona função power"
git push origin feat/endpoint-power
```

🗣️ **Fala:**
> "Push. **A partir desse instante**, o GitHub Actions já está executando
> nosso pipeline. Vamos ver."

#### 1.5 Acompanhar o pipeline (~1.5 min)

🖥️ **Ação:** Aba 2 (Actions) → clique no run que acabou de aparecer.

👀 **Aponte:**
1. Bolinha amarela ⚪ ao lado do run (= "rodando")
2. Barra lateral com os 4 jobs
3. Clique em `test` → mostre as 2 sub-execuções (Python 3.11 e 3.12)

🗣️ **Fala:**
> "Bolinha amarela = rodando. Aqui na lateral, os 4 jobs. Reparem que
> `lint` e `test` estão **rodando ao mesmo tempo**. Em paralelo, não em
> série. Isso é o que torna o pipeline rápido.
>
> E olha esse detalhe: o `test` rodou em **Python 3.11 E 3.12**, ao mesmo
> tempo. É a tal **matrix**: o mesmo job, várias versões. Garante que
> não quebra em ambiente nenhum."

🔗 **Conexão:** Slide 9 (Boas práticas) — "pipeline rápido < 10 min".

#### 1.6 Pipeline verde + abrir PR (~1 min)

🖥️ **Ação:** Espere ficar tudo verde ✅ (30-60s).

🖥️ **Ação:** Aba 1 → banner amarelo "Compare & pull request" → clique →
título "feat: adiciona endpoint power" → **Create pull request**.

👀 **Na página do PR, role até o final e aponte:**
- Bloco verde **"All checks have passed"**
- Botão **Merge pull request** habilitado (verde)

🗣️ **Fala:**
> "PR aberto. Olhem aqui embaixo: '**All checks have passed**'. Lint, test,
> build — tudo verde. Por isso o botão de merge está liberado. Se algum
> check tivesse falhado, ele estaria **bloqueado**."

#### 1.7 Merge → deploy automático (~45s)

🖥️ **Ação:** **Merge pull request** → **Confirm merge** → **Delete branch**.

🖥️ **Ação:** Aba 2 (Actions) → vai aparecer um novo run, disparado pelo
push na `main`.

👀 **Aponte:**
1. Novo run rodando
2. **Agora o job `deploy` aparece** (no PR não aparecia!)
3. Clique no `deploy` → mostre os logs:
   ```
   🚀 Iniciando deploy para PRODUÇÃO...
   ✅ Deploy concluído com sucesso!
   ```

🗣️ **Fala:**
> "O merge na main disparou um novo pipeline. E dessa vez o `deploy` está
> rodando — no PR ele não rodou. Por quê? Porque na linha `if:` do
> workflow eu defini 'só faça deploy se for push direto na main'.
>
> [aguarda ~10s]
>
> Pronto. **Sem clicar em nada depois do merge.** O CD aconteceu sozinho."

🔗 **Conexão:** Slide 5 (CD). Mencione:
> "Isso aqui é Continuous **Deployment**. Se eu quisesse Continuous
> **Delivery** — com humano aprovando — bastaria adicionar um campo
> `environment: production` exigindo reviewer. **Uma linha de YAML
> separa as duas coisas.**"

### Fechamento do Cenário 1

🗣️
> "Esse é o fluxo normal de um time CI/CD: programa, push, pipeline cuida
> do resto. **Mas e se algo der errado?** Próximo cenário."

---

## 🔴 CENÁRIO 2 — O CI segura o bug (≈3-4 min)

> 💬 **Frase de abertura:** "Imagina que estou cansado, sexta à tarde, e cometi um erro bobo. O que acontece?"

### Conceitos demonstrados

- ✓ Pipeline vermelho ❌
- ✓ Logs de teste com saída exata do erro
- ✓ **Branch protection bloqueando o merge**
- ✓ Anti-padrão evitado: "merge mesmo com teste quebrado"

### Passo a passo

#### 2.1 Nova branch + bug intencional (~1 min)

🖥️ **Terminal:**
```bash
git checkout main
git pull
git checkout -b fix/divisao-com-bug
```

🖥️ **Editor:** Em `app/calculator.py`, **introduza um bug** na função `divide`:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a + b   # ← BUG: deveria ser a / b
```

🗣️
> "Trocar o operador da divisão por uma soma é o tipo de erro que a gente
> faz cansado. Em time sem CI, isso poderia ir pra produção. Vamos ver
> com CI."

#### 2.2 Commit + push + abrir PR (~30s)

🖥️ **Terminal:**
```bash
git add .
git commit -m "refactor: simplifica divide"
git push origin fix/divisao-com-bug
```

🖥️ **Ação:** Abra o PR no GitHub.

#### 2.3 Pipeline vermelho (~1 min)

🖥️ **Ação:** Aba 2 (Actions) → acompanhar. Em ~30s o `test` fica vermelho ❌.

🗣️
> "E lá vem... **vermelho**. O CI pegou. Vamos ver o que ele encontrou."

🖥️ **Ação:** Clique no job `test` → expanda "Rodar pytest com cobertura".

👀 **Mostre os logs:**
```
FAILED tests/test_calculator.py::TestDivide::test_divisao_exata
    AssertionError: assert 12 == 5
     +  where 12 = divide(10, 2)
```

🗣️
> "Olhem que beleza: 'chamei `divide(10, 2)`, esperava 5, recebi 12'.
> **Em 30 segundos**, o CI me disse exatamente onde está o erro, com qual
> entrada. Isso é **feedback rápido**."

🔗 **Conexão:** Slide 4 (CI) — "se quebrou, descubro em minutos, não em
semanas".

#### 2.4 Merge bloqueado (~45s)

🖥️ **Ação:** Volte pro PR.

👀 **Aponte:**
1. X vermelho ❌ ao lado de `test`
2. **"Required statuses must pass before merging"**
3. Botão de merge **cinza, desabilitado**

🗣️
> "O GitHub está dizendo: 'esse PR não pode ser mergeado'. Mesmo eu sendo
> o dono do repo, **não consigo subir esse código pra main**. Por quê?
> Porque eu mesmo configurei a regra. **Esse bug nunca vai chegar em
> produção.**"

### Fechamento do Cenário 2

🗣️
> "Se esse bug fosse parar em produção: cliente reclama, time entra em
> pânico, alguém abre incidente. O CI evitou tudo isso. **Esse é o valor
> concreto do CI.** Lembram do slide '200x mais rápido, bugs corrigidos
> em horas'? É exatamente porque o CI pega 90% das besteiras antes de
> virarem incidente."

🔗 **Conexão:** Slide 8 (Benefícios) — fecha alegação numérica com prova.

---

## ⚡ CENÁRIO 3 — Hotfix express (≈2-3 min)

> 💬 **Frase de abertura:** "Agora vou consertar e cronometrar quanto tempo até produção."

### Conceitos demonstrados

- ✓ **Lead time** (DORA)
- ✓ Iteração rápida no mesmo PR
- ✓ Mesmo PR atualiza com novo push

### Passo a passo

#### 3.1 Corrigir o bug (~30s)

🖥️ **Editor:** Em `app/calculator.py`, corrija:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida")
    return a / b   # ← corrigido
```

#### 3.2 Commit + push — INICIE O CRONÔMETRO (~15s)

🗣️
> "Vou marcar o tempo agora. **Cronômetro ligado.** Quanto tempo até chegar
> em produção?"

🖥️ **Terminal:**
```bash
git add .
git commit -m "fix: corrige operador da divisão"
git push
```

#### 3.3 Pipeline verde no MESMO PR (~1 min)

🖥️ **Ação:** Volte pro PR já aberto. O GitHub detecta o novo commit e roda
o pipeline.

🗣️
> "É **o mesmo PR**. Não precisei abrir outro. O GitHub viu novo commit,
> disparou novo run."

🖥️ **Ação:** Aguarde ficar verde ✅ (~30-45s).

#### 3.4 Merge + deploy + cronômetro parado (~45s)

🖥️ **Ação:** **Merge pull request** → **Confirm merge**.

🖥️ **Ação:** Aba 2 (Actions). Run da `main` aparece, `deploy` rodando.

👀 **Quando o deploy terminar, olhe a hora.**

🗣️
> "**Pare o cronômetro.** Quanto deu? Uns 2-3 minutos? **Esse é o lead
> time do nosso pipeline.** Lembram da tabela DORA? 'Time elite: menos
> de 1 hora.' Acabamos em minutos. **Isso é CD funcionando.**"

🔗 **Conexão:** Slide 10 (DORA) — eles acabaram de ver lead time, na prática.

### Fechamento da Demo

🗣️
> "Recapitulando o que vocês acabaram de ver:
> - **Cenário 1**: push → CI valida → CD entrega, sem clicar em nada.
> - **Cenário 2**: bug? CI segura. Não chega em produção.
> - **Cenário 3**: hotfix em minutos, do commit ao deploy.
>
> Tudo isso a partir de um arquivo YAML de cem linhas. **Isso é CI/CD.**"

---

## 🛟 Plano B — Quando algo dá errado

| Problema | Reação |
|---|---|
| **Wifi caiu** | Use as Abas 3 e 4 (run antigo verde + PR antigo vermelho). Conte a história ao invés de fazê-la rodar. |
| **GitHub Actions lento** | Aproveite a espera pra fazer o **tour pelo `.yml`** explicando os blocos. Quando termina o tour, geralmente o pipeline já acabou. |
| **Erro inesperado** | Mostre o log, leia em voz alta. Se for rápido, conserte ao vivo. Senão, **culpe o bug** e vá pro próximo cenário. Demos imperfeitos ensinam mais. |
| **Esqueci branch protection** | No Cenário 2, mostre o X vermelho e diga: "se eu tivesse configurado branch protection, o botão estaria cinza". |
| **Faltou tempo** | Pule o Cenário 2. Cenário 1 + 3 ainda contam a história principal. |

---

## 🔗 Mapa rápido teoria ↔ demo

| Conceito do slide | Onde aparece no demo |
|---|---|
| **CI** (slide 4) | Cenário 1.5 — pipeline rodando após push |
| **Continuous Deployment** (slide 5) | Cenário 1.7 — deploy automático após merge |
| **Pipeline** (slide 6) | Cenário 1.5 — diagrama dos 4 jobs |
| **Lint, Test, Build, Deploy** (slide 7) | Estrutura dos 4 jobs do `.yml` |
| **Pipeline rápido** (slide 9) | Cenário 1.5 — paralelismo + matrix |
| **Testes confiáveis** (slide 9) | Cenário 2 — pytest pegando o bug |
| **Lead time** (slide 10) | Cenário 3 — cronômetro do hotfix |

---

## 📌 Conceitos-chave que aparecem no `.yml`

Use esses ganchos quando estiver fazendo o tour pelo arquivo:

| Linha | Conceito | O que dizer |
|---|---|---|
| `on: push, pull_request` | **Trigger** | "O pipeline reage a eventos do Git" |
| `jobs: lint, test, ...` | **Jobs paralelos** | "Cada job roda numa máquina virtual isolada" |
| `runs-on: ubuntu-latest` | **Runner** | "GitHub te dá um Linux limpo de graça por 2000 min/mês" |
| `uses: actions/checkout@v4` | **Actions reutilizáveis** | "Marketplace tem milhares — não reinventa a roda" |
| `cache: pip` | **Cache** | "Evita reinstalar deps a cada run, deixa o pipeline rápido" |
| `strategy.matrix` | **Matrix** | "Roda o mesmo job em várias versões/SOs ao mesmo tempo" |
| `needs: [lint, test]` | **Dependência** | "Define a ordem: build só depois de lint e test" |
| `if: github.ref == 'refs/heads/main'` | **Condicional** | "Deploy só na main, nunca em PR" |
| `environment: production` | **Environment** | "Aprovação manual + secrets isolados — fintechs fazem assim" |

---

## 🔗 Links úteis

- [DORA — State of DevOps Report](https://dora.dev/)
- [Continuous Delivery (Humble & Farley)](https://continuousdelivery.com/)
- [GitHub Actions — Documentação oficial](https://docs.github.com/en/actions)
- [The Twelve-Factor App](https://12factor.net/)
