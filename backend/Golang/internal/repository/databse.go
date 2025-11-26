// Package repository para postgres
package repository

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/Agenda-Pro/internal/structs"
	"github.com/joho/godotenv"
	_ "github.com/jackc/pgx/v5/stdlib"

)

type Repository struct {
	DB *sql.DB
}

var (
	UserNotFound = structs.CreateError(404, "Usuário não encontrado")
)

func GetPool() (*sql.DB, error) {
	err := godotenv.Load()
	if err != nil {
		return nil, structs.CreateError(500, "Erro ao carregar as variáveis de ambiente")
	}

	postgres := os.Getenv("SQL_URL")
	if postgres == "" {
		return nil, fmt.Errorf("variáveis de conexão ao banco de dados nulas: %v", err)
	}
	db, err := sql.Open("pgx", postgres)
	if err != nil {
		return nil, fmt.Errorf("erro ao conectar ao banco de dados: %v", err)
	}

	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(10)
	db.SetConnMaxLifetime(time.Hour)

	return db, err

}

func NewRepository(db *sql.DB) *Repository {
	return &Repository{
		DB: db,
	}
}

func (r *Repository) CheckLogin(ctx context.Context ,email, password string) (*structs.TokenJwt, error) {
	query := "SELECT id, role, instance, isConnected FROM users WHERE email = $1 AND password = $2"

	var id int
	var role, instance string
	var isConnected bool

	err := r.DB.QueryRowContext(ctx, query, email, password).Scan(&id, &role, &instance, &isConnected)
	if err != nil {
		if err == sql.ErrNoRows {
			erro := structs.CreateError(401, "Email ou senha inválidos")
			fmt.Println(err)
			return nil, erro
		}

		log.Printf("Erro ao buscar usuário no banco de dados: %v", err)
		erro := structs.CreateError(500, "Erro interno de servidor")
		return nil, erro
	}

	data := structs.TokenJwt {
		ID: id,
		Role: role,
		Instance: instance,
		IsConnected: isConnected,
	}

	return &data, nil
}
