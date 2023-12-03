package main

import "fmt"

func errorMessage(message string, err error) string {
	return fmt.Sprintf("%s: %s", message, err.Error())
}
