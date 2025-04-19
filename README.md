# Minecraft Backup Tool

## Descrição

O **Minecraft Backup Tool** é uma ferramenta de linha de comando (CLI) desenvolvida em Python para criar backups dos mundos salvos do Minecraft. Ele suporta as edições **Java** e **Bedrock**, detectando automaticamente os diretórios de mundos salvos e permitindo ao usuário criar backups em formato `.zip`.

## Funcionalidades - v0.2.1

- Suporte a descrições/tags de backup (opcional), armazenadas em `metadata.json` dentro do ZIP.
- Listagem de backups existentes com suas descrições (CLI e GUI).
- Restauração de backups: extrai arquivos do mundo e cria `mvp2.json` com metadados na pasta do mundo.
- Interface gráfica (GUI):
  - Campo de entrada para descrição/tag.  
  - Listagem lado a lado de mundos e backups.  
  - Botões para criar e restaurar backup.  
  - Pop‑ups de notificação de sucesso/erro.
- CLI interativa aprimorada:
  - Prompt para adicionar descrição/tag no momento do backup.  
  - Validação de caracteres inválidos na descrição.

## Requisitos

- Python 3.8 ou superior.

## Instalação

Para garantir que o projeto funcione com os pacotes corretos e evitar conflitos com outros projetos Python no seu sistema, recomenda-se o uso de um ambiente virtual.

1.  Clone este repositório:
    ```bash
    git  clone  <URL_DO_REPOSITORIO>
    cd  MVP_MicroSaas
    ```
2.  Instale as dependências usando o Pipenv:

    ```bash
    pipenv  sync
    ```

## Uso

1.  Execute o programa principal na interface de linha de comando (CLI):

    ```bash
    python src/main_cli.py
    ```
   Ou para abrir a interface gráfica (GUI):

    ```bash
    python src/main_gui.py
    ```

2.  Escolha a edição do Minecraft:

    - Digite `java` para a edição Java.
    - Digite `bedrock` para a edição Bedrock.

3.  Selecione o mundo salvo para criar o backup:

    - O programa listará os mundos disponíveis.
    - Escolha o número correspondente ao mundo desejado.

4.  Adicione uma descrição/tag opcional para o backup.

5.  O backup será criado na pasta `backups_worlds`.

6.  Para restaurar um backup, selecione o arquivo desejado e o programa criará os arquivos do mundo e o `mvp2.json` com metadados.

### Exemplo de saída:

    ==== Minecraft Backup CLI ====

    Qual edição você usa? (java/bedrock): java

    Mundos encontrados em C:\Users\danie\AppData\Roaming\.minecraft\saves

    1. MeuMundo

    2. OutroMundo

    0. Sair

    Escolha o número do mundo para fazer backup: 1

    Adicione uma descrição/tag para o backup (opcional): Backup inicial

    Backup criado: backups_worlds/MeuMundo_20250417-153000.zip

## Testes

Para validar o funcionamento e garantir que futuras alterações não quebrem funcionalidades, execute a suíte de testes com pytest:

```bash
# Instale o pytest se ainda não tiver:
pip install --dev pytest

# Execute todos os testes:
pytest -q
```

## Estrutura do Projeto

- **src/main_cli.py**: Entry-point para a interface de linha de comando (CLI).
- **src/main_gui.py**: Entry-point para a interface gráfica (GUI).
- **src/cli/**: Lógica da CLI.
  - **cli_main.py**: Função `run_cli()` que implementa o fluxo de backup pela linha de comando.
- **src/gui/**: Componentes da GUI.
  - **app.py**: Classe `GuiApp` com construção de widgets e callbacks.
  - **main_window.py**: Stub que expõe `run_gui()`.
- **src/backup/**: Lógica de negócio compartilhada.
  - **core.py**: Funções para listar mundos, criar e restaurar backups.
  - **detect_java.py**: Detecta o caminho dos mundos Java.
  - **detect_bedrock.py**: Detecta o caminho dos mundos Bedrock.
- **tests/**: Testes unitários e de integração usando pytest.
- **backups_worlds/**: Diretório onde os backups são salvos.
- **requirements.txt**, **Pipfile** e **Pipfile.lock**: Dependências do projeto.

## Tratamento de Erros

- **Edição inválida**: O programa exibe uma mensagem de erro se o usuário digitar algo diferente de `java` ou `bedrock`.
- **Caminho não encontrado**: Se o diretório de mundos salvos não existir, o programa exibirá uma mensagem de erro indicando que o Minecraft não foi encontrado ou que não há mundos salvos.
- **Sistema operacional não suportado**: O programa suporta apenas Windows, macOS e Linux para a edição Java, e apenas Windows para a edição Bedrock.
