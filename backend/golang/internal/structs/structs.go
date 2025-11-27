// Package structs responsável
package structs

import "github.com/golang-jwt/jwt/v5"

type Login struct {
	Email string `json:"email"`
	Password string `json:"senha"`
}

type Usuario struct {
	Status string `json:"Status"`
	Token string `json:"Token"`
	Nome string `json:"Nome"`
	Idade int `json:"Idade"`

}

type TokenJwt struct {
	ID string
	BussinesID string
	Nome string
	Email string
	Instance string
	IsConnected bool
	Role string
	jwt.RegisteredClaims
}

