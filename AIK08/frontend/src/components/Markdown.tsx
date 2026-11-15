import { Fragment, ReactNode } from "react";

/** Trình render Markdown tối giản và AN TOÀN: chỉ tạo phần tử React (không dùng dangerouslySetInnerHTML). */
function inline(text: string, keyPrefix: string): ReactNode[] {
  const out: ReactNode[] = [];
  const pattern = /(\*\*[^*]+\*\*|`[^`]+`|\[E\d{1,6}\])/g;
  let last = 0;
  let match: RegExpExecArray | null;
  let n = 0;
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > last) out.push(text.slice(last, match.index));
    const token = match[0];
    const key = `${keyPrefix}-${n++}`;
    if (token.startsWith("**"))
      out.push(<strong key={key}>{token.slice(2, -2)}</strong>);
    else if (token.startsWith("`"))
      out.push(<code key={key}>{token.slice(1, -1)}</code>);
    else
      out.push(
        <span className="cite" key={key}>
          {token}
        </span>,
      );
    last = match.index + token.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

export function Markdown({ source }: { source: string }) {
  const blocks: ReactNode[] = [];
  let bullets: string[] = [];
  const flush = (i: number) => {
    if (bullets.length) {
      blocks.push(
        <ul key={`ul-${i}`}>
          {bullets.map((b, j) => (
            <li key={j}>{inline(b, `li-${i}-${j}`)}</li>
          ))}
        </ul>,
      );
      bullets = [];
    }
  };
  source.split("\n").forEach((raw, i) => {
    const line = raw.trimEnd();
    const bullet = /^\s*[-*]\s+(.*)$/.exec(line);
    if (bullet) {
      bullets.push(bullet[1]);
      return;
    }
    flush(i);
    const heading = /^(#{1,6})\s+(.*)$/.exec(line);
    if (heading) {
      const level = Math.min(heading[1].length + 1, 5);
      const Tag = `h${level}` as "h2" | "h3" | "h4" | "h5";
      blocks.push(<Tag key={i}>{inline(heading[2], `h-${i}`)}</Tag>);
    } else if (/^-{3,}$/.test(line)) blocks.push(<hr key={i} />);
    else if (line) blocks.push(<p key={i}>{inline(line, `p-${i}`)}</p>);
  });
  flush(source.length);
  return <Fragment>{blocks}</Fragment>;
}
