# 🌹 Contributing to HextechButEfficient

First off, thanks for taking your time to contribute. It makes the tool substantially better.

## Guidelines

Actually, not sure what to write here, except for

* Please, use common developers' etiquette 🌹.

## Good Bug Reports

1. Don't open duplicate issues. Please search your issue to see if it has been asked already. Duplicate issues will be closed.

## Good Pull Requests

In general, PRs are welcome. Maybe, I will edit better this part later.

## To New Script contributors

Some of these points are obvious from reading the code but nevertheless.

* Please, subclass `AluConnector` in your script and implement `callback` method to it which is supposed to do the whole job
  * for streamlined user experience use `self.confirm`, `self.output` to show-case script result before user confirms them
* Use Black Formatting tool
  * Overall, my own formatting/typechecking preferences are listed in `pyproject.toml` so if your formatter/ide supports it - good.
* In GUI I simply use icons from emojipedia
  * i.e. I use <https://emojipedia.org/wastebasket#designs> for `BEDisenchantEverything`
  * from that page I choose Microsoft/Windows 11 23H2 styled ones, download `.png` and rename them to remove the gibberish part.
