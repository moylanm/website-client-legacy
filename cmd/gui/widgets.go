package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
	"mylesmoylan.net/internal/validator"
)


func (app *application) excerptForm() *widget.Form {
	authorField := widget.NewEntry()
	workField := widget.NewEntry()
	tagsField := widget.NewEntry()
	bodyField := widget.NewMultiLineEntry()
	bodyField.Wrapping = fyne.TextWrapBreak

	return &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Author", Widget: authorField},
			{Text: "Work", Widget: workField},
			{Text: "Tags", Widget: tagsField},
			{Text: "Body", Widget: bodyField},
		},
		CancelText: "Clear",
		OnCancel: func() {
			authorField.SetText("")
			workField.SetText("")
			tagsField.SetText("")
			bodyField.SetText("")
		},
		SubmitText: "Publish",
		OnSubmit: func() {
			excerpt := marshalExcerptForm(authorField.Text, workField.Text, tagsField.Text, bodyField.Text)
			v := validator.New()

			if validateExcerpt(v, excerpt); !v.Valid() {
				app.showPopUp(v.ErrorsToString())
			} else {
				app.showPopUp(app.publish(excerpt))
			}
		},
	}
}

func (app *application) editList() *widget.List {
	return &widget.List{}
}
