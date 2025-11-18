//Package security contains...
package security

import (
	"golang.org/x/crypto/bcrypt"
)

func GenerateHash(value string) (string, error)  {
	code, err := bcrypt.GenerateFromPassword([]byte(value), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}

	return string(code), nil
}
