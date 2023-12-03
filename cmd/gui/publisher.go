package main

import (
	"encoding/json"
	"io"
	"net/http"
	"strings"
)

func (app *application) publish(excerpt *Excerpt) string {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return errorMessage("marshaling error", err)
	}

	req, err := http.NewRequest(
		http.MethodPost,
		app.config.url,
		strings.NewReader(string(js)),
	)
	if err != nil {
		return errorMessage("request creation error", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return errorMessage("request send error", err)
	}
	defer res.Body.Close()

	body, _:= io.ReadAll(res.Body)

	return string(body)
}
