from django.contrib.admin import AllValuesFieldListFilter


class AllValuesChoicesFieldListFilter(AllValuesFieldListFilter):

    def choices(self, changelist):
        yield {
            "selected": (
                    self.lookup_val is None
                    and self.lookup_val_isnull is None
            ),
            "query_string": changelist.get_query_string(
                {}, [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            "display": "All",
        }
        include_none = False

        # all choices for this field
        choices = dict(self.field.choices)

        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = str(val)
            yield {
                "selected": self.lookup_val == val,
                "query_string": changelist.get_query_string({
                    self.lookup_kwarg: val,
                }, [self.lookup_kwarg_isnull]),

                # instead code, display title
                "display": choices[val],
            }
        if include_none:
            yield {
                "selected": bool(self.lookup_val_isnull),
                "query_string": changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                "display": self.empty_value_display,
            }
