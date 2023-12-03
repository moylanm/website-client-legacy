package main

import (
	"flag"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
)

type config struct {
	addr struct {
		host string
		port int
	}
	admin struct {
		username string
		password string
	}
}

func main() {
	var cfg config

	flag.StringVar(&cfg.addr.host, "server-host", "localhost", "Server host")
	flag.IntVar(&cfg.addr.port, "server-port", 4000, "Server port")

	flag.StringVar(&cfg.admin.username, "admin-username", "", "Server admin username")
	flag.StringVar(&cfg.admin.password, "admin-password", "", "Server admin password")

	flag.Parse()

	app := app.New()
	window := app.NewWindow("Website Client")

	tabs := container.NewAppTabs(
		container.NewTabItem("Publish", publishForm()),
		container.NewTabItem("Edit", editList()),
	)

	window.Resize(fyne.NewSize(750,500))
	window.SetContent(tabs)
	window.ShowAndRun()
}
