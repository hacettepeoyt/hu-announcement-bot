# Hacettepe Duyurucusu

## How To Add New Language?

1. Create a file named by the standard [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
2. You see... there are some files named **en.json**, **tr.json**. Copy one of them and paste into your file.
3. Replace `CHARS` value with the order of your language's alphabet. Notice that there is one space character at the
   beginning. All characters in the department names must exist here.
4. Change the texts on the right side with translations. Don't touch the key values which are on the left side.

Example:

**en.json**

```json
{
  "cmd-start": "Hello there!",
  "cmd-help": "Let me help you!",
  "settings-dnd-btn": "Change DND"
}
```

**tr.json**

```json
{
  "cmd-start": "Merhaba!",
  "cmd-help": "Sana yardım edeyim!",
  "settings-dnd-btn": "DND'yi Aç/Kapat"
}
```

## Important Note

Please remember, you don't need to translate them literally. Make them sound natural and right to the context.

After finishing, you can also add yourself down below!

## Contributors

- [Jeanne Kt](https://github.com/Mesaan) (French)
- [furkansimsekli](https://github.com/furkansimsekli) (English, French, Turkish)
- 