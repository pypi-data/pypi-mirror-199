# Domini

A small, simple package for generating HTML documents.
The syntax aims to immitate HTML as closely as possible for legibility and easy of use.

## Attributes

Attributes *without* a value are entered as *positional arguments*.<br>
Attributes *with* a value are entered as *keyword arguments*.

To specify attributes that collide with reserved Python keywords,
append an underscore and it will be removed.

#### Python

```py
from domini.html import dialog

dialog('open', class_='mydialog')
```

#### HTML

```html
<dialog open class='mydialog'>
```

## Content

To add children to an element, you can use either the `add` method or the short-hand greater-than operator. The right-hand side can be either any sequence, iterator, or generator of elements or a lone element. These elements can be either other tags or plain strings.

**NOTE**: `add` does add them to the current object. `>` returns a new, identical element with those children added.

```py
ul(class_='todo')> (
    li()> 'Buy a fruit basket.',
    li()> (
        'Read', a(href='https://wikipedia.org/')> 'Wikipedia',
        'to learn more about things you may have not otherwise cared about.',
    ),
)
```

## Closing tags

A tag is only closed if content is provided. E.g. `<p></p>` as opposed to `<p>`. This can be an empty tuple.

```py
section()> ()
```

For open tags like `<br>` and `<hr>`, you simply do `br()` and `hr()`.