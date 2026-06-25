import { THEME_STORAGE_KEY } from "@/lib/site";

/**
 * Inline, render-blocking script that applies a stored theme override BEFORE
 * first paint, so a manual choice doesn't flash. No stored value => the page
 * falls back to prefers-color-scheme (the default mechanism from styleguide.html).
 * Stores only a UI preference ("light"/"dark") — never any medical input.
 */
export function ThemeScript() {
  const js = `(function(){try{var t=localStorage.getItem('${THEME_STORAGE_KEY}');if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();`;
  return <script dangerouslySetInnerHTML={{ __html: js }} />;
}
