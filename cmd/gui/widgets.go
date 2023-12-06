package main

import (
	"fmt"
	"strings"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
)

func (app *application) publishForm() *widget.Form {
	authorField := widget.NewEntry()
	workField := widget.NewEntry()
	tagsField := widget.NewEntry()
	bodyField := widget.NewMultiLineEntry()
	bodyField.Wrapping = fyne.TextWrapWord

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
			excerpt := newExcerpt(
				authorField.Text,
				workField.Text,
				tagsField.Text,
				bodyField.Text,
			)

			res, err := app.publishExcerpt(excerpt)
			if err != nil {
				app.showError(err)
			} else {
				app.showInfo("Publish", res)
				authorField.SetText("")
				workField.SetText("")
				tagsField.SetText("")
				bodyField.SetText("")
			}
		},
	}
}

func (app *application) editList() *widget.List {
	excerpts, err := app.listExcerpts()
	if err != nil {
		app.showError(err)
		return &widget.List{}
	}

	return widget.NewList(
		func() int {
			return len(excerpts)
		},
		func() fyne.CanvasObject {
			return &widget.Button{}
		},
		func(lii widget.ListItemID, co fyne.CanvasObject) {
			text := entryText(excerpts[lii])

			co.(*widget.Button).SetText(text)
			co.(*widget.Button).Alignment = widget.ButtonAlignLeading
			co.(*widget.Button).OnTapped = func() {
				w := fyne.CurrentApp().NewWindow(text)
				w.SetContent(app.newEntryForm(excerpts[lii]))
				w.Resize(app.config.windowSize)
				w.Show()
			}
		},
	)
}

func (app *application) newEntryForm(excerpt Excerpt) *widget.Form {
	authorField := widget.NewEntry()
	authorField.SetText(excerpt.Author)

	workField := widget.NewEntry()
	workField.SetText(excerpt.Work)

	tagsField := widget.NewEntry()
	tagsField.SetText(strings.Join(excerpt.Tags, ","))

	bodyField := widget.NewMultiLineEntry()
	bodyField.Wrapping = fyne.TextWrapWord
	bodyField.SetText(excerpt.Body)

	return &widget.Form{
		Items: []*widget.FormItem{
			{Text: "Author", Widget: authorField},
			{Text: "Work", Widget: workField},
			{Text: "Tags", Widget: tagsField},
			{Text: "Body", Widget: bodyField},
		},
		CancelText: "Delete",
		OnCancel: func() {
			res, err := app.deleteExcerpt(excerpt.ID)
			if err != nil {
				app.showError(err)
			} else {
				app.showInfo("Delete", res)
			}
		},
		SubmitText: "Update",
		OnSubmit: func() {
			excerpt.Author = authorField.Text
			excerpt.Work = workField.Text
			excerpt.Tags = strings.Split(strings.ReplaceAll(tagsField.Text, " ", ""), ",")
			excerpt.Body = bodyField.Text

			res, err := app.updateExcerpt(excerpt)
			if err != nil {
				app.showError(err)
			} else {
				app.showInfo("Update", res)
			}
		},
	}
}

func entryText(excerpt Excerpt) string {
	return fmt.Sprintf("%s - %s", excerpt.Author, excerpt.Work)
}
