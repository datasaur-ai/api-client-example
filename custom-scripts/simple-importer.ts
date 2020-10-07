/**
 * This function should be written as this template and correctly implements ImportFunction interface.
 */
(fileContent: string): ConverterImportable => {
    return {
      name: 'Document name',
      cells: [
        {
          line: 0,
          index: 0,
          content: 'It was the best of times.',
          tokens: ['It', 'was', 'the', 'best', 'of', 'times', '.'],
        },
        {
          line: 1,
          index: 0,
          content: 'I had a dream.',
          tokens: ['I', 'had', 'a', 'dream', '.'],
        },
        {
          line: 2,
          index: 0,
          content: 'He said further scientific study was required and if it was found that action was needed it should be taken by the European Union.',
          tokens: ["He", "said", "further", "scientific", "study", "was", "required", "and", "if", "it", "was", "found", "that", "action", "was", "needed", "it", "should", "be", "taken", "by", "the", "European", "Union", "."],
        },
      ],
      labels: [{
          id: 1,
          startCellIndex: 0,
          startCellLine: 2,
          startTokenIndex: 0,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: 2,
          endTokenIndex: 0,
          endCharIndex: 1,
          layer: 0,
          counter: 0,
          type: 'SPAN',
          labelSetItemId: 'PER',
        }
        ,{
          id: 2,
          startCellIndex: 0,
          startCellLine: 2,
          startTokenIndex: 22,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: 2,
          endTokenIndex: 23,
          endCharIndex: 4,
          layer: 0,
          counter: 0,
          type: 'SPAN',
          labelSetItemId: 'GEO',
        },
        {
          id: 3,
          startCellIndex: 0,
          startCellLine: 2,
          startTokenIndex: 22,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: 2,
          endTokenIndex: 23,
          endCharIndex: 4,
          layer: 0,
          counter: 1,
          type: 'SPAN',
          labelSetItemId: 'GEO',
        },
        {
          id: 4,
          originId: 1,
          destinationId: 3,
          startCellIndex: 0,
          startCellLine: 2,
          startTokenIndex: 0,
          startCharIndex: 0,
          endCellIndex: 0,
          endCellLine: 2,
          endTokenIndex: 23,
          endCharIndex: 4,
          layer: 0,
          counter: 0,
          type: 'ARROW',
          labelSetItemId: 'ARROW LABEL',
        }
      ]
    };
  };
  