 package utils

import (
	"fmt"
	"net/http"
)

func CheckRequest(method, header string) error {
	if method != http.MethodPost {
		return fmt.Errorf("method-error")
	}

	if header != "application/json" {
		return fmt.Errorf("header-error")
	}

	return nil
}
