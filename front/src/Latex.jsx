import katex from 'katex';
import 'katex/dist/katex.min.css';

function Latex({ texString }) {
  const html = katex.renderToString(texString, {
    throwOnError: false,
  });

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}

export default Latex;
