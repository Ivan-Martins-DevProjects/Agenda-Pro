package security

import (
	"fmt"
	"os"
	"time"

	"github.com/Agenda-Pro/internal/structs"
	"github.com/joho/godotenv"
	"github.com/golang-jwt/jwt/v5"
)

func CreateToken(s *structs.TokenJwt) (string, error) {
	err := godotenv.Load()
	if err != nil {
		erro := structs.CreateError(500, "Erro interno do servidor")
		fmt.Println(err)
		return "", erro
	}

	key := os.Getenv("JWT_KEY")
	claims := structs.TokenJwt {
		ID: s.ID,
		Nome: s.Nome,
		Email: s.Email,
		Instance: s.Instance,
		IsConnected: s.IsConnected,
		Role: s.Role,
		RegisteredClaims: jwt.RegisteredClaims {
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(1 *time.Hour)),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenStr, err := token.SignedString([]byte(key))
	if err != nil {
		erro := structs.CreateError(500, "Erro interno do servidor")
		fmt.Println(err)
		return "", erro

	}

	return tokenStr, nil
}

