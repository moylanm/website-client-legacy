package main

import (
	"fmt"

	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
)

type Excerpt struct {
	ID     int64  `json:"id,omitempty"`
	Author string `json:"author"`
	Work   string `json:"work"`
	Body   string `json:"body"`
}

func newExcerpt(author, work, body string) *Excerpt {
	return &Excerpt{
		Author: author,
		Work:   work,
		Body:   body,
	}
}

func (app *application) fetchExcerpts() {
	var err error

	app.excerpts, err = app.listExcerpts()
	if err != nil {
		fmt.Printf("error fetching excerpts: %s", err.Error())
	}
}

func (app *application) refreshAfterPublish() {
	app.fetchExcerpts()

	tabs := container.NewAppTabs(
		container.NewTabItem("Publish", app.publishForm()),
		container.NewTabItem("Edit", app.editList()),
	)

	app.window.SetContent(tabs)
}

func (app *application) refreshAfterEdit() {
	app.fetchExcerpts()

	editTab := container.NewTabItem("Edit", app.editList())

	tabs := container.NewAppTabs(
		container.NewTabItem("Publish", app.publishForm()),
		editTab,
	)

	tabs.Select(editTab)
	app.window.SetContent(tabs)
}

func (app *application) showInfo(title, message string) {
	dialog.ShowInformation(title, message, app.window)
}

func (app *application) showError(err error) {
	dialog.ShowError(err, app.window)
}
