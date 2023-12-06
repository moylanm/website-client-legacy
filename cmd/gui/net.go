package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

func (app *application) publishExcerpt(excerpt *Excerpt) (string, error) {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequest(
		http.MethodPost,
		app.config.publishUrl,
		strings.NewReader(string(js)),
	)
	if err != nil {
		return "", err
	}

	req.Header.Set("Content-Type", "application/json")
	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)

	return string(body), nil
}

func (app *application) listExcerpts() ([]Excerpt, error) {
	req, err := http.NewRequest(
		http.MethodGet,
		app.config.listUrl,
		nil,
	)
	if err != nil {
		return nil, err
	}

	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	var excerpts map[string][]Excerpt

	dec := json.NewDecoder(res.Body)

	err = dec.Decode(&excerpts)
	if err != nil {
		return nil, err
	}

	return excerpts["excerpts"], nil
}

func (app *application) updateExcerpt(excerpt *Excerpt) string {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return errorMessage("marshaling error", err)
	}

	req, err := http.NewRequest(
		http.MethodPatch,
		fmt.Sprintf("%s/%d", app.config.publishUrl, excerpt.ID),
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

func (app *application) deleteExcerpt(id int64) string {
	req, err := http.NewRequest(
		http.MethodDelete,
		fmt.Sprintf("%s/%d", app.config.publishUrl, id),
		nil,
	)
	if err != nil {
		return errorMessage("request creation error", err)
	}

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
