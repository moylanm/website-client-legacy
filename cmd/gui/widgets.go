package main

import (
	"fyne.io/fyne/v2/widget"
)


func publishWidget() *widget.Form {
	authorField := widget.NewEntry()
	workField := widget.NewEntry()
	tagsField := widget.NewEntry()
	bodyField := widget.NewMultiLineEntry()

	return &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Author", Widget: authorField},
			{Text: "Work", Widget: workField},
			{Text: "Tags", Widget: tagsField},
			{Text: "Body", Widget: bodyField},
		},
		SubmitText: "Publish",
		OnCancel: func() {
			// clear form
		},
		CancelText: "Clear",
		OnSubmit: func() {
			// submit form
		},
	}
}
