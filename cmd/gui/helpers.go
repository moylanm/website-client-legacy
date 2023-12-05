package main

import (
	"strings"

	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"mylesmoylan.net/internal/validator"
)

type Excerpt struct {
	ID     int64    `json:"id"`
	Author string   `json:"author"`
	Work   string   `json:"work"`
	Body   string   `json:"body"`
	Tags   []string `json:"tags"`
}

func marshalExcerptForm(author, work, tags, body string) *Excerpt {
	return &Excerpt{
		Author: author,
		Work:   work,
		Body:   body,
		Tags:   strings.Split(strings.ReplaceAll(tags, " ", ""), ","),
	}
}

func validateExcerpt(v *validator.Validator, excerpt *Excerpt) {
	v.Check(excerpt.Author != "", "author", "must be provided")

	v.Check(excerpt.Work != "", "work", "must be provided")

	v.Check(excerpt.Body != "", "body", "must be provided")

	v.Check(excerpt.Tags != nil, "tags", "must be provided")
	v.Check(len(excerpt.Tags) >= 1, "tags", "must contain at least one tag")
	v.Check(len(excerpt.Tags) <= 5, "tags", "must not contain more than 5 tags")
	v.Check(validator.Unique(excerpt.Tags), "tags", "must not contain duplicate values")
}

func (app *application) showPopUp(text string) {
	app.modal = widget.NewModalPopUp(
		container.NewVBox(
			widget.NewRichTextWithText(text),
			widget.NewButton("Close", func() { app.modal.Hide() }),
		),
		app.window.Canvas(),
	)

	app.modal.Show()
}
