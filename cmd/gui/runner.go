package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
)

func (app *application) run() {
	tabs := container.NewAppTabs(
		container.NewTabItem("Publish", app.publishForm()),
		container.NewTabItem("Edit", app.editList()),
	)

	app.window.Resize(fyne.NewSize(750,500))
	app.window.SetContent(tabs)
	app.window.ShowAndRun()
}
