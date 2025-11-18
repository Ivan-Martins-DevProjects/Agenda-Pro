package structs

import (
	"encoding/json"
	"net/http"
)

type CustomError struct {
	Status string `json:"status"`
	Code int `json:"code"`
	Message string `json:"message"`
}

func (e *CustomError) Error() string {
	return e.Message
}

func CreateError(code int, message string) *CustomError{
	return &CustomError {
		Status: "error",
		Code: code,
		Message: message,
	}
}

func SendError(w http.ResponseWriter, Err *CustomError)  {
	w.Header().Set("Content-Type", "application/json")

	w.WriteHeader(Err.Code)

	json.NewEncoder(w).Encode(Err)
}
