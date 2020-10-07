/**
 * This function will parse token like this "token[label]"" and store the label.
 */
(fileContent: string): ConverterImportable => {
  const regex = /(.+)\[(.+)\]/;
  const sentences = fileContent.split('\n').filter((sentence) => sentence.trim().length > 0);
  let id = 0;
  const labels = [];
  const cells = sentences.map((sentence: string, lineIndex) => {
    let tokens = sentence.split(' ');
    tokens = tokens.map((token: string, tokenIndex) => {
      const labeledToken = token.match(regex);
      if (labeledToken != null && labeledToken.length === 3) {
        labels.push({
          id,
          startCellIndex: 0,
          startCellLine: lineIndex,
          startTokenIndex: tokenIndex,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: lineIndex,
          endTokenIndex: tokenIndex,
          endCharIndex: labeledToken[1].length - 1,
          layer: 0,
          counter: 0,
          type: 'SPAN',
          labelSetItemId: labeledToken[2],
        });
        id++;
        return labeledToken[1];
      }
      return token;
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
