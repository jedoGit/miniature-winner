export function splitRecursively(
  text: string,
  chunkSize = 800,
  chunkOverlap = 100
): string[] {
  const separators = ["\n\n", "\n", ". ", " "];

  function recursiveSplit(txt: string, level = 0): string[] {
    if (txt.length <= chunkSize) return [txt];

    const sep = separators[level] ?? "";
    const pieces = sep ? txt.split(sep) : [txt];
    const chunks: string[] = [];

    let current = "";
    for (const piece of pieces) {
      if ((current + piece + sep).length < chunkSize) {
        current += piece + sep;
      } else {
        if (current) chunks.push(current.trim());
        current = piece + sep;
      }
    }
    if (current) chunks.push(current.trim());

    if (chunks.length === 1 && level < separators.length - 1) {
      return recursiveSplit(txt, level + 1);
    }

    // Handle overlap
    const merged: string[] = [];
    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      if (i > 0) {
        const prev = merged[merged.length - 1];
        const overlapText = prev.slice(-chunkOverlap);
        merged.push(overlapText + chunk);
      } else {
        merged.push(chunk);
      }
    }

    return merged;
  }

  return recursiveSplit(text);
}
