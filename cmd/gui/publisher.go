package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

func (app *application) publish(excerpt *Excerpt) string {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return fmt.Sprintf("marshaling error: %s", err.Error())
	}

	req, err := http.NewRequest(
		http.MethodPost,
		fmt.Sprintf("http://%s:%d/excerpts", app.config.addr.host, app.config.addr.port),
		strings.NewReader(string(js)),
	)
	if err != nil {
		return fmt.Sprintf("request creation error: %s", err.Error())
	}

	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return fmt.Sprintf("request send error: %s", err.Error())
	}
	defer res.Body.Close()

	body, _:= io.ReadAll(res.Body)

	return string(body)
}
