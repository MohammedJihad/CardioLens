import * as React from "react";

/** PlainLanguageBox — "What this means", verbatim from copy.md (/try). */
export function PlainLanguageBox() {
  return (
    <div className="rounded-md border-l-2 border-accent bg-subtle p-s5">
      <h3 className="text-xl">What this means</h3>
      <p className="mt-s2 text-base leading-normal text-muted">
        A higher model score means this input pattern looks more like the
        historical research patterns the model associates with heart disease in
        its training data. It is not a medical verdict, and it does not describe
        you. To understand your own health, talk to a qualified clinician.
      </p>
    </div>
  );
}
