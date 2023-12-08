package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
)

var messageRX = regexp.MustCompile(`"([\w\s]*)"\s*:\s*"([\w\s]*)"`)

func parseMessage(body []byte) (string, string) {
	message := messageRX.FindStringSubmatch(string(body))

	return message[2], message[1]
}

func (app *application) makeAPIRequest(method, url string, body io.Reader, headers http.Header) ([]byte, error) {
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, err
	}

	for key, value := range headers {
		req.Header[key] = value
	}

	req.SetBasicAuth(app.config.admin.username, app.config.admin.password)

	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	responseBody, err := io.ReadAll(res.Body)
	if err != nil {
		return nil, err
	}

	return responseBody, nil
}

func (app *application) listExcerpts() ([]Excerpt, error) {
	responseBody, err := app.makeAPIRequest(
		http.MethodGet,
		app.config.listUrl,
		nil,
		nil,
	)
	if err != nil {
		return nil, err
	}

	var excerpts map[string][]Excerpt

	if err := json.Unmarshal(responseBody, &excerpts); err != nil {
		return nil, err
	}

	return excerpts["excerpts"], nil
}

func (app *application) publishExcerpt(excerpt *Excerpt) (string, error) {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return "", err
	}

	headers := make(http.Header)
	headers.Set("Content-Type", "application/json")
	
	responseBody, err := app.makeAPIRequest(
		http.MethodPost,
		app.config.publishUrl,
		strings.NewReader(string(js)),
		headers,
	)
	if err != nil {
		return "", err
	}

	message, desc := parseMessage(responseBody)
	if desc == "error" {
		return "", errors.New(message)
	}

	return message, nil
}

func (app *application) updateExcerpt(excerpt Excerpt) (string, error) {
	js, err := json.Marshal(excerpt)
	if err != nil {
		return "", err
	}

	headers := make(http.Header)
	headers.Set("Content-Type", "application/json")

	responseBody, err := app.makeAPIRequest(
		http.MethodPatch,
		fmt.Sprintf("%s/%d", app.config.publishUrl, excerpt.ID),
		strings.NewReader(string(js)),
		headers,
	)
	if err != nil {
		return "", err
	}

	message, desc := parseMessage(responseBody)
	if desc == "error" {
		return "", errors.New(message)
	}

	return message, nil
}

func (app *application) deleteExcerpt(id int64) (string, error) {
	responseBody, err := app.makeAPIRequest(
		http.MethodDelete,
		fmt.Sprintf("%s/%d", app.config.publishUrl, id),
		nil,
		nil,
	)
	if err != nil {
		return "", err
	}

	message, desc := parseMessage(responseBody)
	if desc == "error" {
		return "", errors.New(message)
	}

	return message, nil
}
