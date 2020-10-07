### Custom Script
- simple-importer.ts 

    It contains hard-coded import file function.

- text.importer.ts

    It will parse simple text files with space as token separator and \n as line separator. You can provide prelabeled token by adding "[LABEL]". See simple-text-prelabeled.txt file.

- tab-separated.importer.ts

    It will parse the text using \n as token separator and [EOL] as line separator. You can provide prelabeled token by adding \tLABEL after the token. See tab-separated-token.txt file for further information.