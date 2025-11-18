package api

import (
	"net/http"
	"fmt"

	"encoding/json"
	"github.com/Agenda-Pro/internal/structs"
)

func IndexHandler(w http.ResponseWriter, r *http.Request) {
		data := structs.Usuario {
		Status: "success",
		Nome: "Ivan",
		Idade: 25,
	}

	if err := json.NewEncoder(w).Encode(data); err != nil {
		fmt.Println("Erro ao codificar resposta para o servidor", err)
		http.Error(w, "Erro ao gerar JSON", http.StatusInternalServerError)
		return
	}

}
