package main

import (
	"flag"
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/widget"
)

type config struct {
	publishUrl string
	listUrl    string
	windowSize fyne.Size
	addr       struct {
		host string
		port int
	}
	admin struct {
		username string
		password string
	}
}

type application struct {
	config config
	window fyne.Window
	modal  *widget.PopUp
}

func main() {
	var cfg config

	flag.StringVar(&cfg.addr.host, "server-host", "localhost", "Server host")
	flag.IntVar(&cfg.addr.port, "server-port", 4000, "Server port")

	flag.StringVar(&cfg.admin.username, "admin-username", "", "Server admin username")
	flag.StringVar(&cfg.admin.password, "admin-password", "", "Server admin password")

	flag.Parse()

	var protocol string

	if cfg.addr.host == "localhost" {
		protocol = "http"
	} else {
		protocol = "https"
	}

	cfg.publishUrl = fmt.Sprintf("%s://%s:%d/excerpts", protocol, cfg.addr.host, cfg.addr.port)
	cfg.listUrl = fmt.Sprintf("%s://%s:%d/json/excerpts", protocol, cfg.addr.host, cfg.addr.port)
	cfg.windowSize = fyne.NewSize(750, 400)

	gui := app.New()
	window := gui.NewWindow("Website Client")

	app := &application{
		config: cfg,
		window: window,
		modal:  &widget.PopUp{},
	}

	app.run()
}
