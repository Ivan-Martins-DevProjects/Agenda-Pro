// Package api para endpoints
package api

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/Agenda-Pro/internal/repository"
	"github.com/Agenda-Pro/internal/security"
	"github.com/Agenda-Pro/internal/structs"
	"github.com/Agenda-Pro/internal/utils"
)

func UserLogin(w http.ResponseWriter, r *http.Request)  {
	if err := utils.CheckRequest(r.Method, r.Header.Get("Content-Type")); err != nil {
		erro := structs.CreateError(400, "Formato Inválido")
		structs.SendError(w, erro)
		return
	}

	// Validação de informações de login
	var login structs.Login

	err := json.NewDecoder(r.Body).Decode(&login)
	if err != nil {
		erro := structs.CreateError(500, "Erro Interno do servidor")
		structs.SendError(w, erro)
		return
	}

	//Estabelecendo conexão com o banco de dados
	db, err := repository.GetPool()
	if err != nil {
		erro := structs.CreateError(500, "Erro Interno do servidor")
		structs.SendError(w, erro)
		log.Printf("Erro ao configurar pool de conexões: %v", err)
		return
	}
	Repository := repository.NewRepository(db)

	/* Função para gerar hash de senha
	senhaHash, err := security.GenerateHash(login.Password)
	if err != nil {
		erro := structs.CreateError(500, "Erro interno do servidor")
		structs.SendError(w, erro)
		return
	}

	fmt.Println(senhaHash)
	*/

	//Consultando credenciais no banco de dados

	credentials, err := Repository.CheckLogin(r.Context(), login.Email, login.Password)
	if err != nil {
		if customErr, ok := err.(*structs.CustomError); ok {
			structs.SendError(w, customErr)
			return
		}
	}

	token, err := security.CreateToken(credentials)
	if err != nil {
		if customErr, ok := err.(*structs.CustomError); ok {
			structs.SendError(w, customErr)
			return
		}

	}

	w.Header().Set("Content-Type", "application/json")

	data := structs.Usuario {
		Status: "success",
		Token: token,
		Nome: "Ivan",
		Idade: 25,
	}

	if err = json.NewEncoder(w).Encode(data); err != nil {
		fmt.Println("Erro ao codificar resposta para o servidor", err)
		http.Error(w, "Erro ao gerar JSON", http.StatusInternalServerError)
		return
	}

}
