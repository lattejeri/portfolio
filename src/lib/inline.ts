const escape = (str: string) =>
  str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Escape plain text, then turn [text](url) into links so it stays editable as plain text in the CMS.
export const inlineLinks = (text = '') =>
  escape(text).replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2">$1</a>');
