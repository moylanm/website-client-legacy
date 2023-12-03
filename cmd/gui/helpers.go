package main

import (
	"strings"

	"mylesmoylan.net/internal/validator"
)

type Excerpt struct {
	Author string
	Work   string
	Body   string
	Tags   []string
}

func marshalExcerptForm(author, work, tags, body string) *Excerpt {
	return &Excerpt{
		Author: author,
		Work:   work,
		Body:   body,
		Tags:   strings.Split(strings.ReplaceAll(tags, " ", ""), ","),
	}
}

func validateExcerpt(v *validator.Validator, excerpt *Excerpt) {
	v.Check(excerpt.Author != "", "author", "must be provided")

	v.Check(excerpt.Work != "", "work", "must be provided")

	v.Check(excerpt.Body != "", "body", "must be provided")

	v.Check(excerpt.Tags != nil, "tags", "must be provided")
	v.Check(len(excerpt.Tags) >= 1, "tags", "must contain at least one tag")
	v.Check(len(excerpt.Tags) <= 5, "tags", "must not contain more than 5 tags")
	v.Check(validator.Unique(excerpt.Tags), "tags", "must not contain duplicate values")
}
