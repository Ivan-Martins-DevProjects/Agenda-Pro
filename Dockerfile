# =================================================================
# ESTÁGIO 1: Compilador da Aplicação Go
# =================================================================
# Usa uma imagem oficial do Go para compilar o binário
FROM golang:1.25.4-alpine AS builder-go

# Define o diretório de trabalho para o código Go
WORKDIR /app/backend/golang

# Copia os arquivos de dependência do Go (go.mod e go.sum)
COPY backend/Golang/go.mod backend/Golang/go.sum ./

# Baixa as dependências. Isso é feito em um passo separado para aproveitar o cache do Docker
RUN go mod download

# Copia todo o código fonte da aplicação Go
COPY backend/Golang/ ./

# Compila a aplicação, criando um binário estático chamado 'api-go'
# -w e -s removem informações de debug, tornando o binário menor
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o api-go -ldflags="-w -s" ./cmd


# =================================================================
# ESTÁGIO 2: Imagem Final
# =================================================================
# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho principal
WORKDIR /app

# Copia e instala as dependências do Python
COPY backend/Python/requirements.txt ./backend/python/
RUN pip install --no-cache-dir -r backend/python/requirements.txt

# Copia o código Python para a imagem
COPY backend/Python/ ./backend/python/

# Copia o binário Go compilado do estágio "builder-go" para a imagem final
COPY --from=builder-go /app/backend/golang/api-go ./backend/golang/

# Copia o script de inicialização
COPY start.sh .

# Expõe as portas que suas APIs usam
# Substitua 8000 e 8080 pelas portas reais das suas APIs
EXPOSE 8000
EXPOSE 8080

# Define o script de inicialização como o comando a ser executado
CMD ["./start.sh"]
