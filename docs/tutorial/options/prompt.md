It's also possible to, instead of just showing an error, ask for the missing value with `prompt=True`:

```Python hl_lines="4"
{!../docs_src/options/prompt/tutorial001.py!}
```

And then your program will ask the user for it in the terminal:

<div class="termy">

```console
// Call it with the NAME CLI argument
$ python main.py Camila

// It asks for the missing CLI option --lastname
# Lastname: $ Gutiérrez

Hello Camila Gutiérrez
```

</div>

## Customize the prompt

You can also set a custom prompt, passing the string that you want to use instead of just `True`:

```Python hl_lines="5"
{!../docs_src/options/prompt/tutorial002.py!}
```

And then your program will ask for it using with your custom prompt:

<div class="termy">

```console
// Call it with the NAME CLI argument
$ python main.py Camila

// It uses the custom prompt
# Please tell me your last name: $ Gutiérrez

Hello Camila Gutiérrez
```

</div>

## Confirmation prompt

In some cases you could want to prompt for something and then ask the user to confirm it by typing it twice.

You can do it passing the parameter `confirmation_prompt=True`.

Let's say it's a CLI app to delete a project:

```Python hl_lines="4"
{!../docs_src/options/prompt/tutorial003.py!}
```

And it will prompt the user for a value and then for the confirmation:

<div class="termy">

```console
$ python main.py

// Your app will first prompt for the project name, and then for the confirmation
# Project name: $ Old Project
# Repeat for confirmation: $ Old Project

Deleting project Old Project

// If the user doesn't type the same, receives an error and a new prompt
$ python main.py

# Project name: $ Old Project
# Repeat for confirmation: $ New Spice

Error: the two entered values do not match

# Project name: $ Old Project
# Repeat for confirmation: $ Old Project

Deleting project Old Project

// Now it works 🎉
```

</div>
