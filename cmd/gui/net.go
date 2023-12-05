package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

func (app *application) publishExcerpt(excerpt *Excerpt) string {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return errorMessage("marshaling error", err)
	}

	req, err := http.NewRequest(
		http.MethodPost,
		app.config.publishUrl,
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

	body, _ := io.ReadAll(res.Body)

	return string(body)
}

func (app *application) listExcerpts() []Excerpt {
	req, err := http.NewRequest(
		http.MethodGet,
		app.config.listUrl,
		nil,
	)
	if err != nil {
		fmt.Println(errorMessage("request creation error", err))
		return []Excerpt{}
	}

	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		fmt.Println(errorMessage("request send error", err))
		return []Excerpt{}
	}
	defer res.Body.Close()

	var excerpts map[string][]Excerpt

	dec := json.NewDecoder(res.Body)

	err = dec.Decode(&excerpts)
	if err != nil {
		fmt.Println(errorMessage("json decoding error", err))
		return []Excerpt{}
	}

	return excerpts["excerpts"]
}

func (app *application) updateExcerpt(id int64, excerpt *Excerpt) string {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return errorMessage("marshaling error", err)
	}

	req, err := http.NewRequest(
		http.MethodPatch,
		fmt.Sprintf("%s/%d", app.config.publishUrl, id),
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

	body, _ := io.ReadAll(res.Body)

	return string(body)
}