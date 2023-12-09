package main

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
)

func entryText(excerpt Excerpt) string {
	return fmt.Sprintf("%s - %s", excerpt.Author, excerpt.Work)
}

func (app *application) publishForm() *widget.Form {
	authorField := widget.NewEntry()
	workField := widget.NewEntry()
	bodyField := widget.NewMultiLineEntry()
	bodyField.Wrapping = fyne.TextWrapWord

	return &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Author", Widget: authorField},
			{Text: "Work", Widget: workField},
			{Text: "Body", Widget: bodyField},
		},
		CancelText: "Clear",
		OnCancel: func() {
			authorField.SetText("")
			workField.SetText("")
			bodyField.SetText("")
		},
		SubmitText: "Publish",
		OnSubmit: func() {
			excerpt := newExcerpt(
				authorField.Text,
				workField.Text,
				bodyField.Text,
			)

			res, err := app.publishExcerpt(excerpt)
			if err != nil {
				app.showError(err)
			} else {
				app.refreshAfterPublish()
				app.showInfo("Server Response", res)
			}
		},
	}
}

func (app *application) editList() *widget.List {
	return widget.NewList(
		func() int {
			return len(app.excerpts)
		},
		func() fyne.CanvasObject {
			return &widget.Button{}
		},
		func(lii widget.ListItemID, co fyne.CanvasObject) {
			text := entryText(app.excerpts[lii])

			co.(*widget.Button).SetText(text)
			co.(*widget.Button).Alignment = widget.ButtonAlignLeading
			co.(*widget.Button).OnTapped = func() {
				w := fyne.CurrentApp().NewWindow(text)
				w.SetContent(app.newEntryForm(w, app.excerpts[lii]))
				w.Resize(app.config.windowSize)
				w.Show()
			}
		},
	)
}

func (app *application) newEntryForm(window fyne.Window, excerpt Excerpt) *widget.Form {
	authorField := widget.NewEntry()
	authorField.SetText(excerpt.Author)

	workField := widget.NewEntry()
	workField.SetText(excerpt.Work)

	bodyField := widget.NewMultiLineEntry()
	bodyField.Wrapping = fyne.TextWrapWord
	bodyField.SetText(excerpt.Body)

	return &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Author", Widget: authorField},
			{Text: "Work", Widget: workField},
			{Text: "Body", Widget: bodyField},
		},
		CancelText: "Delete",
		OnCancel: func() {
			res, err := app.deleteExcerpt(excerpt.ID)
			if err != nil {
				window.Close()
				app.showError(err)
			} else {
				window.Close()
				app.refreshAfterEdit()
				app.showInfo("Server Response", res)
			}
		},
		SubmitText: "Update",
		OnSubmit: func() {
			excerpt.Author = authorField.Text
			excerpt.Work = workField.Text
			excerpt.Body = bodyField.Text

			res, err := app.updateExcerpt(excerpt)
			if err != nil {
				window.Close()
				app.showError(err)
			} else {
				window.Close()
				app.refreshAfterEdit()
				app.showInfo("Server Response", res)
			}
		},
	}
}
