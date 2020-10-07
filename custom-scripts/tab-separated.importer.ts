/**
 * This function will parse token like this "token[label]"" and store the label.
 */
(fileContent: string): ConverterImportable => {
  const sentences = fileContent.split('[EOL]').filter((sentence) => sentence.trim().length > 0);
  let id = 0;
  const labels = [];
  const cells = sentences.map((sentence: string, lineIndex) => {
    let tokens = sentence.split('\n');
    tokens = tokens.filter((token) => !!token);
    tokens = tokens.map((token: string, tokenIndex) => {
      const labeledToken = token.split('\t');
      if (labeledToken.length > 1) {
        labels.push({
          id,
          startCellIndex: 0,
          startCellLine: lineIndex,
          startTokenIndex: tokenIndex,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: lineIndex,
          endTokenIndex: tokenIndex,
          endCharIndex: labeledToken[0].trim().length - 1,
          layer: 0,
          counter: 0,
          type: 'SPAN',
          labelSetItemId: labeledToken[1].trim(),
        });
        id++;
        return labeledToken[0].trim();
      }
      return token.trim();
    });
    

    return {
      line: lineIndex,
      index: 0,
      content: tokens.join(' '),
      tokens,
    };
  });

  return {
    name: 'Document name',
    cells,
    labels,
  };
};
