package validator

import (
	"fmt"
	"strings"
)

type Validator struct {
	Errors map[string]string
}

func New() *Validator {
	return &Validator{Errors: make(map[string]string)}
}

func (v *Validator) ErrorsToString() string {
	var sb strings.Builder

	for k, v := range v.Errors {
		fmt.Fprintf(&sb, "%s: %s\n", k, v)
	}

	return sb.String()
}

func (v *Validator) Valid() bool {
	return len(v.Errors) == 0
}


func (v *Validator) AddError(key, message string) {
	if _, exists := v.Errors[key]; !exists {
		v.Errors[key] = message
	}
}

func (v *Validator) Check(ok bool, key, message string) {
	if !ok {
		v.AddError(key, message)
	}
}

func Unique[T comparable](values []T) bool {
	uniqueValues := make(map[T]bool)

	for _, value := range values {
		uniqueValues[value] = true
	}

	return len(values) == len(uniqueValues)
}
