<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>kauansstz Terminal Profile</title>
  <style>
    * {
      box-sizing: border-box;
    }
    body {
      background-color: #000000;
      color: #c9d1d9;
      font-family: 'Courier New', Courier, monospace;
      padding: 20px;
      margin: 0;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    #terminal {
      background: #000000;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 20px;
      width: 100%;
      max-width: 850px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.9);
      display: flex;
      flex-direction: column;
    }
    #output-area {
      background: #000000;
      max-height: 520px;
      overflow-y: auto;
      margin-bottom: 12px;
    }
    .text-green { color: #3fb950; }
    .text-yellow { color: #d29922; }
    .text-red { color: #f85149; }
    .text-white { color: #f0f6fc; }
    .text-cyan { color: #38bdf8; }
    
    pre {
      margin: 0;
      font-family: inherit;
      white-space: pre-wrap;
      word-break: break-all;
    }
    .output-line {
      margin-bottom: 4px;
      white-space: pre-wrap;
      line-height: 1.4;
    }
    
    .input-container {
      display: flex;
      align-items: center;
      background: #0d1117;
      padding: 10px 14px;
      border-radius: 6px;
      border: 1px solid #30363d;
      cursor: text;
    }
    .prompt {
      color: #3fb950;
      font-weight: bold;
      margin-right: 8px;
      white-space: nowrap;
      user-select: none;
    }
    
    #commandInput {
      background: transparent;
      border: none;
      outline: none;
      color: #ffffff;
      font-family: inherit;
      font-size: 1.05rem;
      width: 100%;
      flex: 1;
      caret-color: #ffffff;
    }

    .btn-send {
      background: #238636;
      color: #ffffff;
      border: 1px solid #2ea043;
      padding: 8px 16px;
      font-family: inherit;
      font-size: 0.9rem;
      font-weight: bold;
      border-radius: 4px;
      cursor: pointer;
      margin-left: 10px;
      transition: background 0.2s;
      user-select: none;
    }
    .btn-send:hover {
      background: #2ea043;
    }
    .btn-send:active {
      transform: scale(0.98);
    }
  </style>
</head>
<body>

<div id="terminal">
  <!-- Área do Terminal onde as saídas e listas são renderizadas -->
  <div id="output-area">
    <div id="ascii-banner">
      <pre class="text-green">
  _  __    _   _   _   _   _   _  ____  ____  _____ ____  
 | |/ /   / \  | | | | / \ | \ | |/ ___||  _ \|_   _|_  /  
 | ' /   / _ \ | | | |/ _ \|  \| |\___ \| |_) | | |   / /   
 | . \  / ___ \| |_| / ___ \ |\  | ___) |  _ &lt;  | |  / /_   
 |_|\_\/_/   \_\___//_/   \_\_| \_|____/|_| \_\ |_| /___|  
      </pre>
    </div>
    <!-- A lista primaria e o historico de comandos aparecem exatamente aqui -->
    <div id="history"></div>
  </div>

  <!-- Campo de Entrada posicionado logo abaixo das listas -->
  <div class="input-container" id="inputContainer">
    <span class="prompt">kauan@dev-environment:~$</span>
    <input type="text" id="commandInput" autofocus autocomplete="off" spellcheck="false" placeholder="Digite o número da opção..." />
    <button type="button" id="btnEnter" class="btn-send">[ ENTER ]</button>
  </div>
</div>

<script>
  let state = 'MAIN_MENU';

  const projects = {
    '1': {
      name: 'projex-core-service',
      readme: '# Projex Core Service\n\nSistema backend em Java e Spring Boot para gerenciamento de perfis e quizzes interativos.\n\n- Autenticação JWT\n- Banco de dados relacional\n- Conteinerização via Docker'
    },
    '2': {
      name: 'rust-high-perf-api',
      readme: '# Rust High Perf API\n\nAPI de altíssima performance em Rust focada em baixo consumo de memória e baixa latência.'
    },
    '3': {
      name: 'legacy-data-migrator',
      readme: null
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('commandInput');
    const history = document.getElementById('history');
    const outputArea = document.getElementById('output-area');
    const btnEnter = document.getElementById('btnEnter');

    function focusInput() {
      input.focus();
    }

    function printLine(text, className = 'text-white') {
      const div = document.createElement('div');
      div.className = `output-line ${className}`;
      div.textContent = text;
      history.appendChild(div);
      outputArea.scrollTop = outputArea.scrollHeight;
    }

    // Lista Primária (Lista do Menu Principal) - Estilo `dir`/`ls`
    function showPrimaryList() {
      state = 'MAIN_MENU';
      printLine("kauan@dev-environment:~$ dir ./menu_opcoes", "text-green");
      printLine("--------------------------------------------------------", "text-yellow");
      printLine("  1 - Saber quem é o Kauan", "text-cyan");
      printLine("  2 - Listar as tecnologias dominantes", "text-cyan");
      printLine("  3 - Listar repositórios", "text-cyan");
      printLine("--------------------------------------------------------", "text-yellow");
    }

    // Segunda Lista (Lista dos Repositórios) - Chamada ao escolher a opção 3
    function showSecondaryList() {
      state = 'PROJECTS_MENU';
      printLine("kauan@dev-environment:~$ dir ./repositorios", "text-green");
      printLine("--------------------------------------------------------", "text-yellow");
      printLine("  1 - projex-core-service", "text-cyan");
      printLine("  2 - rust-high-perf-api", "text-cyan");
      printLine("  3 - legacy-data-migrator", "text-cyan");
      printLine("  0 - Voltar ao menu principal", "text-cyan");
      printLine("--------------------------------------------------------", "text-yellow");
      printLine("Digite o número do repositório para ler o README:", "text-white");
    }

    function handleCommand(cmd) {
      const cleanCmd = cmd.trim();
      if (!cleanCmd) return;

      printLine(`kauan@dev-environment:~$ ${cleanCmd}`, 'text-green');

      if (state === 'MAIN_MENU') {
        switch(cleanCmd) {
          case '1':
            printLine("\n--- [ 1 - SOBRE KAUAN ] ---", "text-yellow");
            printLine("• Nome Completo : Kauan dos Santos de Souza");
            printLine("• Idade         : 22 anos");
            printLine("• Experiência   : Programando desde os 18 anos");
            printLine("• Perfil        : Desenvolvedor Backend / Full-Stack focado em arquitetura e microsserviços.\n");
            showPrimaryList();
            break;

          case '2':
            printLine("\n--- [ 2 - TECNOLOGIAS DOMINANTES ] ---", "text-yellow");
            printLine("• Linguagens     : Rust, Python, Java");
            printLine("• Frameworks     : Django Framework e REST, Flask, Spring Boot");
            printLine("• Banco de Dados : SQL Server, Oracle, MySQL");
            printLine("• DevOps / Infra : Docker, Docker Compose, Kubernetes");
            printLine("• Frontend       : HTML, CSS\n");
            showPrimaryList();
            break;

          case '3':
            showSecondaryList();
            break;

          default:
            printLine("❌ Opção inválida. Digite 1, 2 ou 3.", "text-red");
        }
      } else if (state === 'PROJECTS_MENU') {
        if (cleanCmd === '0') {
          showPrimaryList();
        } else if (projects[cleanCmd]) {
          const proj = projects[cleanCmd];
          printLine(`\n--- LENDO README: ${proj.name} ---`, "text-yellow");
          
          if (proj.readme) {
            printLine(proj.readme, "text-white");
          } else {
            printLine("README não encontrado", "text-red");
          }
          
          printLine("\nDigite outro número de repositório (1 a 3) ou '0' para voltar:", "text-yellow");
        } else {
          printLine("❌ Opção inválida. Digite 1, 2, 3 para ver um README ou 0 para voltar.", "text-red");
        }
      }
    }

    function submitCommand() {
      const val = input.value;
      if (val.trim() !== '') {
        handleCommand(val);
        input.value = '';
      }
      focusInput();
    }

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitCommand();
      }
    });

    btnEnter.addEventListener('click', function(e) {
      e.stopPropagation();
      submitCommand();
    });

    document.getElementById('terminal').addEventListener('click', focusInput);

    // Exibe a lista primária imediatamente após o carregamento completo do DOM
    showPrimaryList();
    focusInput();
  });
</script>

</body>
</html>