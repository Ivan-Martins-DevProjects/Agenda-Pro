package api

import (
	"net/http"

	utils "github.com/Agenda-Pro/internal/utils"
)

func AddClients(w http.ResponseWriter, r *http.Request) {
	if err := utils.CheckRequest(r.Method, r.Header.Get("Content-Type")); err != nil {
		http.Error(w, "Formato inválido", http.StatusBadRequest)
	}


}
