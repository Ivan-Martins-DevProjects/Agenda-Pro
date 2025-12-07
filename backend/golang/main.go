// Package main provides ...
package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/rs/cors"

	endpoint "github.com/Agenda-Pro/cmd/api"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/login", endpoint.UserLogin)
	mux.HandleFunc("/api/dashboard", endpoint.IndexHandler)

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"http://127.0.0.1:7000", "http://localhost:7000", "http://0.0.0.0:7000"},
		AllowedMethods: []string{"POST", "GET"},
		AllowedHeaders: []string{"*"},
		AllowCredentials: true,
		MaxAge: 12,
		Debug: false,
	})

	handler := c.Handler(mux)

	log.Println("Servidor rodando em http://localhost:8181")
	if err := http.ListenAndServe(":8181", handler); err != nil {
		fmt.Println("Erro ao iniciar o srevidor")
	}
}
