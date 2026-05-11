git checkout -b feat/endpoint-power
def power(a: float, b: float) -> float:
git add .
git commit -m "feat: adiciona funcao power"
git checkout main
git pull
git checkout -b fix/divisao-com-bug
def divide(a: float, b: float) -> float:
git add .
git commit -m "refactor: simplifica divide"
def divide(a: float, b: float) -> float:
git add .
git commit -m "fix: corrige operador da divisao"
o pipeline.
# Calculadora API - Projeto-demo de CI/CD

Projeto-exemplo para a mini-aula sobre **Integracao Continua (CI)** e
**Entrega/Implantacao Continua (CD)** usando **GitHub Actions**.

---

## Estrutura

```
calculadora-exemplo-cicd-manutencao-de-software/
├── app/
│   ├── calculator.py          # Logica de negocio (testavel isoladamente)
│   └── main.py                # API FastAPI
├── tests/
│   ├── test_calculator.py     # Testes unitarios puros
│   └── test_main.py           # Testes de integracao (HTTP)
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # O coracao do demo: o pipeline
├── pyproject.toml             # Config do ruff + pytest
└── requirements.txt
```

A separacao **logica de negocio (`calculator.py`) <-> camada HTTP (`main.py`)**
e proposital: permite testes unitarios rapidissimos e mostra uma boa
pratica de arquitetura. Vale mencionar isso na hora.

---

## Setup local

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Validar tudo (mesmo que o pipeline vai rodar)
ruff check app tests
ruff format --check app tests
pytest

# 4. Subir o servidor pra confirmar que sobe
uvicorn app.main:app --reload
# Acesse: http://localhost:8000/docs
```

Se passou tudo localmente, vai passar no GitHub. **Nunca de push sem
rodar local antes** - isso e a regra mais basica de quem usa CI/CD bem.

---

## O Pipeline - visao geral

O arquivo `.github/workflows/ci-cd.yml` define **4 jobs**:

```
   +---------+    +---------+
   |  lint   |    |  test   |   <- rodam em paralelo (rapido!)
   +----+----+    +----+----+
       \----+----/
           v
       +---------+
       |  build  |              <- so roda se lint+test passaram
       +----+----+
           v
       +---------+
       | deploy  |              <- so em push na main
       +---------+
```

| Job | O que faz | Bloqueia o que |
|-----|-----------|-----------------|
| **lint** | `ruff check` + `ruff format --check` em segundos | Build, test, deploy |
| **test** | pytest em **Python 3.11 e 3.12** simultaneamente (matrix) | Build, deploy |
| **build** | Sobe o servidor e bate em `/health` e `/add` | Deploy |
| **deploy** | Simula deploy em producao | - (ultimo) |

---

## Setup pre-aula no GitHub (uma unica vez)

Faca isso **uma vez**, antes da primeira apresentacao:

1. **Crie um repositorio publico** no GitHub e faca push deste projeto:
   ```bash
   git init
   git add .
   git commit -m "chore: setup inicial do projeto demo"
   git branch -M main
   git remote add origin git@github.com:SEU-USUARIO/SEU-REPO.git
   git push -u origin main
   ```

2. **Confirme que o pipeline rodou**: abra a aba **Actions** do repo e
   espere o primeiro run da `main` ficar verde.

3. **Habilite branch protection na `main`** - *etapa critica para o
   Cenario 2 funcionar*:
   - Va em **Settings -> Branches -> Add branch ruleset** (ou *Add rule*
     na interface antiga)
   - Branch name pattern: `main`
   - Marque **Require status checks to pass**
   - Em "Status checks that are required", adicione: `lint`, `test (3.11)`,
     `test (3.12)`, `build` (eles aparecem so depois do primeiro run)
   - Marque **Require a pull request before merging**
   - Salve

4. **(Opcional) Crie o environment `production`**:
   - Settings -> Environments -> New environment -> `production`
   - Isso habilita a aba "Environments" no run do deploy (visualmente fica bonito)

---

## Checklist 5 minutos antes de comecar

Ter tudo isso aberto antes da aula evita 2-3 minutos de friccao
constrangedora na frente da turma:

- [ ] Aba 1 do navegador -> pagina principal do repo
- [ ] Aba 2 -> aba **Actions**
- [ ] Aba 3 (plano B) -> um run antigo verde
- [ ] Aba 4 (plano B) -> um PR antigo com pipeline vermelho
- [ ] Terminal aberto na pasta, com `git status` limpo na `main`
- [ ] Editor aberto na pasta, fonte aumentada
- [ ] `git pull` recente
- [ ] Wifi confirmado
- [ ] Notificacoes silenciadas

---

# ROTEIRO DOS 3 CENARIOS DO DEMO

> Tempo total: **12-15 minutos**.
> Cenario 1: ~5-6 min - Cenario 2: ~3-4 min - Cenario 3: ~2-3 min.

## Quadro-resumo

| # | Cenario | Mensagem central | Slide que ele "prova" |
|---|---------|------------------|-----------------------|
| 1 | **Caminho feliz** | Push limpo -> CI valida -> CD entrega, sem ninguem clicar em nada | Slide 6 (Pipeline) |
| 2 | **PR com bug** | O CI segura a porteira: bug ruim **nao chega em producao** | Slide 8 (Beneficios) |
| 3 | **Hotfix express** | Do `git push` ate deploy em segundos = lead time de time elite | Slide 10 (DORA) |

---

## CENARIO 1 - O caminho feliz (~5-6 min)

> **Frase de abertura:** "Vou fazer uma alteracao simples e mostrar o pipeline rodar do inicio ao fim, sem eu tocar em nada depois do push."

### Conceitos demonstrados

- Trigger por evento (push)
- Jobs paralelos (lint + test ao mesmo tempo)
- Matrix strategy (mesmo job em 2 versoes do Python)
- Dependencia entre jobs (`needs:`)
- Deploy condicional (`if:`)
- Status checks bloqueando merge

### Passo a passo

#### 1.1 Tour pelo projeto (~45s)

**Acao:** No editor, mostre rapidamente os 4 arquivos-chave:
- `app/calculator.py`
- `app/main.py`
- `tests/test_calculator.py`
- `.github/workflows/ci-cd.yml`

**Fala sugerida:**
> "Esse e o projeto. Calculadora simples em Python: logica em `calculator.py`,
> API em `main.py`, testes em `tests/`. Mas a estrela e esse aqui:
> `.github/workflows/ci-cd.yml`. **Esse arquivo E o pipeline.**"

#### 1.2 Tour pelo `.yml` (~1 min)

**Acao:** Abra o `.github/workflows/ci-cd.yml` no editor.

**Aponte 3 coisas (sem entrar em detalhe):**
1. Bloco `on:` no topo -> "**gatilho**"
2. Os 4 `jobs:` -> "as **etapas**"
3. As linhas `needs:` e `if:` -> "o que **encadeia** as etapas"

**Fala sugerida:**
> "Arquivo grande, ideia simples. `on:` define quando rodar - todo push e
> todo PR. Aqui temos 4 jobs: `lint`, `test`, `build`, `deploy` - exatamente
> as etapas do slide do pipeline. E essa palavra `needs` aqui? Ela diz
> 'so rode esse job depois que os outros passaram'. **Vamos ver rodar.**"

**Conexao com a teoria:** Slide 6 (Pipeline) - o desenho dos slides
agora esta em codigo.

#### 1.3 Criar branch + adicionar feature (~1 min)

**Terminal:**
```bash
git checkout -b feat/endpoint-power
```

**Editor:** Em `app/calculator.py`, adicione ao final:
```python
def power(a: float, b: float) -> float:
    """Eleva a a potencia b."""
    return a ** b
```

**Editor:** Em `tests/test_calculator.py`, adicione ao final:
```python
class TestPower:
    def test_power_basico(self):
        assert calculator.power(2, 10) == 1024

    def test_power_zero(self):
        assert calculator.power(5, 0) == 1
```

**Fala (enquanto digita):**
> "Branch nova, funcao nova, **e o teste junto**. Sem teste, o CI nao
> tem como te dar feedback de nada."

#### 1.4 Commit + push (~30s)

**Terminal:**
```bash
git add .
git commit -m "feat: adiciona funcao power"
git push origin feat/endpoint-power
```

**Fala:**
> "Push. **A partir desse instante**, o GitHub Actions ja esta executando
> nosso pipeline. Vamos ver."

#### 1.5 Acompanhar o pipeline (~1.5 min)

**Acao:** Aba 2 (Actions) -> clique no run que acabou de aparecer.

**Aponte:**
1. Bolinha amarela ao lado do run (= "rodando")
2. Barra lateral com os 4 jobs
3. Clique em `test` -> mostre as 2 sub-execucoes (Python 3.11 e 3.12)

**Fala:**
> "Bolinha amarela = rodando. Aqui na lateral, os 4 jobs. Reparem que
> `lint` e `test` estao **rodando ao mesmo tempo**. Em paralelo, nao em
> serie. Isso e o que torna o pipeline rapido.
>
> E olha esse detalhe: o `test` rodou em **Python 3.11 E 3.12**, ao mesmo
> tempo. E a tal **matrix**: o mesmo job, varias versoes. Garante que
> nao quebra em ambiente nenhum."

**Conexao:** Slide 9 (Boas praticas) - "pipeline rapido < 10 min".

#### 1.6 Pipeline verde + abrir PR (~1 min)

**Acao:** Espere ficar tudo verde (30-60s).

**Acao:** Aba 1 -> banner amarelo "Compare & pull request" -> clique ->
titulo "feat: adiciona endpoint power" -> **Create pull request**.

**Na pagina do PR, role ate o final e aponte:**
- Bloco verde **"All checks have passed"**
- Botao **Merge pull request** habilitado (verde)

**Fala:**
> "PR aberto. Olhem aqui embaixo: '**All checks have passed**'. Lint, test,
> build - tudo verde. Por isso o botao de merge esta liberado. Se algum
> check tivesse falhado, ele estaria **bloqueado**."

#### 1.7 Merge -> deploy automatico (~45s)

**Acao:** **Merge pull request** -> **Confirm merge** -> **Delete branch**.

**Acao:** Aba 2 (Actions) -> vai aparecer um novo run, disparado pelo
push na `main`.

**Aponte:**
1. Novo run rodando
2. **Agora o job `deploy` aparece** (no PR nao aparecia!)
3. Clique no `deploy` -> mostre os logs:
   ```
   Iniciando deploy para PRODUCAO...
   Deploy concluido com sucesso!
   ```

**Fala:**
> "O merge na main disparou um novo pipeline. E dessa vez o `deploy` esta
> rodando - no PR ele nao rodou. Por que? Porque na linha `if:` do
> workflow eu defini 'so faca deploy se for push direto na main'.
>
> [aguarda ~10s]
>
> Pronto. **Sem clicar em nada depois do merge.** O CD aconteceu sozinho."

**Conexao:** Slide 5 (CD). Mencione:
> "Isso aqui e Continuous **Deployment**. Se eu quisesse Continuous
> **Delivery** - com humano aprovando - bastaria adicionar um campo
> `environment: production` exigindo reviewer. **Uma linha de YAML
> separa as duas coisas.**"

### Fechamento do Cenario 1

> "Esse e o fluxo normal de um time CI/CD: programa, push, pipeline cuida
> do resto. **Mas e se algo der errado?** Proximo cenario."

---

## CENARIO 2 - O CI segura o bug (~3-4 min)

> **Frase de abertura:** "Imagina que estou cansado, sexta a tarde, e cometi um erro bobo. O que acontece?"

### Conceitos demonstrados

- Pipeline vermelho
- Logs de teste com saida exata do erro
- **Branch protection bloqueando o merge**
- Anti-padrao evitado: "merge mesmo com teste quebrado"

### Passo a passo

#### 2.1 Nova branch + bug intencional (~1 min)

**Terminal:**
```bash
git checkout main
git pull
git checkout -b fix/divisao-com-bug
```

**Editor:** Em `app/calculator.py`, **introduza um bug** na funcao `divide`:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisao por zero nao e permitida")
    return a + b   # BUG: deveria ser a / b
```

> "Trocar o operador da divisao por uma soma e o tipo de erro que a gente
> faz cansado. Em time sem CI, isso poderia ir pra producao. Vamos ver
> com CI."

#### 2.2 Commit + push + abrir PR (~30s)

**Terminal:**
```bash
git add .
git commit -m "refactor: simplifica divide"
git push origin fix/divisao-com-bug
```

**Acao:** Abra o PR no GitHub.

#### 2.3 Pipeline vermelho (~1 min)

**Acao:** Aba 2 (Actions) -> acompanhar. Em ~30s o `test` fica vermelho.

> "E la vem... **vermelho**. O CI pegou. Vamos ver o que ele encontrou."

**Acao:** Clique no job `test` -> expanda "Rodar pytest com cobertura".

**Mostre os logs:**
```
FAILED tests/test_calculator.py::TestDivide::test_divisao_exata
    AssertionError: assert 12 == 5
     +  where 12 = divide(10, 2)
```

> "Olhem que beleza: 'chamei `divide(10, 2)`, esperava 5, recebi 12'.
> **Em 30 segundos**, o CI me disse exatamente onde esta o erro, com qual
> entrada. Isso e **feedback rapido**."

**Conexao:** Slide 4 (CI) - "se quebrou, descubro em minutos, nao em
semanas".

#### 2.4 Merge bloqueado (~45s)

**Acao:** Volte pro PR.

**Aponte:**
1. X vermelho ao lado de `test`
2. **"Required statuses must pass before merging"**
3. Botao de merge **cinza, desabilitado**

> "O GitHub esta dizendo: 'esse PR nao pode ser mergeado'. Mesmo eu sendo
> o dono do repo, **nao consigo subir esse codigo pra main**. Por que?
> Porque eu mesmo configurei a regra. **Esse bug nunca vai chegar em
> producao.**"

### Fechamento do Cenario 2

> "Se esse bug fosse parar em producao: cliente reclama, time entra em
> panico, alguem abre incidente. O CI evitou tudo isso. **Esse e o valor
> concreto do CI.** Lembram do slide '200x mais rapido, bugs corrigidos
> em horas'? E exatamente porque o CI pega 90% das besteiras antes de
> virarem incidente."

**Conexao:** Slide 8 (Beneficios) - fecha alegacao numerica com prova.

---

## CENARIO 3 - Hotfix express (~2-3 min)

> **Frase de abertura:** "Agora vou consertar e cronometrar quanto tempo ate producao."

### Conceitos demonstrados

- **Lead time** (DORA)
- Iteracao rapida no mesmo PR
- Mesmo PR atualiza com novo push

### Passo a passo

#### 3.1 Corrigir o bug (~30s)

**Editor:** Em `app/calculator.py`, corrija:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisao por zero nao e permitida")
    return a / b   # corrigido
```

#### 3.2 Commit + push - INICIE O CRONOMETRO (~15s)

> "Vou marcar o tempo agora. **Cronometro ligado.** Quanto tempo ate chegar
> em producao?"

**Terminal:**
```bash
git add .
git commit -m "fix: corrige operador da divisao"
git push
```

#### 3.3 Pipeline verde no MESMO PR (~1 min)

**Acao:** Volte pro PR ja aberto. O GitHub detecta o novo commit e roda


> "E **o mesmo PR**. Nao precisei abrir outro. O GitHub viu novo commit,
> disparou novo run."

**Acao:** Aguarde ficar verde (30-45s).

#### 3.4 Merge + deploy + cronometro parado (~45s)

**Acao:** **Merge pull request** -> **Confirm merge**.

**Acao:** Aba 2 (Actions). Run da `main` aparece, `deploy` rodando.

**Quando o deploy terminar, olhe a hora.**

> "**Pare o cronometro.** Quanto deu? Uns 2-3 minutos? **Esse e o lead
> time do nosso pipeline.** Lembram da tabela DORA? 'Time elite: menos
> de 1 hora.' Acabamos em minutos. **Isso e CD funcionando.**"

**Conexao:** Slide 10 (DORA) - eles acabaram de ver lead time, na pratica.

### Fechamento da Demo

> "Recapitulando o que voces acabaram de ver:
> - **Cenario 1**: push -> CI valida -> CD entrega, sem clicar em nada.
> - **Cenario 2**: bug? CI segura. Nao chega em producao.
> - **Cenario 3**: hotfix em minutos, do commit ao deploy.
>
> Tudo isso a partir de um arquivo YAML de cem linhas. **Isso e CI/CD.**"

---

## Plano B - Quando algo da errado

| Problema | Reacao |
|---|---|
| **Wifi caiu** | Use as Abas 3 e 4 (run antigo verde + PR antigo vermelho). Conte a historia ao inves de faze-la rodar. |
| **GitHub Actions lento** | Aproveite a espera pra fazer o **tour pelo `.yml`** explicando os blocos. Quando termina o tour, geralmente o pipeline ja acabou. |
| **Erro inesperado** | Mostre o log, leia em voz alta. Se for rapido, conserte ao vivo. Senao, **culpe o bug** e va pro proximo cenario. Demos imperfeitos ensinam mais. |
| **Esqueci branch protection** | No Cenario 2, mostre o X vermelho e diga: "se eu tivesse configurado branch protection, o botao estaria cinza". |
| **Faltou tempo** | Pule o Cenario 2. Cenario 1 + 3 ainda contam a historia principal. |

---

## Mapa rapido teoria <-> demo

| Conceito do slide | Onde aparece no demo |
|---|---|
| **CI** (slide 4) | Cenario 1.5 - pipeline rodando apos push |
| **Continuous Deployment** (slide 5) | Cenario 1.7 - deploy automatico apos merge |
| **Pipeline** (slide 6) | Cenario 1.5 - diagrama dos 4 jobs |
| **Lint, Test, Build, Deploy** (slide 7) | Estrutura dos 4 jobs do `.yml` |
| **Pipeline rapido** (slide 9) | Cenario 1.5 - paralelismo + matrix |
| **Testes confiaveis** (slide 9) | Cenario 2 - pytest pegando o bug |
| **Lead time** (slide 10) | Cenario 3 - cronometro do hotfix |

---

## Conceitos-chave que aparecem no `.yml`

Use esses ganchos quando estiver fazendo o tour pelo arquivo:

| Linha | Conceito | O que dizer |
|---|---|---|
| `on: push, pull_request` | **Trigger** | "O pipeline reage a eventos do Git" |
| `jobs: lint, test, ...` | **Jobs paralelos** | "Cada job roda numa maquina virtual isolada" |
| `runs-on: ubuntu-latest` | **Runner** | "GitHub te da um Linux limpo de graca por 2000 min/mes" |
| `uses: actions/checkout@v4` | **Actions reutilizaveis** | "Marketplace tem milhares - nao reinventa a roda" |
| `cache: pip` | **Cache** | "Evita reinstalar deps a cada run, deixa o pipeline rapido" |
| `strategy.matrix` | **Matrix** | "Roda o mesmo job em varias versoes/SOs ao mesmo tempo" |
| `needs: [lint, test]` | **Dependencia** | "Define a ordem: build so depois de lint e test" |
| `if: github.ref == 'refs/heads/main'` | **Condicional** | "Deploy so na main, nunca em PR" |
| `environment: production` | **Environment** | "Aprovacao manual + secrets isolados - fintechs fazem assim" |

---

## Links uteis

- [DORA - State of DevOps Report](https://dora.dev/)
- [Continuous Delivery (Humble & Farley)](https://continuousdelivery.com/)
- [GitHub Actions - Documentacao oficial](https://docs.github.com/en/actions)
- [The Twelve-Factor App](https://12factor.net/)
