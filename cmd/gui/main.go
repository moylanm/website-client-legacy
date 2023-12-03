package main

import (
	"flag"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

type config struct {
	username string
	password string
}

func main() {
	var cfg config

	flag.StringVar(&cfg.username, "admin-username", "", "Server admin username")
	flag.StringVar(&cfg.password, "admin-password", "", "Server admin password")

	app := app.New()
	window := app.NewWindow("Website Client")

	tabs := container.NewAppTabs(
		container.NewTabItem("Publish", publishWidget()),
		container.NewTabItem("Edit", widget.NewLabel("Edit")),
	)

	window.Resize(fyne.NewSize(750,500))
	window.SetContent(tabs)
	window.ShowAndRun()
}
