package main

import (
	"flag"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
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

type application struct {
	config config
	window fyne.Window
}

func main() {
	var cfg config

	flag.StringVar(&cfg.addr.host, "server-host", "localhost", "Server host")
	flag.IntVar(&cfg.addr.port, "server-port", 4000, "Server port")

	flag.StringVar(&cfg.admin.username, "admin-username", "", "Server admin username")
	flag.StringVar(&cfg.admin.password, "admin-password", "", "Server admin password")

	flag.Parse()

	gui := app.New()
	window := gui.NewWindow("Website Client")

	app := &application{
		config: cfg,
		window: window,
	}

	app.run()
}
