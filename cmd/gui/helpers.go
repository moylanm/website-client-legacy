package main

import (
	"strings"

	"fyne.io/fyne/v2/dialog"
)

type Excerpt struct {
	ID     int64    `json:"id,omitempty"`
	Author string   `json:"author"`
	Work   string   `json:"work"`
	Body   string   `json:"body"`
	Tags   []string `json:"tags"`
}

func newExcerpt(author, work, tags, body string) *Excerpt {
	return &Excerpt{
		Author: author,
		Work:   work,
		Body:   body,
		Tags:   strings.Split(strings.ReplaceAll(tags, " ", ""), ","),
	}
}

func (app *application) showInfo(title, message string) {
	app.window.RequestFocus()
	dialog.ShowInformation(title, message, app.window)
}

func (app *application) showError(err error) {
	app.window.RequestFocus()
	dialog.ShowError(err, app.window)
}
