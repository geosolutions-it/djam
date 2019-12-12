- python manage.py creatersakey
- python manage.py rundramatiq

- html for mjml generation - write down + docker (node.js)
```#!/bin/bash
cd app/email_engine/templates/cyberus_key
for D in *; do
    if [ -d "${D}" ]; then
        ../../../../node_modules/mjml/bin/mjml $D/$D.mjml -o $D/$D.html   # templates generate
    fi
done
cd ../eliot_pro/
for D in *; do
    if [ -d "${D}" ]; then
        ../../../../node_modules/mjml/bin/mjml $D/$D.mjml -o $D/$D.html   # templates generate
    fi
done```
