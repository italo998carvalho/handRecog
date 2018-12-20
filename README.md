## Introdução
Sistema de reconhecimento de imagens para predizer através da foto de uma mão, se a mesma se encontra aberta ou fechada.

## Pré-processamento
- Converte o esquema de cores da imagem para HSV, para pegar a versão em preto e branco.
- Faz o aguçamento de bordas através do filtro laplaciano.
- Equaliza o histograma da imagem para evidenciar os detalhes.
- Converte a imagem para binária
- Executa os algoritmos de abertura e fechamento para reduzir ruídos

## Extração das informações e predição do resultado
Com a imagem binarizada, os sete [momentos de hu](https://pt.wikipedia.org/wiki/Momentos_invariantes_de_uma_imagem#Momentos_Invariantes_de_Hu) são extraídos e através do algoritmo K-NN, os valores são comparados com os armazenados no banco e assim o sistema realiza a predição.

## Executar a aplicação
#### Requisitos
- Python 3.X
- Pip
- PostgreSQL (ou qualquer outro banco relacional suportado pela biblioteca flask-sqlalchemy)

#### Execução
- Faça o download deste repositório e o acesse via terminal
- Efetue as configurações do banco de dados em handRecog/views/recog.py
- Efetue a instalação das dependências via pip
```bash
pip install -r requirements.txt
```
- Execute a aplicação
```bash
python3 run.py
```