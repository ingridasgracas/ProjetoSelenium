# Serviços Prefeitura Rio - Web Scraping

Este projeto realiza a extração automatizada de links dos serviços disponíveis no portal da Prefeitura do Rio de Janeiro (https://pref.rio/). Utilizando Selenium WebDriver, o script coleta informações sobre os serviços e seus respectivos links de acesso.

## Funcionalidades

- Extração automatizada de links dos serviços
- Coleta de informações por categoria de serviço
- Exportação dos dados para arquivo Excel
- Tratamento de erros e timeout
- Modo headless para execução em background

## Requisitos

- Python 3.8+
- Google Chrome
- ChromeDriver

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/ingridasgracas/ProjetoSelenium.git
   ```

2. Entre no diretório do projeto:
   ```bash
   cd ProjetoSelenium
   ```

3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Execute o script:
   ```bash
   python ScrapingPrefrio.py
   ```

2. Os resultados serão salvos na pasta `output` em um arquivo Excel chamado `servicos_pref_rio_links.xlsx`

## Estrutura dos Dados

O arquivo Excel gerado contém as seguintes colunas:
- Categoria: categoria do serviço
- Serviço: nome do serviço
- URL Serviço: URL da página de descrição do serviço
- Link Final: URL do botão "Acessar serviço"

## Notas

- O script utiliza modo headless por padrão (execução sem interface gráfica)
- É necessário que o ChromeDriver seja compatível com a versão do Google Chrome instalada
- O script inclui tratamento de erros para páginas que não carregam ou não possuem o botão de acesso

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autora

Ingrid Gracas
